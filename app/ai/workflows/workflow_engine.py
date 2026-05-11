from typing import List, Dict, Any, Callable, Optional
from enum import Enum
from app.core.logger import logger

class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class WorkflowNode:
    def __init__(self, name: str, action: Callable, params: Optional[Dict[str, Any]] = None):
        self.name = name
        self.action = action
        self.params = params or {}
        self.next_nodes: List['WorkflowNode'] = []
        self.condition: Optional[Callable[[Dict[str, Any]], bool]] = None

    def add_next(self, node: 'WorkflowNode', condition: Optional[Callable[[Dict[str, Any]], bool]] = None):
        node.condition = condition
        self.next_nodes.append(node)
        return self

class WorkflowContext:
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.status: WorkflowStatus = WorkflowStatus.PENDING
        self.errors: List[str] = []
        self.current_node: Optional[str] = None

    def set_data(self, key: str, value: Any):
        self.data[key] = value

    def get_data(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def add_error(self, error: str):
        self.errors.append(error)
        self.status = WorkflowStatus.FAILED

class WorkflowEngine:
    def __init__(self):
        self.workflows: Dict[str, WorkflowNode] = {}

    def register_workflow(self, name: str, start_node: WorkflowNode):
        self.workflows[name] = start_node
        logger.info(f"Registered workflow: {name}")

    def execute(self, workflow_name: str, initial_data: Optional[Dict[str, Any]] = None) -> WorkflowContext:
        if workflow_name not in self.workflows:
            raise ValueError(f"Workflow not found: {workflow_name}")

        context = WorkflowContext()
        context.status = WorkflowStatus.RUNNING
        
        if initial_data:
            context.data.update(initial_data)

        start_node = self.workflows[workflow_name]
        self._execute_node(start_node, context)

        if context.status == WorkflowStatus.RUNNING:
            context.status = WorkflowStatus.COMPLETED

        logger.info(f"Workflow '{workflow_name}' completed with status: {context.status}")
        return context

    def _execute_node(self, node: WorkflowNode, context: WorkflowContext):
        if context.status == WorkflowStatus.FAILED:
            return

        context.current_node = node.name
        logger.debug(f"Executing node: {node.name}")

        try:
            result = node.action(context, **node.params)
            
            if result is not None:
                if isinstance(result, dict):
                    context.data.update(result)
                else:
                    context.set_data(f"{node.name}_result", result)

        except Exception as e:
            error_msg = f"Error executing node '{node.name}': {str(e)}"
            logger.error(error_msg)
            context.add_error(error_msg)
            return

        for next_node in node.next_nodes:
            if next_node.condition is None or next_node.condition(context.data):
                self._execute_node(next_node, context)
                break

    def list_workflows(self) -> List[str]:
        return list(self.workflows.keys())

workflow_engine = WorkflowEngine()