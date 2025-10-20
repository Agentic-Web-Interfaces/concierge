"""Tool result communication."""
import json
from concierge.core.communications.base import Communications
from concierge.core.communications.messages import TOOL_RESULT_MESSAGE


class ToolResultMessage(Communications):
    """Message after tool execution"""
    
    def render(self, context: dict) -> str:
        """Render tool result with stage context"""
        result = context["result"]
        result_str = json.dumps(result, indent=2) if isinstance(result, dict) else str(result)
        
        return TOOL_RESULT_MESSAGE.format(
            tool_name=context["tool_name"],
            result=result_str,
            stage_message=context["stage_message"]
        )

