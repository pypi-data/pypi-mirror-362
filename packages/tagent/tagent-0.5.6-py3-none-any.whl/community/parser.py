"""
YAML parser and workflow loader for TAgent Community workflows.

Handles loading and validation of workflow definitions from YAML files
with proper error handling and validation.
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Union, Optional
from pydantic import ValidationError

from .models import WorkflowDefinition, WorkflowGroup, AgentDefinition, BaseToolConfig

logger = logging.getLogger(__name__)


class WorkflowParseError(Exception):
    """Raised when workflow parsing fails."""
    pass


class WorkflowParser:
    """Parser for TAgent Community workflow YAML files."""
    
    def __init__(self):
        self.yaml_loader = yaml.SafeLoader
    
    def parse_file(self, file_path: Union[str, Path]) -> WorkflowDefinition:
        """
        Parse a workflow definition from a YAML file.
        
        Args:
            file_path: Path to the YAML workflow file
            
        Returns:
            Validated WorkflowDefinition instance
            
        Raises:
            WorkflowParseError: If parsing or validation fails
            FileNotFoundError: If the file doesn't exist
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Workflow file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.load(f, Loader=self.yaml_loader)
            
            return self.parse_dict(data)
            
        except yaml.YAMLError as e:
            raise WorkflowParseError(f"YAML parsing error in {file_path}: {e}")
        except Exception as e:
            raise WorkflowParseError(f"Error loading workflow from {file_path}: {e}")
    
    def parse_dict(self, data: Dict[str, Any]) -> WorkflowDefinition:
        """
        Parse a workflow definition from a dictionary.
        
        Args:
            data: Dictionary containing workflow definition
            
        Returns:
            Validated WorkflowDefinition instance
            
        Raises:
            WorkflowParseError: If parsing or validation fails
        """
        try:
            # Validate and normalize the data
            normalized_data = self._normalize_workflow_data(data)
            
            # Create and validate the workflow definition
            workflow = WorkflowDefinition(**normalized_data)
            
            # Additional validation
            self._validate_workflow_consistency(workflow)
            
            return workflow
            
        except ValidationError as e:
            raise WorkflowParseError(f"Workflow validation error: {e}")
        except Exception as e:
            raise WorkflowParseError(f"Error parsing workflow: {e}")
    
    def parse_string(self, yaml_content: str) -> WorkflowDefinition:
        """
        Parse a workflow definition from a YAML string.
        
        Args:
            yaml_content: YAML content as string
            
        Returns:
            Validated WorkflowDefinition instance
            
        Raises:
            WorkflowParseError: If parsing or validation fails
        """
        try:
            data = yaml.load(yaml_content, Loader=self.yaml_loader)
            return self.parse_dict(data)
            
        except yaml.YAMLError as e:
            raise WorkflowParseError(f"YAML parsing error: {e}")
    
    def _normalize_workflow_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize and validate workflow data structure."""
        if not isinstance(data, dict):
            raise WorkflowParseError("Workflow definition must be a dictionary")
        
        # Ensure required fields exist
        if 'name' not in data:
            raise WorkflowParseError("Workflow must have a 'name' field")
        
        if 'groups' not in data:
            raise WorkflowParseError("Workflow must have a 'groups' field")
        
        # Normalize groups
        if not isinstance(data['groups'], list):
            raise WorkflowParseError("'groups' must be a list")
        
        normalized_groups = []
        for i, group_data in enumerate(data['groups']):
            try:
                normalized_group = self._normalize_group_data(group_data)
                normalized_groups.append(normalized_group)
            except Exception as e:
                raise WorkflowParseError(f"Error in group {i}: {e}")
        
        data['groups'] = normalized_groups
        
        # Set defaults for optional fields
        data.setdefault('initial_context', {})
        data.setdefault('metadata', {})
        
        return data
    
    def _normalize_group_data(self, group_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize and validate group data structure."""
        if not isinstance(group_data, dict):
            raise WorkflowParseError("Group definition must be a dictionary")
        
        # Ensure required fields
        if 'name' not in group_data:
            raise WorkflowParseError("Group must have a 'name' field")
        
        if 'agents' not in group_data:
            raise WorkflowParseError("Group must have an 'agents' field")
        
        # Normalize agents
        if not isinstance(group_data['agents'], list):
            raise WorkflowParseError("'agents' must be a list")
        
        normalized_agents = []
        for i, agent_data in enumerate(group_data['agents']):
            try:
                normalized_agent = self._normalize_agent_data(agent_data)
                normalized_agents.append(normalized_agent)
            except Exception as e:
                raise WorkflowParseError(f"Error in agent {i} of group '{group_data.get('name', 'unknown')}': {e}")
        
        group_data['agents'] = normalized_agents
        
        return group_data
    
    def _normalize_agent_data(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize and validate agent data structure."""
        if not isinstance(agent_data, dict):
            raise WorkflowParseError("Agent definition must be a dictionary")
        
        # Ensure required fields
        if 'name' not in agent_data:
            raise WorkflowParseError("Agent must have a 'name' field")
        
        if 'tool_config' not in agent_data:
            raise WorkflowParseError("Agent must have a 'tool_config' field")
        
        # Normalize tool_config
        tool_config = agent_data['tool_config']
        if not isinstance(tool_config, dict):
            raise WorkflowParseError("'tool_config' must be a dictionary")
        
        # Ensure required tool_config fields
        if 'tools' not in tool_config:
            raise WorkflowParseError("tool_config must have a 'tools' field")
        
        if 'prompt' not in tool_config:
            raise WorkflowParseError("tool_config must have a 'prompt' field")
        
        # Ensure tools is a list
        if not isinstance(tool_config['tools'], list):
            raise WorkflowParseError("'tools' must be a list")
        
        return agent_data
    
    def _validate_workflow_consistency(self, workflow: WorkflowDefinition):
        """Perform additional consistency validation on the workflow."""
        # Check for duplicate group names
        group_names = set()
        for group in workflow.groups:
            if group.name in group_names:
                raise WorkflowParseError(f"Duplicate group name: {group.name}")
            group_names.add(group.name)
            
            # Check for duplicate agent names within group
            agent_names = set()
            for agent in group.agents:
                if agent.name in agent_names:
                    raise WorkflowParseError(f"Duplicate agent name '{agent.name}' in group '{group.name}'")
                agent_names.add(agent.name)
            
            # Validate min_success_rate logic
            required_count = sum(1 for agent in group.agents if agent.required)
            if required_count == 0 and group.min_success_rate > 0:
                logger.warning(f"Group '{group.name}' has min_success_rate > 0 but no required agents")
    
    def save_workflow(self, workflow: WorkflowDefinition, file_path: Union[str, Path]):
        """
        Save a workflow definition to a YAML file.
        
        Args:
            workflow: WorkflowDefinition to save
            file_path: Path where to save the YAML file
        """
        file_path = Path(file_path)
        
        try:
            # Convert to dictionary for YAML serialization
            workflow_dict = workflow.model_dump(exclude_none=True, by_alias=True)
            
            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(
                    workflow_dict,
                    f,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                    indent=2
                )
            
            logger.info(f"Workflow saved to {file_path}")
            
        except Exception as e:
            raise WorkflowParseError(f"Error saving workflow to {file_path}: {e}")
    
    def validate_yaml_syntax(self, file_path: Union[str, Path]) -> bool:
        """
        Check if a YAML file has valid syntax without full parsing.
        
        Args:
            file_path: Path to the YAML file
            
        Returns:
            True if syntax is valid, False otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                yaml.load(f, Loader=self.yaml_loader)
            return True
        except Exception:
            return False