import json
import logging
import time
from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from queue import Queue
import os
from datetime import datetime, timedelta

from .content_smart_chat import ContentSmartChat, SmartChatResponse
from .content_config import ContentConfig
from .content_search import IndexSearch, ContentSearch
from .content_adm_index_group import ContentAdmIndexGroup
from .content_adm_index import ContentAdmIndex

class AgentState(Enum):
    """Agent states for workflow management"""
    IDLE = "idle"
    PROCESSING = "processing"
    WAITING = "waiting"
    ERROR = "error"
    COMPLETED = "completed"


class AgentTask(Enum):
    """Types of tasks the agent can perform"""
    DOCUMENT_ANALYSIS = "document_analysis"
    CONVERSATION_MANAGEMENT = "conversation_management"
    SEARCH_OPTIMIZATION = "search_optimization"
    WORKFLOW_AUTOMATION = "workflow_automation"
    CONTENT_CLASSIFICATION = "content_classification"


@dataclass
class AgentWorkflow:
    """Represents a workflow that the agent can execute"""
    name: str
    description: str
    steps: List[Dict[str, Any]]
    required_parameters: List[str]
    estimated_duration: int  # in seconds
    priority: int = 1  # 1=low, 5=high


@dataclass
class AgentResponse:
    """Enhanced response from the AI agent"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    conversation_id: Optional[str] = None
    workflow_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    execution_time: Optional[float] = None


class SmartChatAgent:
    """
    AI Agent for Smart Chat that provides automated workflows, 
    conversation management, and intelligent document processing.
    """
    
    def __init__(self, content_config: ContentConfig, agent_name: str = "SmartChatAgent"):
        """
        Initialize the Smart Chat AI Agent.
        
        Args:
            content_config: ContentConfig object for API access
            agent_name: Name identifier for the agent
        """
        self.agent_name = agent_name
        self.content_config = content_config
        self.smart_chat = ContentSmartChat(content_config)
        self.content_search = ContentSearch(content_config)
        self.content_adm_index_group = ContentAdmIndexGroup(content_config)
        self.content_adm_index = ContentAdmIndex(content_config)
        self.logger = content_config.logger
        
        # Agent state management
        self.state = AgentState.IDLE
        self.current_task = None
        self.workflows: Dict[str, AgentWorkflow] = {}
        self.conversation_history: Dict[str, List[Dict[str, Any]]] = {}
        self.task_queue = Queue()
        self.results_queue = Queue()
        
        # Performance tracking
        self.execution_stats = {
            'total_queries': 0,
            'successful_queries': 0,
            'failed_queries': 0,
            'average_response_time': 0.0
        }
        
        # Initialize default workflows
        self._initialize_default_workflows()
        
        # Cargar índices válidos dinámicamente
        self.valid_indexes = self._load_valid_indexes()
        
        # Start background processing thread
        self._start_background_processor()
    
    def _initialize_default_workflows(self):
        """Initialize default workflows for common tasks"""
        
        # Document Analysis Workflow
        doc_analysis_workflow = AgentWorkflow(
            name="Document Analysis",
            description="Analyze documents and extract key information",
            steps=[
                {"action": "search_documents", "description": "Search for relevant documents"},
                {"action": "analyze_content", "description": "Analyze document content"},
                {"action": "extract_metadata", "description": "Extract key metadata"},
                {"action": "generate_summary", "description": "Generate analysis summary"}
            ],
            required_parameters=["search_criteria", "analysis_type"],
            estimated_duration=30,
            priority=3
        )
        self.workflows["document_analysis"] = doc_analysis_workflow
        
        # Conversation Management Workflow
        conv_workflow = AgentWorkflow(
            name="Conversation Management",
            description="Manage multi-turn conversations with context",
            steps=[
                {"action": "initialize_conversation", "description": "Start new conversation"},
                {"action": "process_query", "description": "Process user query"},
                {"action": "maintain_context", "description": "Maintain conversation context"},
                {"action": "generate_response", "description": "Generate contextual response"}
            ],
            required_parameters=["initial_query", "conversation_id"],
            estimated_duration=15,
            priority=4
        )
        self.workflows["conversation_management"] = conv_workflow
        
        # Content Classification Workflow
        classification_workflow = AgentWorkflow(
            name="Content Classification",
            description="Classify documents into categories",
            steps=[
                {"action": "search_documents", "description": "Search for documents to classify"},
                {"action": "analyze_content", "description": "Analyze document content"},
                {"action": "determine_category", "description": "Determine document category"},
                {"action": "apply_classification", "description": "Apply classification tags"}
            ],
            required_parameters=["classification_criteria", "target_categories"],
            estimated_duration=45,
            priority=2
        )
        self.workflows["content_classification"] = classification_workflow
    
    def _start_background_processor(self):
        """Start background thread for processing tasks"""
        self.background_thread = threading.Thread(
            target=self._background_processor,
            daemon=True,
            name=f"{self.agent_name}_processor"
        )
        self.background_thread.start()
        self.logger.info(f"Started background processor for {self.agent_name}")
    
    def _background_processor(self):
        """Background thread for processing queued tasks"""
        while True:
            try:
                if not self.task_queue.empty():
                    task = self.task_queue.get()
                    self._process_task(task)
                else:
                    time.sleep(0.1)  # Small delay to prevent busy waiting
            except Exception as e:
                self.logger.error(f"Error in background processor: {e}")
                time.sleep(1)
    
    def _process_task(self, task: Dict[str, Any]):
        """Process a single task"""
        try:
            self.state = AgentState.PROCESSING
            self.current_task = task
            
            task_type = task.get('type')
            task_data = task.get('data', {})
            
            if task_type == AgentTask.DOCUMENT_ANALYSIS:
                result = self._execute_document_analysis(task_data)
            elif task_type == AgentTask.CONVERSATION_MANAGEMENT:
                result = self._execute_conversation_management(task_data)
            elif task_type == AgentTask.SEARCH_OPTIMIZATION:
                result = self._execute_search_optimization(task_data)
            elif task_type == AgentTask.WORKFLOW_AUTOMATION:
                result = self._execute_workflow_automation(task_data)
            elif task_type == AgentTask.CONTENT_CLASSIFICATION:
                result = self._execute_content_classification(task_data)
            else:
                result = AgentResponse(
                    success=False,
                    message=f"Unknown task type: {task_type}"
                )
            
            self.results_queue.put(result)
            
        except Exception as e:
            self.logger.error(f"Error processing task: {e}")
            error_result = AgentResponse(
                success=False,
                message=f"Task processing failed: {str(e)}"
            )
            self.results_queue.put(error_result)
        finally:
            self.state = AgentState.IDLE
            self.current_task = None
    
    def reload_valid_indexes(self):
        """Permite recargar los índices válidos dinámicamente."""
        self.valid_indexes = self._load_valid_indexes()

    def get_valid_indexes(self):
        """Devuelve la lista de IDs de índices válidos actualmente cargados."""
        return sorted(self.valid_indexes)

    def _execute_document_analysis(self, task_data: Dict[str, Any]) -> AgentResponse:
        """Execute document analysis workflow"""
        start_time = time.time()
        try:
            # Filtrar criterios por índices válidos
            search_criteria = task_data.get('search_criteria', {})
            filtered_criteria = self._filter_valid_criteria(search_criteria)
            analysis_type = task_data.get('analysis_type', 'general')
            custom_query = task_data.get('custom_query', '')
            # Search for documents
            index_search = IndexSearch()
            for criteria in filtered_criteria:
                index_search.add_constraint(
                    index_name=criteria.get('index_name'),
                    operator=criteria.get('operator', 'EQ'),
                    index_value=criteria.get('index_value')
                )
            search_results = self.content_search.search_index(index_search)
            # Analyze documents (simulado)
            analysis_result = {
                'documents_analyzed': len(search_results) if search_results else 0,
                'analysis_type': analysis_type
            }
            execution_time = time.time() - start_time
            return AgentResponse(
                success=True,
                message="Document analysis completed",
                data=analysis_result,
                execution_time=execution_time,
                timestamp=datetime.now()
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Document analysis failed: {str(e)}",
                execution_time=time.time() - start_time
            )
    
    def _execute_conversation_management(self, task_data: Dict[str, Any]) -> AgentResponse:
        """Execute conversation management workflow"""
        start_time = time.time()
        
        try:
            conversation_id = task_data.get('conversation_id')
            user_query = task_data.get('query')
            document_ids = task_data.get('document_ids')
            
            # Get conversation history if available
            conversation_context = ""
            if conversation_id and conversation_id in self.conversation_history:
                # Build context from previous messages
                history = self.conversation_history[conversation_id]
                conversation_context = self._build_conversation_context(history)
            
            # Execute smart chat with context
            smart_chat_response = self.smart_chat.smart_chat(
                user_query,
                document_ids,
                conversation_context
            )
            
            # Update conversation history
            if conversation_id:
                if conversation_id not in self.conversation_history:
                    self.conversation_history[conversation_id] = []
                
                self.conversation_history[conversation_id].append({
                    'query': user_query,
                    'response': smart_chat_response.answer,
                    'timestamp': datetime.now().isoformat(),
                    'document_ids': document_ids
                })
            
            execution_time = time.time() - start_time
            
            return AgentResponse(
                success=True,
                message="Conversation processed successfully",
                data={
                    'response': smart_chat_response.answer,
                    'conversation_id': conversation_id,
                    'document_ids': smart_chat_response.object_ids,
                    'conversation_context': smart_chat_response.conversation
                },
                conversation_id=conversation_id,
                execution_time=execution_time,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Conversation management failed: {str(e)}",
                execution_time=time.time() - start_time
            )
    
    def _load_valid_indexes(self):
        """Exporta y carga los IDs de índices válidos de todos los grupos y de índices individuales."""
        output_dir = os.path.join(os.path.dirname(__file__), '../output')
        valid_indexes = set()
        # Exportar todos los grupos de índices (puedes ajustar el id para filtrar si es necesario)
        try:
            # Exportar grupos de índices
            group_file = self.content_adm_index_group.export_index_groups('', output_dir)
            if group_file and os.path.exists(group_file):
                with open(group_file, 'r', encoding='utf-8') as f:
                    groups = json.load(f)
                    for group in groups:
                        for topic in group.get('topics', []):
                            if 'id' in topic:
                                valid_indexes.add(topic['id'])
            # Exportar índices individuales (puedes ajustar el id para filtrar si es necesario)
            index_file = self.content_adm_index.export_indexes('', output_dir)
            if index_file and os.path.exists(index_file):
                with open(index_file, 'r', encoding='utf-8') as f:
                    indexes = json.load(f)
                    for topic in indexes:
                        if 'id' in topic:
                            valid_indexes.add(topic['id'])
        except Exception as e:
            self.logger.error(f"Error loading valid indexes: {e}")
        return valid_indexes

    def _filter_valid_criteria(self, criteria_list):
        """Filtra criterios de búsqueda para usar solo índices válidos."""
        filtered = []
        for crit in criteria_list:
            if crit.get('index_name') in self.valid_indexes:
                filtered.append(crit)
            else:
                self.logger.warning(f"[ADVERTENCIA] Índice no válido ignorado en búsqueda: {crit.get('index_name')}")
        return filtered

    def _execute_search_optimization(self, task_data: Dict[str, Any]) -> AgentResponse:
        """Execute search optimization workflow"""
        start_time = time.time()
        try:
            original_search = task_data.get('search_criteria', {})
            # Filtrar criterios por índices válidos
            filtered_search = self._filter_valid_criteria(original_search)
            optimization_type = task_data.get('optimization_type', 'relevance')
            # Create optimized search
            optimized_search = self._optimize_search_criteria(filtered_search, optimization_type)
            # Execute optimized search
            index_search = IndexSearch()
            for criteria in optimized_search:
                index_search.add_constraint(
                    index_name=criteria.get('index_name'),
                    operator=criteria.get('operator', 'EQ'),
                    index_value=criteria.get('index_value')
                )
            search_results = self.content_search.search_index(index_search)
            execution_time = time.time() - start_time
            return AgentResponse(
                success=True,
                message="Search optimization completed",
                data={
                    'original_search': original_search,
                    'optimized_search': optimized_search,
                    'results_count': len(search_results) if search_results else 0,
                    'optimization_type': optimization_type
                },
                execution_time=execution_time,
                timestamp=datetime.now()
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Search optimization failed: {str(e)}",
                execution_time=time.time() - start_time
            )
    
    def _execute_workflow_automation(self, task_data: Dict[str, Any]) -> AgentResponse:
        """Execute workflow automation"""
        start_time = time.time()
        try:
            workflow_name = task_data.get('workflow_name')
            workflow_params = task_data.get('workflow_params', {})
            if workflow_name not in self.workflows:
                return AgentResponse(
                    success=False,
                    message=f"Workflow '{workflow_name}' not found"
                )
            workflow = self.workflows[workflow_name]
            workflow_id = f"{workflow_name}_{int(time.time())}"
            # Si el workflow usa criterios de búsqueda, filtrarlos
            if 'search_criteria' in workflow_params:
                workflow_params['search_criteria'] = self._filter_valid_criteria(workflow_params['search_criteria'])
            # Ejecutar pasos del workflow
            results = []
            for step in workflow.steps:
                step_result = self._execute_workflow_step(step, workflow_params)
                results.append(step_result)
            execution_time = time.time() - start_time
            return AgentResponse(
                success=True,
                message=f"Workflow '{workflow_name}' completed successfully",
                data={
                    'workflow_name': workflow_name,
                    'steps_executed': len(results),
                    'step_results': results,
                    'workflow_params': workflow_params
                },
                workflow_id=workflow_id,
                execution_time=execution_time,
                timestamp=datetime.now()
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Workflow automation failed: {str(e)}",
                execution_time=time.time() - start_time
            )
    
    def _execute_content_classification(self, task_data: Dict[str, Any]) -> AgentResponse:
        """Execute content classification workflow"""
        start_time = time.time()
        try:
            classification_criteria = task_data.get('classification_criteria', {})
            # Filtrar criterios por índices válidos
            filtered_criteria = self._filter_valid_criteria(classification_criteria)
            target_categories = task_data.get('target_categories', [])
            # Search for documents to classify
            index_search = IndexSearch()
            for criteria in filtered_criteria:
                index_search.add_constraint(
                    index_name=criteria.get('index_name'),
                    operator=criteria.get('operator', 'EQ'),
                    index_value=criteria.get('index_value')
                )
            search_results = self.content_search.search_index(index_search)
            # Classify documents
            classification_query = self._build_classification_query(target_categories)
            smart_chat_response = self.smart_chat.smart_chat(
                classification_query,
                search_results
            )
            execution_time = time.time() - start_time
            return AgentResponse(
                success=True,
                message="Content classification completed",
                data={
                    'documents_classified': len(search_results) if search_results else 0,
                    'target_categories': target_categories,
                    'classification_result': smart_chat_response.answer,
                    'classified_documents': smart_chat_response.object_ids
                },
                execution_time=execution_time,
                timestamp=datetime.now()
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Content classification failed: {str(e)}",
                execution_time=time.time() - start_time
            )
    
    def _build_analysis_query(self, analysis_type: str, task_data: Dict[str, Any]) -> str:
        """Build analysis query based on type"""
        base_query = task_data.get('custom_query', '')
        
        if analysis_type == 'financial':
            return f"{base_query} Analyze the financial documents and provide a summary of key financial metrics, risks, and recommendations."
        elif analysis_type == 'legal':
            return f"{base_query} Review the legal documents and identify key legal terms, obligations, and potential issues."
        elif analysis_type == 'technical':
            return f"{base_query} Analyze the technical documents and provide insights on system architecture, configurations, and technical requirements."
        else:
            return f"{base_query} Provide a comprehensive analysis of the documents including key findings, patterns, and recommendations."
    
    def _build_conversation_context(self, history: List[Dict[str, Any]]) -> str:
        """Build conversation context from history"""
        if not history:
            return ""
        
        context_parts = []
        for entry in history[-5:]:  # Last 5 entries for context
            context_parts.append(f"Q: {entry.get('query', '')}")
            context_parts.append(f"A: {entry.get('response', '')}")
        
        return "\n".join(context_parts)
    
    def _optimize_search_criteria(self, original_search: List[Dict[str, Any]], optimization_type: str) -> List[Dict[str, Any]]:
        """Optimize search criteria based on type"""
        optimized = original_search.copy()
        
        if optimization_type == 'relevance':
            # Add relevance scoring
            for criteria in optimized:
                criteria['relevance_score'] = 1.0
        elif optimization_type == 'performance':
            # Limit results for performance
            optimized = optimized[:3]  # Limit to 3 criteria
        
        return optimized
    
    def _build_classification_query(self, target_categories: List[str]) -> str:
        """Build classification query"""
        categories_str = ", ".join(target_categories)
        return f"Classify the documents into the following categories: {categories_str}. For each document, specify which category it belongs to and provide a brief explanation."
    
    def _execute_workflow_step(self, step: Dict[str, Any], workflow_params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        action = step.get('action')
        description = step.get('description', '')
        
        # Placeholder for step execution logic
        return {
            'action': action,
            'description': description,
            'status': 'completed',
            'result': f"Executed {action}"
        }
    
    # Public API methods
    
    def submit_task(self, task_type: AgentTask, task_data: Dict[str, Any]) -> str:
        """
        Submit a task for processing by the agent.
        
        Args:
            task_type: Type of task to execute
            task_data: Data for the task
            
        Returns:
            Task ID for tracking
        """
        task_id = f"{task_type.value}_{int(time.time())}"
        
        task = {
            'id': task_id,
            'type': task_type,
            'data': task_data,
            'submitted_at': datetime.now().isoformat()
        }
        
        self.task_queue.put(task)
        self.logger.info(f"Submitted task {task_id} of type {task_type.value}")
        
        return task_id
    
    def get_task_result(self, timeout: float = 5.0) -> Optional[AgentResponse]:
        """
        Get the next available task result.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            AgentResponse if available, None otherwise
        """
        try:
            return self.results_queue.get(timeout=timeout)
        except:
            return None
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            'agent_name': self.agent_name,
            'state': self.state.value,
            'current_task': self.current_task,
            'queue_size': self.task_queue.qsize(),
            'results_available': self.results_queue.qsize(),
            'execution_stats': self.execution_stats,
            'available_workflows': list(self.workflows.keys())
        }
    
    def add_workflow(self, workflow: AgentWorkflow) -> None:
        """Add a new workflow to the agent"""
        self.workflows[workflow.name.lower().replace(' ', '_')] = workflow
        self.logger.info(f"Added workflow: {workflow.name}")
    
    def get_conversation_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Get conversation history for a specific conversation"""
        return self.conversation_history.get(conversation_id, [])
    
    def clear_conversation_history(self, conversation_id: str = "") -> None:
        """Clear conversation history"""
        if conversation_id:
            self.conversation_history.pop(conversation_id, None)
        else:
            self.conversation_history.clear()
    
    def get_workflow_info(self, workflow_name: str) -> Optional[AgentWorkflow]:
        """Get information about a specific workflow"""
        return self.workflows.get(workflow_name)
    
    def list_workflows(self) -> List[str]:
        """List all available workflows"""
        return list(self.workflows.keys()) 