"""
Workflow execution engine for TAgent Community workflows.

Handles orchestration of agent groups with parallel/sequential execution,
context management, error handling, and result aggregation.
"""

import asyncio
import time
import logging
from typing import Dict, List, Any, Optional, Callable
from contextlib import asynccontextmanager

from .models import (
    WorkflowDefinition,
    WorkflowGroup,
    AgentDefinition,
    AgentResult,
    GroupResult,
    WorkflowResult,
    GroupExecutionMode,
)
from .evaluator import ConditionEvaluator, TemplateRenderer

logger = logging.getLogger(__name__)


class WorkflowExecutor:
    """
    Executes TAgent Community workflows with robust error handling and context management.
    
    Supports parallel and sequential agent execution within groups,
    conditional group execution, and comprehensive result tracking.
    """
    
    def __init__(
        self,
        agent_executor: Callable,
        llm_client: Optional[Callable] = None,
        max_concurrent_agents: int = 10,
    ):
        """
        Initialize the workflow executor.
        
        Args:
            agent_executor: Function to execute individual agents
            llm_client: LLM client for summarization (optional)
            max_concurrent_agents: Maximum number of concurrent agent executions
        """
        self.agent_executor = agent_executor
        self.llm_client = llm_client
        self.semaphore = asyncio.Semaphore(max_concurrent_agents)
        self.condition_evaluator = ConditionEvaluator()
        self.template_renderer = TemplateRenderer()
        
    async def execute_workflow(
        self, 
        workflow: WorkflowDefinition,
        input_context: Optional[Dict[str, Any]] = None,
    ) -> WorkflowResult:
        """
        Execute a complete workflow.
        
        Args:
            workflow: Workflow definition to execute
            input_context: Additional context to merge with initial_context
            
        Returns:
            WorkflowResult containing all execution results and final context
        """
        start_time = time.time()
        
        # Initialize context
        context = workflow.initial_context.copy()
        if input_context:
            context.update(input_context)
        
        # Initialize result tracking
        context.setdefault("results", {})
        context.setdefault("summaries", {})
        
        group_results = []
        workflow_success = True
        
        logger.info(f"Starting workflow execution: {workflow.name}")
        
        try:
            # Execute groups sequentially
            for group in workflow.groups:
                try:
                    # Evaluate condition if present
                    if group.condition:
                        should_execute = await self._evaluate_condition(
                            group.condition, 
                            context,
                            group.fail_on_condition_error
                        )
                        if not should_execute:
                            logger.info(f"Skipping group {group.name} due to condition")
                            continue
                    
                    # Execute the group
                    group_result = await self._execute_group(group, context)
                    group_results.append(group_result)
                    
                    # Update context with group results
                    await self._update_context_with_group_result(
                        context, group, group_result
                    )
                    
                    if not group_result.success:
                        workflow_success = False
                        logger.warning(f"Group {group.name} failed")
                        
                except Exception as e:
                    logger.error(f"Error executing group {group.name}: {e}")
                    workflow_success = False
                    
                    # Create failed group result
                    failed_result = GroupResult(
                        group_name=group.name,
                        success=False,
                        agent_results=[],
                        execution_time=0.0,
                        success_rate=0.0
                    )
                    group_results.append(failed_result)
            
            # Generate final summary if requested
            final_summary = None
            if workflow.final_summary_prompt and self.llm_client:
                try:
                    rendered_prompt = self.template_renderer.render(
                        workflow.final_summary_prompt, 
                        context
                    )
                    final_summary = await self._generate_summary(rendered_prompt, context)
                except Exception as e:
                    logger.warning(f"Failed to generate final summary: {e}")
            
            execution_time = time.time() - start_time
            
            return WorkflowResult(
                workflow_name=workflow.name,
                success=workflow_success,
                group_results=group_results,
                final_context=context,
                final_summary=final_summary,
                total_execution_time=execution_time,
                metadata=workflow.metadata
            )
            
        except Exception as e:
            logger.error(f"Workflow {workflow.name} failed with error: {e}")
            execution_time = time.time() - start_time
            
            return WorkflowResult(
                workflow_name=workflow.name,
                success=False,
                group_results=group_results,
                final_context=context,
                total_execution_time=execution_time,
                metadata=workflow.metadata
            )
    
    async def _execute_group(
        self, 
        group: WorkflowGroup, 
        context: Dict[str, Any]
    ) -> GroupResult:
        """Execute a single workflow group."""
        start_time = time.time()
        logger.info(f"Executing group: {group.name} ({group.execution_mode.value})")
        
        try:
            if group.execution_mode == GroupExecutionMode.PARALLEL:
                agent_results = await self._execute_agents_parallel(group, context)
            else:
                agent_results = await self._execute_agents_sequential(group, context)
            
            # Calculate success rate
            required_agents = [r for r in agent_results if self._is_agent_required(group, r.agent_name)]
            success_rate = sum(1 for r in required_agents if r.success) / len(required_agents) if required_agents else 1.0
            
            group_success = success_rate >= group.min_success_rate
            
            # Generate group summary if requested
            summary = None
            if group.summary_prompt and self.llm_client and group_success:
                try:
                    rendered_prompt = self.template_renderer.render(
                        group.summary_prompt, 
                        {**context, "group_results": agent_results}
                    )
                    summary = await self._generate_summary(rendered_prompt, context)
                except Exception as e:
                    logger.warning(f"Failed to generate group summary for {group.name}: {e}")
            
            execution_time = time.time() - start_time
            
            return GroupResult(
                group_name=group.name,
                success=group_success,
                agent_results=agent_results,
                summary=summary,
                execution_time=execution_time,
                success_rate=success_rate
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Group {group.name} execution failed: {e}")
            
            return GroupResult(
                group_name=group.name,
                success=False,
                agent_results=[],
                execution_time=execution_time,
                success_rate=0.0
            )
    
    async def _execute_agents_parallel(
        self, 
        group: WorkflowGroup, 
        context: Dict[str, Any]
    ) -> List[AgentResult]:
        """Execute agents in parallel."""
        tasks = []
        for agent in group.agents:
            task = asyncio.create_task(
                self._execute_single_agent(agent, context, group.timeout)
            )
            tasks.append(task)
        
        try:
            results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=group.timeout
            )
            
            agent_results = []
            for i, result in enumerate(results):
                if isinstance(result, AgentResult):
                    agent_results.append(result)
                else:
                    # Handle exception
                    agent_results.append(AgentResult(
                        agent_name=group.agents[i].name,
                        success=False,
                        error=str(result) if result else "Unknown error",
                        execution_time=0.0
                    ))
            
            return agent_results
            
        except asyncio.TimeoutError:
            logger.warning(f"Group {group.name} timed out")
            return [
                AgentResult(
                    agent_name=agent.name,
                    success=False,
                    error="Group timeout",
                    execution_time=group.timeout
                )
                for agent in group.agents
            ]
    
    async def _execute_agents_sequential(
        self, 
        group: WorkflowGroup, 
        context: Dict[str, Any]
    ) -> List[AgentResult]:
        """Execute agents sequentially."""
        agent_results = []
        remaining_time = group.timeout
        
        for agent in group.agents:
            if remaining_time <= 0:
                # No time remaining
                agent_results.append(AgentResult(
                    agent_name=agent.name,
                    success=False,
                    error="Group timeout",
                    execution_time=0.0
                ))
                continue
            
            agent_timeout = min(agent.timeout, remaining_time)
            start_time = time.time()
            
            result = await self._execute_single_agent(agent, context, agent_timeout)
            agent_results.append(result)
            
            elapsed = time.time() - start_time
            remaining_time -= elapsed
            
            # Update context with this agent's result for next agents
            if result.success and result.result:
                if "results" not in context:
                    context["results"] = {}
                if group.name not in context["results"]:
                    context["results"][group.name] = {}
                context["results"][group.name][agent.name] = result.result
        
        return agent_results
    
    async def _execute_single_agent(
        self, 
        agent: AgentDefinition, 
        context: Dict[str, Any],
        timeout: int
    ) -> AgentResult:
        """Execute a single agent with retry logic."""
        async with self.semaphore:
            for attempt in range(agent.retry_count + 1):
                start_time = time.time()
                
                try:
                    # Render prompt template with context
                    rendered_prompt = self.template_renderer.render(
                        agent.tool_config.prompt, 
                        context
                    )
                    
                    # Execute agent
                    result = await asyncio.wait_for(
                        self.agent_executor(
                            tools=agent.tool_config.tools,
                            prompt=rendered_prompt,
                            model=agent.tool_config.model,
                            temperature=agent.tool_config.temperature,
                            max_tokens=agent.tool_config.max_tokens,
                        ),
                        timeout=timeout
                    )
                    
                    execution_time = time.time() - start_time
                    
                    return AgentResult(
                        agent_name=agent.name,
                        success=True,
                        result=result,
                        execution_time=execution_time,
                        retry_count=attempt
                    )
                    
                except Exception as e:
                    execution_time = time.time() - start_time
                    error_msg = str(e)
                    
                    if attempt < agent.retry_count:
                        logger.warning(f"Agent {agent.name} attempt {attempt + 1} failed: {error_msg}, retrying...")
                        await asyncio.sleep(agent.retry_delay * (2 ** attempt))  # Exponential backoff
                        continue
                    else:
                        logger.error(f"Agent {agent.name} failed after {attempt + 1} attempts: {error_msg}")
                        return AgentResult(
                            agent_name=agent.name,
                            success=False,
                            error=error_msg,
                            execution_time=execution_time,
                            retry_count=attempt
                        )
    
    async def _evaluate_condition(
        self, 
        condition: str, 
        context: Dict[str, Any],
        fail_on_error: bool = True
    ) -> bool:
        """Evaluate a condition expression against the context."""
        try:
            return self.condition_evaluator.evaluate(condition, context)
        except Exception as e:
            logger.warning(f"Condition evaluation failed: {e}")
            if fail_on_error:
                raise
            return False
    
    async def _generate_summary(
        self, 
        prompt: str, 
        context: Dict[str, Any]
    ) -> Optional[str]:
        """Generate summary using LLM client."""
        if not self.llm_client:
            return None
        
        try:
            return await self.llm_client(prompt=prompt, context=context)
        except Exception as e:
            logger.warning(f"Summary generation failed: {e}")
            return None
    
    async def _update_context_with_group_result(
        self, 
        context: Dict[str, Any], 
        group: WorkflowGroup, 
        group_result: GroupResult
    ):
        """Update context with group execution results."""
        # Add agent results to context
        if "results" not in context:
            context["results"] = {}
        
        context["results"][group.name] = {}
        for agent_result in group_result.agent_results:
            if agent_result.success and agent_result.result:
                context["results"][group.name][agent_result.agent_name] = agent_result.result
        
        # Add group summary if available
        if group_result.summary:
            if "summaries" not in context:
                context["summaries"] = {}
            context["summaries"][group.name] = group_result.summary
    
    def _is_agent_required(self, group: WorkflowGroup, agent_name: str) -> bool:
        """Check if an agent is marked as required."""
        for agent in group.agents:
            if agent.name == agent_name:
                return agent.required
        return True  # Default to required if not found