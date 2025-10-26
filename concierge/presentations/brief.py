"""Brief Presentation - minimal response with just result and current state."""
import json
from concierge.presentations.base import Presentation


class BriefPresentation(Presentation):
    
    def render_text(self, orchestrator) -> str:
        """
        Render brief response with just the result and current state.
        
        Used for task calls and actions after handshake to save tokens.
        """
        current_stage = orchestrator.get_current_stage()
        
        lines = [
            self.content,
            "",
            f"Current stage: {current_stage.name}",
            f"State: {self._format_current_state(current_stage)}",
            f"Available tasks: {self._format_available_tasks(current_stage)}",
            f"Available transitions: {self._format_available_transitions(current_stage)}",
        ]
        
        return "\n".join(lines)
    
    def _format_current_state(self, stage) -> str:
        """Format current state variables"""
        state_data = dict(stage.local_state.data)
        if state_data:
            return json.dumps(state_data)
        return "{}"
    
    def _format_available_tasks(self, stage) -> str:
        """List available task names"""
        if not stage.tasks:
            return "none"
        return ", ".join(stage.tasks.keys())
    
    def _format_available_transitions(self, stage) -> str:
        """List available transition targets"""
        if not stage.transitions:
            return "none"
        return ", ".join(stage.transitions)

