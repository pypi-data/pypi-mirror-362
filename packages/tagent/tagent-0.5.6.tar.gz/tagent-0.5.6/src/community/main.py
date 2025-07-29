"""
Main interface for TAgent Community workflows.

Provides convenience functions for loading, executing, and managing workflows.
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Callable, Union, List

from .models import WorkflowDefinition, WorkflowResult
from .parser import WorkflowParser, WorkflowParseError
from .executor import WorkflowExecutor

logger = logging.getLogger(__name__)


class CommunityWorkflowManager:
    """
    High-level manager for TAgent Community workflows.
    
    Provides a simple interface for loading and executing workflows
    with proper error handling and logging.
    """
    
    def __init__(
        self,
        agent_executor: Callable,
        llm_client: Optional[Callable] = None,
        max_concurrent_agents: int = 10,
    ):
        """
        Initialize the workflow manager.
        
        Args:
            agent_executor: Function to execute individual agents
            llm_client: LLM client for summarization (optional)
            max_concurrent_agents: Maximum number of concurrent agent executions
        """
        self.parser = WorkflowParser()
        self.executor = WorkflowExecutor(
            agent_executor=agent_executor,
            llm_client=llm_client,
            max_concurrent_agents=max_concurrent_agents,
        )
    
    async def execute_workflow_file(
        self,
        workflow_file: Union[str, Path],
        input_context: Optional[Dict[str, Any]] = None,
    ) -> WorkflowResult:
        """
        Load and execute a workflow from a YAML file.
        
        Args:
            workflow_file: Path to the workflow YAML file
            input_context: Additional context to merge with workflow's initial_context
            
        Returns:
            WorkflowResult with execution results
            
        Raises:
            WorkflowParseError: If workflow loading fails
            Exception: If workflow execution fails
        """
        logger.info(f"Loading workflow from {workflow_file}")
        
        try:
            workflow = self.parser.parse_file(workflow_file)
            return await self.execute_workflow(workflow, input_context)
        except WorkflowParseError:
            raise
        except Exception as e:
            logger.error(f"Failed to execute workflow from {workflow_file}: {e}")
            raise
    
    async def execute_workflow(
        self,
        workflow: WorkflowDefinition,
        input_context: Optional[Dict[str, Any]] = None,
    ) -> WorkflowResult:
        """
        Execute a workflow definition.
        
        Args:
            workflow: WorkflowDefinition to execute
            input_context: Additional context to merge with workflow's initial_context
            
        Returns:
            WorkflowResult with execution results
        """
        logger.info(f"Executing workflow: {workflow.name}")
        
        try:
            result = await self.executor.execute_workflow(workflow, input_context)
            
            if result.success:
                logger.info(f"Workflow '{workflow.name}' completed successfully in {result.total_execution_time:.2f}s")
            else:
                logger.warning(f"Workflow '{workflow.name}' failed after {result.total_execution_time:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            raise
    
    def load_workflow(self, workflow_file: Union[str, Path]) -> WorkflowDefinition:
        """
        Load a workflow definition from a YAML file without executing it.
        
        Args:
            workflow_file: Path to the workflow YAML file
            
        Returns:
            Loaded WorkflowDefinition
            
        Raises:
            WorkflowParseError: If workflow loading fails
        """
        return self.parser.parse_file(workflow_file)
    
    def validate_workflow_file(self, workflow_file: Union[str, Path]) -> bool:
        """
        Validate a workflow YAML file without executing it.
        
        Args:
            workflow_file: Path to the workflow YAML file
            
        Returns:
            True if the workflow is valid, False otherwise
        """
        try:
            self.parser.parse_file(workflow_file)
            return True
        except Exception as e:
            logger.warning(f"Workflow validation failed: {e}")
            return False
    
    def list_example_workflows(self) -> List[Path]:
        """
        List available example workflow files.
        
        Returns:
            List of paths to example workflow files
        """
        examples_dir = Path(__file__).parent.parent.parent / "examples"
        if examples_dir.exists():
            return list(examples_dir.glob("*.yaml"))
        return []


# Convenience functions for direct usage
async def execute_workflow_file(
    workflow_file: Union[str, Path],
    agent_executor: Callable,
    input_context: Optional[Dict[str, Any]] = None,
    llm_client: Optional[Callable] = None,
    max_concurrent_agents: int = 10,
) -> WorkflowResult:
    """
    Convenience function to execute a workflow file directly.
    
    Args:
        workflow_file: Path to the workflow YAML file
        agent_executor: Function to execute individual agents
        input_context: Additional context for the workflow
        llm_client: LLM client for summarization (optional)
        max_concurrent_agents: Maximum number of concurrent agent executions
        
    Returns:
        WorkflowResult with execution results
    """
    manager = CommunityWorkflowManager(
        agent_executor=agent_executor,
        llm_client=llm_client,
        max_concurrent_agents=max_concurrent_agents,
    )
    
    return await manager.execute_workflow_file(workflow_file, input_context)


def load_workflow_file(workflow_file: Union[str, Path]) -> WorkflowDefinition:
    """
    Convenience function to load a workflow file.
    
    Args:
        workflow_file: Path to the workflow YAML file
        
    Returns:
        Loaded WorkflowDefinition
    """
    parser = WorkflowParser()
    return parser.parse_file(workflow_file)