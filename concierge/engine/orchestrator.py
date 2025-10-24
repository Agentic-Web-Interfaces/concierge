"""
Orchestrator: Core business logic for workflow execution.
"""
from dataclasses import dataclass, field
from typing import Optional

from concierge.core.state import State
from concierge.core.stage import Stage
from concierge.core.workflow import Workflow
from concierge.core.actions import Action, MethodCallAction, StageTransitionAction
from concierge.core.results import Result, ToolResult, TransitionResult, ErrorResult, StateInputRequiredResult
from concierge.presentations import ComprehensivePresentation


@dataclass
class Orchestrator:
    """
    Orchestrator handles the core business logic of workflow execution.
    Maintains state and handles interactions.
    """
    workflow: Workflow
    session_id: str
    state: State = field(default_factory=State)
    history: list = field(default_factory=list)
    pending_transition: Optional[str] = None
    
    def __post_init__(self):
        """Initialize session with workflow's initial stage"""
        self.workflow.initialize()
        self.state = State()
        self.history = []
        self.pending_transition = None
    
    def get_current_stage(self) -> Stage:
        """Get current stage object"""
        return self.workflow.get_cursor()
    
    async def execute_method_call(self, action: MethodCallAction) -> Result:
        """Execute a method call action"""
        stage = self.get_current_stage()
        
        result = await self.workflow.call_tool(stage.name, action.tool_name, action.args)
        
        if result["type"] == "tool_result":
            self.history.append({
                "action": "method_call",
                "tool": action.tool_name,
                "args": action.args,
                "result": result["result"]
            })
            return ToolResult(
                tool_name=action.tool_name,
                result=result["result"],
                presentation_type=ComprehensivePresentation
            )
        else:
            return ErrorResult(
                message=result.get("message", result.get("error", "Unknown error")),
                presentation_type=ComprehensivePresentation
            )
    
    async def execute_stage_transition(self, action: StageTransitionAction) -> Result:
        """Execute a stage transition action"""
        stage = self.get_current_stage()
        
        validation = self.workflow.validate_transition(
            stage.name,
            action.target_stage,
            self.state
        )
        
        if not validation["valid"]:
            if validation.get("reason") == "missing_state":
                self.pending_transition = action.target_stage
                return StateInputRequiredResult(
                    target_stage=action.target_stage,
                    message=f"To transition to '{action.target_stage}', please provide: {validation['missing']}",
                    required_fields=validation["missing"],
                    presentation_type=ComprehensivePresentation
                )
            else:
                return ErrorResult(
                    message=validation["error"],
                    allowed=validation.get("allowed"),
                    presentation_type=ComprehensivePresentation
                )
        
        target = self.workflow.transition_to(action.target_stage)
        self.pending_transition = None
        
        self.history.append({
            "action": "stage_transition",
            "from": stage.name,
            "to": action.target_stage
        })
        
        return TransitionResult(
            from_stage=stage.name,
            to_stage=action.target_stage,
            presentation_type=ComprehensivePresentation
        )
    
    def populate_state(self, state_data: dict) -> None:
        """
        Store provided state in current stage's local_state.
        User will manually request transition again after this.
        """
        current_stage = self.get_current_stage()
        for key, value in state_data.items():
            current_stage.local_state.set(key, value)
    
    def get_session_info(self) -> dict:
        """Get current session information"""
        stage = self.get_current_stage()
        return {
            "session_id": self.session_id,
            "workflow": self.workflow.name,
            "current_stage": stage.name,
            "available_tools": [t.name for t in stage.tools.values()],
            "can_transition_to": stage.transitions,
            "state_summary": {
                construct: len(data) if isinstance(data, (list, dict, str)) else 1 
                for construct, data in self.state.data.items()
            },
            "history_length": len(self.history)
        }

