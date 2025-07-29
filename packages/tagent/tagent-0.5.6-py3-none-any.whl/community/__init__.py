"""
TAgent Community Workflow Module

A modular system for orchestrating multiple AI agents in organized workflows.
Provides declarative YAML configuration and robust execution patterns.
"""

from .models import (
    GroupExecutionMode,
    BaseToolConfig,
    AgentDefinition,
    WorkflowGroup,
    WorkflowDefinition,
    AgentResult,
    GroupResult,
    WorkflowResult,
)
from .executor import WorkflowExecutor
from .parser import WorkflowParser, WorkflowParseError
from .evaluator import ConditionEvaluator, TemplateRenderer
from .main import CommunityWorkflowManager, execute_workflow_file, load_workflow_file

__all__ = [
    "GroupExecutionMode",
    "BaseToolConfig", 
    "AgentDefinition",
    "WorkflowGroup",
    "WorkflowDefinition",
    "AgentResult",
    "GroupResult", 
    "WorkflowResult",
    "WorkflowExecutor",
    "WorkflowParser",
    "WorkflowParseError",
    "ConditionEvaluator",
    "TemplateRenderer",
    "CommunityWorkflowManager",
    "execute_workflow_file",
    "load_workflow_file",
]