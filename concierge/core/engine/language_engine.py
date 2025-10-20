"""Language Engine: Parses JSON input and routes to orchestrator."""
from concierge.core.actions import MethodCallAction, StageTransitionAction
from concierge.core.results import Result, ErrorResult
from concierge.core.engine.orchestrator import Orchestrator


class LanguageEngine:
    """
    Language engine that receives JSON input and routes to orchestrator.
    Handles parsing and conditional routing logic.
    """
    
    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator
    
    async def process(self, llm_json: dict) -> Result:
        """
        Process LLM JSON input and route to appropriate orchestrator method.
        
        Expected formats:
        - {"action": "method_call", "tool": "tool_name", "args": {...}}
        - {"action": "stage_transition", "stage": "stage_name"}
        """
        action_type = llm_json.get("action")
        
        if action_type == "method_call":
            action = MethodCallAction(
                tool_name=llm_json["tool"],
                args=llm_json.get("args", {})
            )
            return await self.orchestrator.execute_method_call(action)
        
        elif action_type == "stage_transition":
            action = StageTransitionAction(
                target_stage=llm_json["stage"]
            )
            return await self.orchestrator.execute_stage_transition(action)
        
        else:
            return ErrorResult(message=f"Unknown action type: {action_type}")

