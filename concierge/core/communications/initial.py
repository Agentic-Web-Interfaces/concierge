"""Initial message communication."""
import json
from concierge.core.communications.base import Communications
from concierge.core.communications.messages import INITIAL_MESSAGE


class InitialMessage(Communications):
    """Message for initial workflow selection"""
    
    def render(self, context: dict) -> str:
        """Render initial message with workflow options"""
        workflows = context["workflows"]
        
        workflows_list = []
        for i, wf in enumerate(workflows, 1):
            stages = ', '.join(wf["stages"])
            workflows_list.append(
                f"{i}. {wf['id']}: {wf['description']}\n"
                f"   Stages: {stages}"
            )
        
        return INITIAL_MESSAGE.format(
            app_name=context["app_name"],
            app_description=context["app_description"],
            workflow_count=len(workflows),
            workflows_list='\n'.join(workflows_list)
        )

