"""Test Tool - execution and schema."""
import asyncio
from pydantic import BaseModel, Field
from concierge.core import State, tool, construct


@construct()
class Output(BaseModel):
    result: str


@tool()
def simple_tool(state: State, x: int) -> dict:
    """A simple tool"""
    return {"result": x * 2}


@tool(output=Output)
def typed_tool(state: State, x: int = Field(ge=0, description="Positive number")) -> dict:
    """A typed tool"""
    return {"result": str(x)}


def test_tool_execution():
    state = State()
    result = asyncio.run(simple_tool._concierge_tool.execute(state, x=5))
    assert result == {"result": 10}


def test_tool_state_mutation():
    state = State()
    
    @tool()
    def mutate_tool(state: State, value: str) -> dict:
        state.set("key", value)
        return {}
    
    asyncio.run(mutate_tool._concierge_tool.execute(state, value="test"))
    assert state.get("key") == "test"


def test_tool_schema():
    schema = simple_tool._concierge_tool.to_schema()
    assert schema["name"] == "simple_tool"
    assert schema["description"] == "A simple tool"
    assert "input_schema" in schema


def test_tool_field_metadata():
    schema = typed_tool._concierge_tool.to_schema()
    input_schema = schema["input_schema"]
    assert "x" in input_schema["properties"]
    assert input_schema["properties"]["x"]["description"] == "Positive number"
    assert input_schema["properties"]["x"]["minimum"] == 0

