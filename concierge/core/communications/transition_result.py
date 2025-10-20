"""Transition result communication."""
from concierge.core.communications.base import Communications
from concierge.core.communications.messages import TRANSITION_RESULT_MESSAGE


class TransitionResultMessage(Communications):
    """Message after successful stage transition"""
    
    def render(self, context: dict) -> str:
        """Render transition result with new stage context"""
        return TRANSITION_RESULT_MESSAGE.format(
            from_stage=context["from_stage"],
            to_stage=context["to_stage"],
            stage_message=context["stage_message"]
        )

