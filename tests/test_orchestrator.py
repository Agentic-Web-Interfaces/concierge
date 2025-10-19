"""Test Orchestrator - runtime execution."""
import asyncio
from concierge.core import State, tool, stage, workflow
from concierge.core.engine import Orchestrator


@stage(name="start")
class StartStage:
    @tool()
    def init(self, state: State, value: int) -> dict:
        state.set("value", value)
        return {"result": value}


@stage(name="end")
class EndStage:
    @tool()
    def finalize(self, state: State) -> dict:
        return {"result": "done"}


@workflow(name="test_flow")
class TestFlow:
    start = StartStage
    end = EndStage
    
    transitions = {
        StartStage: [EndStage]
    }


def test_orchestrator_tool_call():
    wf = TestFlow._workflow
    orch = Orchestrator(wf, session_id="test")
    
    result = asyncio.run(orch.process_action({
        "action": "tool",
        "tool": "init",
        "args": {"value": 42}
    }))
    
    assert result["type"] == "tool_result"
    assert result["result"]["result"] == 42


def test_orchestrator_transition():
    wf = TestFlow._workflow
    orch = Orchestrator(wf, session_id="test")
    
    result = asyncio.run(orch.process_action({
        "action": "transition",
        "stage": "end"
    }))
    
    assert result["type"] == "transitioned"
    assert result["from"] == "start"
    assert result["to"] == "end"
    assert orch.current_stage == "end"


def test_orchestrator_invalid_transition():
    wf = TestFlow._workflow
    orch = Orchestrator(wf, session_id="test")
    
    result = asyncio.run(orch.process_action({
        "action": "transition",
        "stage": "start"
    }))
    
    assert result["type"] == "error"


def test_orchestrator_session_info():
    wf = TestFlow._workflow
    orch = Orchestrator(wf, session_id="test")
    
    info = orch.get_session_info()
    assert info["session_id"] == "test"
    assert info["workflow"] == "test_flow"
    assert info["current_stage"] == "start"

