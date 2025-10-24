"""Language Engine: Parses JSON input and routes to orchestrator."""
import json
from concierge.core.workflow import Workflow
from concierge.core.actions import MethodCallAction, StageTransitionAction
from concierge.core.results import Result, ToolResult, TransitionResult, ErrorResult, StateInputRequiredResult
from concierge.engine.orchestrator import Orchestrator
from concierge.presentations import ComprehensivePresentation
from concierge.communications import (
    StageMessage,
    ToolResultMessage,
    TransitionResultMessage,
    ErrorMessage,
    StateInputRequiredMessage
)


class LanguageEngine:
    """
    Language engine that receives JSON input and routes to orchestrator.
    Handles parsing, execution, and message formatting.
    Creates and manages its own orchestrator instance.
    """
    
    def __init__(self, workflow: Workflow, session_id: str):
        self.workflow = workflow
        self.session_id = session_id
        self.orchestrator = Orchestrator(workflow, session_id)
    
    def get_initial_message(self) -> str:
        """Get initial handshake message for new session"""
        stage = self.orchestrator.get_current_stage()
        state = stage.local_state
        return StageMessage().render(stage, self.workflow, state)
    
    def get_error_message(self, error_text: str) -> str:
        """Format an error message"""
        return json.dumps({"error": error_text})
    
    def get_termination_message(self, session_id: str) -> str:
        """Format a termination message"""
        return json.dumps({"status": "terminated", "session_id": session_id})
    
    async def process(self, llm_json: dict) -> str:
        """
        Process LLM JSON input and return formatted message.
        Handles all exceptions internally.
        
        Expected formats:
        - {"action": "handshake"}
        - {"action": "method_call", "tool": "tool_name", "args": {...}}
        - {"action": "stage_transition", "stage": "stage_name"}
        - {"action": "state_input", "data": {"field1": "value1", ...}}
        """
        try:
            action_type = llm_json.get("action")
            
            if action_type == "handshake":
                return self.get_initial_message()
            
            elif action_type == "method_call":
                action = MethodCallAction(
                    tool_name=llm_json["tool"],
                    args=llm_json.get("args", {})
                )
                result = await self.orchestrator.execute_method_call(action)
                if isinstance(result, ToolResult):
                    return self._format_tool_result(result)
                return self._format_error_result(result)
            
            elif action_type == "stage_transition":
                action = StageTransitionAction(
                    target_stage=llm_json["stage"]
                )
                result = await self.orchestrator.execute_stage_transition(action)
                if isinstance(result, TransitionResult):
                    return self._format_transition_result(result)
                elif isinstance(result, StateInputRequiredResult):
                    return self._format_state_input_required(result)
                return self._format_error_result(result)
            
            elif action_type == "state_input":
                state_data = llm_json.get("data", {})
                self.orchestrator.populate_state(state_data)
                stage = self.orchestrator.get_current_stage()
                state = stage.local_state
                return StageMessage().render(stage, self.workflow, state)
            
            else:
                return self._format_error_result(ErrorResult(
                    message=f"Unknown action type: {action_type}",
                    presentation_type=ComprehensivePresentation
                ))
        except Exception as e:
            return self.get_error_message(str(e))
    
    def _format_tool_result(self, result: ToolResult) -> str:
        """Format tool execution result with current stage context"""
        content = ToolResultMessage().render(result)
        presentation = result.presentation_type(content)
        return presentation.render_text(self.orchestrator)
    
    def _format_transition_result(self, result: TransitionResult) -> str:
        """Format transition result with new stage context"""
        content = TransitionResultMessage().render(result)
        presentation = result.presentation_type(content)
        return presentation.render_text(self.orchestrator)
    
    def _format_error_result(self, result: ErrorResult) -> str:
        """Format error message"""
        content = ErrorMessage().render(result)
        presentation = result.presentation_type(content)
        return presentation.render_text(self.orchestrator)
    
    def _format_state_input_required(self, result: StateInputRequiredResult) -> str:
        """Format state input required message"""
        content = StateInputRequiredMessage().render(result)
        presentation = result.presentation_type(content)
        return presentation.render_text(self.orchestrator)

