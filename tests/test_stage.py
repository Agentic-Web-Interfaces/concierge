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
    assert len(TestStage.tools) == 2
    assert "tool1" in TestStage.tools
    assert "tool2" in TestStage.tools


def test_stage_local_state():
    # Execute tool2 which mutates local state
    asyncio.run(TestStage.tools["tool2"].execute(TestStage.local_state, y="test"))
    
    # Verify stage local state was updated
    assert TestStage.local_state.get("key") == "test"


def test_stage_instance_binding():
    tool_obj = TestStage.tools["tool1"]
    
    # Verify func is bound to instance (not unbound)
    assert hasattr(tool_obj.func, '__self__')

