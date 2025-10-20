"""Result types for workflow execution."""
from dataclasses import dataclass
from typing import Any


@dataclass
class ToolResult:
    """Result of a tool execution"""
    tool_name: str
    result: Any
    error: str | None = None


@dataclass
class TransitionResult:
    """Result of a stage transition"""
    from_stage: str
    to_stage: str
    prompt: str


@dataclass
class ErrorResult:
    """Error result"""
    message: str
    allowed: list[str] | None = None


Result = ToolResult | TransitionResult | ErrorResult

