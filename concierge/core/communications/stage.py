"""Stage message communication."""
import json
from concierge.core.communications.base import Communications
from concierge.core.communications.messages import STAGE_MESSAGE


class StageMessage(Communications):
    """Message for stage execution context"""
    
    def render(self, context: dict) -> str:
        """Render stage message with available actions"""
        return STAGE_MESSAGE.format(
            workflow_name=context["workflow_name"],
            current_stage=context["current_stage"],
            stage_index=context["stage_index"],
            total_stages=context["total_stages"],
            stage_description=context["stage_description"],
            available_tools=', '.join(context["available_tools"]),
            next_stages=', '.join(context["next_stages"]),
            previous_stages=', '.join(context["previous_stages"]),
            state=json.dumps(context["state"], indent=2)
        )

