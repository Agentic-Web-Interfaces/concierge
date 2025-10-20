"""Error communication."""
from concierge.core.communications.base import Communications
from concierge.core.communications.messages import ERROR_MESSAGE


class ErrorMessage(Communications):
    """Message for errors"""
    
    def render(self, context: dict) -> str:
        """Render error message"""
        error_context = []
        
        if "allowed" in context:
            error_context.append(f"Allowed options: {', '.join(context['allowed'])}")
        
        return ERROR_MESSAGE.format(
            message=context["message"],
            context='\n'.join(error_context) if error_context else ""
        )

