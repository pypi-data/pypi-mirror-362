"""
Pydantic models for TAgent Community Workflow definitions.

These models provide type safety, validation, and serialization for workflow configurations.
"""

from typing import Dict, List, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field


class GroupExecutionMode(str, Enum):
    """Execution mode for agent groups."""
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"


class BaseToolConfig(BaseModel):
    """Base configuration for agent tools."""
    tools: List[str] = Field(..., description="List of tool names to use")
    prompt: str = Field(..., description="Prompt template for the agent")
    model: str = Field("gpt-4-turbo", description="LLM model to use")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Model temperature")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens for response")


class AgentDefinition(BaseModel):
    """Definition of a single agent within a workflow group."""
    name: str = Field(..., description="Unique name for the agent")
    tool_config: BaseToolConfig = Field(..., description="Tool configuration for the agent")
    timeout: int = Field(180, gt=0, description="Timeout in seconds for agent execution")
    required: bool = Field(True, description="Whether agent failure should fail the group")
    retry_count: int = Field(0, ge=0, description="Number of retries on failure")
    retry_delay: float = Field(1.0, ge=0.0, description="Delay between retries in seconds")


class WorkflowGroup(BaseModel):
    """A group of agents that execute together."""
    name: str = Field(..., description="Unique name for the group")
    agents: List[AgentDefinition] = Field(..., min_items=1, description="List of agents in the group")
    execution_mode: GroupExecutionMode = Field(
        GroupExecutionMode.PARALLEL, 
        description="How agents within the group should execute"
    )
    timeout: int = Field(300, gt=0, description="Total timeout for the group")
    min_success_rate: float = Field(
        1.0, 
        ge=0.0, 
        le=1.0, 
        description="Minimum success rate of required agents for group success"
    )
    summary_prompt: Optional[str] = Field(
        None, 
        description="Prompt for LLM to summarize group results"
    )
    condition: Optional[str] = Field(
        None, 
        description="Python expression to evaluate against context for conditional execution"
    )
    fail_on_condition_error: bool = Field(
        True, 
        description="Whether to fail if condition evaluation throws an error"
    )


class WorkflowDefinition(BaseModel):
    """Complete workflow definition."""
    name: str = Field(..., description="Unique name for the workflow")
    description: Optional[str] = Field(None, description="Human-readable description")
    version: str = Field("1.0", description="Workflow version")
    groups: List[WorkflowGroup] = Field(..., min_items=1, description="Ordered list of workflow groups")
    initial_context: Dict[str, Any] = Field(default_factory=dict, description="Initial context data")
    final_summary_prompt: Optional[str] = Field(
        None, 
        description="Prompt for generating final workflow summary"
    )
    global_timeout: Optional[int] = Field(
        None, 
        gt=0, 
        description="Global timeout for entire workflow execution"
    )
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class AgentResult(BaseModel):
    """Result from a single agent execution."""
    agent_name: str
    success: bool
    result: Any = None
    error: Optional[str] = None
    execution_time: float
    retry_count: int = 0


class GroupResult(BaseModel):
    """Result from a group execution."""
    group_name: str
    success: bool
    agent_results: List[AgentResult]
    summary: Optional[str] = None
    execution_time: float
    success_rate: float


class WorkflowResult(BaseModel):
    """Complete workflow execution result."""
    workflow_name: str
    success: bool
    group_results: List[GroupResult]
    final_context: Dict[str, Any]
    final_summary: Optional[str] = None
    total_execution_time: float
    metadata: Dict[str, Any] = Field(default_factory=dict)