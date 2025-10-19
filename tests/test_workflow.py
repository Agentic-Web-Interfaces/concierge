"""Test Workflow - stage registration and transitions."""
import asyncio
from concierge.core import State, tool, stage, workflow


@stage(name="stage1")
class Stage1:
    @tool()
    def action1(self, state: State) -> dict:
        return {"result": "stage1"}


@stage(name="stage2")
class Stage2:
    @tool()
    def action2(self, state: State) -> dict:
        return {"result": "stage2"}


@workflow(name="test_workflow")
class TestWorkflow:
    s1 = Stage1
    s2 = Stage2
    
    transitions = {
        Stage1: [Stage2],
        Stage2: [Stage1]
    }


def test_workflow_stage_registration():
    wf = TestWorkflow._workflow
    assert len(wf.stages) == 2
    assert "stage1" in wf.stages
    assert "stage2" in wf.stages


def test_workflow_initial_stage():
    wf = TestWorkflow._workflow
    assert wf.initial_stage == "stage1"


def test_workflow_transitions():
    wf = TestWorkflow._workflow
    assert wf.stages["stage1"].transitions == ["stage2"]
    assert wf.stages["stage2"].transitions == ["stage1"]


def test_workflow_can_transition():
    wf = TestWorkflow._workflow
    assert wf.can_transition("stage1", "stage2")
    assert not wf.can_transition("stage1", "stage1")


def test_workflow_validate_transition():
    wf = TestWorkflow._workflow
    state = State()
    
    result = wf.validate_transition("stage1", "stage2", state)
    assert result["valid"]
    
    result = wf.validate_transition("stage1", "stage1", state)
    assert not result["valid"]


def test_workflow_call_tool():
    wf = TestWorkflow._workflow
    result = asyncio.run(wf.call_tool("stage1", "action1", {}))
    assert result["type"] == "tool_result"
    assert result["result"] == {"result": "stage1"}

