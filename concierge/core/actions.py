"""Action types for workflow execution."""
from dataclasses import dataclass
from typing import Any


@dataclass
class MethodCallAction:
    """Action to call a tool in current stage"""
    tool_name: str
    args: dict[str, Any]


@dataclass
class StageTransitionAction:
    """Action to transition to a new stage"""
    target_stage: str


Action = MethodCallAction | StageTransitionAction

