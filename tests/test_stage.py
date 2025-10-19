"""Test Stage - tool discovery and local state."""
import asyncio
from concierge.core import State, tool, stage


@stage(name="test_stage")
class TestStage:
    """Test stage"""
    
    @tool()
    def tool1(self, state: State, x: int) -> dict:
        """First tool"""
        return {"result": x}
    
    @tool()
    def tool2(self, state: State, y: str) -> dict:
        """Second tool"""
        state.set("key", y)
        return {"result": y}


def test_stage_tool_discovery():
    stage_obj = TestStage._stage
    assert len(stage_obj.tools) == 2
    assert "tool1" in stage_obj.tools
    assert "tool2" in stage_obj.tools


def test_stage_local_state():
    stage_obj = TestStage._stage
    
    # Execute tool2 which mutates local state
    asyncio.run(stage_obj.tools["tool2"].execute(stage_obj.local_state, y="test"))
    
    # Verify stage local state was updated
    assert stage_obj.local_state.get("key") == "test"


def test_stage_instance_binding():
    stage_obj = TestStage._stage
    tool_obj = stage_obj.tools["tool1"]
    
    # Verify func is bound to instance (not unbound)
    assert hasattr(tool_obj.func, '__self__')

