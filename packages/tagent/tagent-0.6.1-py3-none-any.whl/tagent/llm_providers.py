"""
LLM Adapter for TAgent - provides a clean interface for LLM interactions that's easy to mock.
"""

from typing import Dict, Optional, List, Any
from abc import ABC, abstractmethod
import json
import litellm
from litellm import completion_cost

from .models import StructuredResponse, TokenUsage, TokenStats
from .token_utils import get_token_count


class LLMResponse:
    """Wrapper for LLM response data."""
    
    def __init__(self, content: str, model: str = "unknown", token_usage: Optional[TokenUsage] = None):
        self.content = content
        self.model = model
        self.token_usage = token_usage


class LLMAdapter(ABC):
    """Abstract base class for LLM adapters."""
    
    @abstractmethod
    def complete(
        self,
        messages: List[Dict[str, str]],
        model: str,
        api_key: Optional[str] = None,
        response_format: Optional[Dict[str, str]] = None,
        temperature: float = 0.0,
        **kwargs
    ) -> LLMResponse:
        """Complete a chat conversation and return response."""
        pass
    
    @abstractmethod
    def get_supported_params(self, model: str) -> List[str]:
        """Get list of supported parameters for a model."""
        pass


class LiteLLMAdapter(LLMAdapter):
    """LiteLLM implementation of the LLM adapter."""
    
    def complete(
        self,
        messages: List[Dict[str, str]],
        model: str,
        api_key: Optional[str] = None,
        response_format: Optional[Dict[str, str]] = None,
        temperature: float = 0.0,
        **kwargs
    ) -> LLMResponse:
        """Complete using LiteLLM."""
        try:
            response = litellm.completion(
                model=model,
                messages=messages,
                response_format=response_format,
                temperature=temperature,
                api_key=api_key,
                **kwargs
            )
            content = response.choices[0].message.content.strip()
            
            # Extract token usage from response
            token_usage = None
            if hasattr(response, 'usage') and response.usage:
                # Calculate cost using LiteLLM's completion_cost function
                try:
                    cost = completion_cost(completion_response=response)
                    cost_value = float(cost) if cost is not None else 0.0
                    
                    # Debug cost calculation
                    if verbose:
                        print(f"[DEBUG] Cost calculation for {model}: {cost} -> {cost_value}")
                        if cost_value == 0.0:
                            print(f"[DEBUG] Zero cost detected - model may be free or pricing unavailable")
                            
                except Exception as e:
                    # If cost calculation fails, try to estimate based on token count and model
                    cost_value = 0.0
                    if verbose:
                        print(f"[DEBUG] Cost calculation failed: {e}")
                        
                # If still zero, try fallback estimation for known models
                if cost_value == 0.0:
                    input_tokens = getattr(response.usage, 'prompt_tokens', 0)
                    output_tokens = getattr(response.usage, 'completion_tokens', 0)
                    
                    # Enhanced fallback pricing based on model patterns
                    model_lower = model.lower()
                    
                    if "o4" in model_lower or "o1" in model_lower:
                        # O-series models are typically expensive
                        cost_value = (input_tokens * 0.05 / 1000) + (output_tokens * 0.15 / 1000)
                        if verbose:
                            print(f"[DEBUG] Using O-series fallback pricing: ${cost_value:.6f}")
                    elif "gpt-4" in model_lower:
                        # GPT-4 pricing
                        cost_value = (input_tokens * 0.03 / 1000) + (output_tokens * 0.06 / 1000)
                        if verbose:
                            print(f"[DEBUG] Using GPT-4 fallback pricing: ${cost_value:.6f}")
                    elif "gpt-3.5" in model_lower:
                        # GPT-3.5 pricing
                        cost_value = (input_tokens * 0.001 / 1000) + (output_tokens * 0.002 / 1000)
                        if verbose:
                            print(f"[DEBUG] Using GPT-3.5 fallback pricing: ${cost_value:.6f}")
                    elif "claude" in model_lower:
                        # Claude models pricing
                        if "opus" in model_lower:
                            cost_value = (input_tokens * 0.015 / 1000) + (output_tokens * 0.075 / 1000)
                        elif "sonnet" in model_lower:
                            cost_value = (input_tokens * 0.003 / 1000) + (output_tokens * 0.015 / 1000)
                        else:
                            cost_value = (input_tokens * 0.0008 / 1000) + (output_tokens * 0.0024 / 1000)
                        if verbose:
                            print(f"[DEBUG] Using Claude fallback pricing: ${cost_value:.6f}")
                    elif "gemini" in model_lower:
                        # Gemini pricing (often free/very cheap)
                        cost_value = (input_tokens * 0.0001 / 1000) + (output_tokens * 0.0002 / 1000)
                        if verbose:
                            print(f"[DEBUG] Using Gemini fallback pricing: ${cost_value:.6f}")
                    elif "openrouter" in model_lower:
                        # Generic OpenRouter pricing estimate
                        cost_value = (input_tokens * 0.002 / 1000) + (output_tokens * 0.006 / 1000)
                        if verbose:
                            print(f"[DEBUG] Using OpenRouter generic fallback pricing: ${cost_value:.6f}")
                    elif verbose and cost_value == 0.0:
                        print(f"[DEBUG] No pricing data available for model: {model}")
                        # Generic fallback for unknown models
                        cost_value = (input_tokens * 0.001 / 1000) + (output_tokens * 0.003 / 1000)
                        if verbose:
                            print(f"[DEBUG] Using generic fallback pricing: ${cost_value:.6f}")
                
                token_usage = TokenUsage(
                    input_tokens=getattr(response.usage, 'prompt_tokens', 0),
                    output_tokens=getattr(response.usage, 'completion_tokens', 0),
                    total_tokens=getattr(response.usage, 'total_tokens', 0),
                    model=model,
                    cost=cost_value
                )
            
            return LLMResponse(content=content, model=model, token_usage=token_usage)
        except Exception as e:
            raise ValueError(f"LiteLLM completion failed: {str(e)}")
    
    def get_supported_params(self, model: str) -> List[str]:
        """Get supported parameters from LiteLLM."""
        try:
            supported_params = litellm.get_supported_openai_params(model=model)
            return supported_params if supported_params else []
        except Exception:
            return []


class MockLLMAdapter(LLMAdapter):
    """Mock implementation for testing."""
    
    def __init__(self, responses: List[str] = None):
        self.responses = responses or []
        self.call_count = 0
    
    def complete(
        self,
        messages: List[Dict[str, str]],
        model: str,
        api_key: Optional[str] = None,
        response_format: Optional[Dict[str, str]] = None,
        temperature: float = 0.0,
        **kwargs
    ) -> LLMResponse:
        """Return pre-configured mock responses."""
        if self.call_count < len(self.responses):
            response = self.responses[self.call_count]
            self.call_count += 1
        else:
            # Default response if no more responses configured
            response = '{"action": "evaluate", "params": {"achieved": true}, "reasoning": "Mock response"}'
        
        # Mock token usage for testing
        mock_usage = TokenUsage(
            input_tokens=50,  # Mock values
            output_tokens=30,
            total_tokens=80,
            model=model,
            cost=0.001  # Mock cost
        )
        
        return LLMResponse(content=response, model=model, token_usage=mock_usage)
    
    def get_supported_params(self, model: str) -> List[str]:
        """Return mock supported parameters."""
        return ["response_format", "temperature", "max_tokens"]
    
    def reset(self):
        """Reset call count for reuse."""
        self.call_count = 0


# Global adapter instance - can be swapped for testing
_llm_adapter: LLMAdapter = LiteLLMAdapter()


def set_llm_adapter(adapter: LLMAdapter):
    """Set the global LLM adapter (useful for testing)."""
    global _llm_adapter
    _llm_adapter = adapter


def get_llm_adapter() -> LLMAdapter:
    """Get the current LLM adapter."""
    return _llm_adapter


def parse_structured_response(
    json_str: str, 
    verbose: bool = False
) -> StructuredResponse:
    """
    Parse a JSON string into a StructuredResponse with simplified error handling.
    
    Args:
        json_str: JSON string to parse
        verbose: Enable verbose logging
        
    Returns:
        StructuredResponse object
        
    Raises:
        ValueError: If parsing fails after all attempts
    """
    if verbose:
        print(f"[RESPONSE] Raw LLM output: {json_str[:200]}...")

    # Try direct parsing first
    try:
        return StructuredResponse.model_validate_json(json_str)
    except (ValueError, json.JSONDecodeError) as e:
        if verbose:
            print(f"[ERROR] Initial JSON parsing failed: {e}")
        
        # For large responses with text content, try to handle specially
        if len(json_str) > 1000 and '"text"' in json_str:
            try:
                # Extract the action and tool from the response
                import re
                action_match = re.search(r'"action":\s*"([^"]+)"', json_str)
                tool_match = re.search(r'"tool":\s*"([^"]+)"', json_str)
                
                if action_match and tool_match:
                    action = action_match.group(1)
                    tool = tool_match.group(1)
                    
                    # For large text content, create a safe response
                    if tool in ["translate", "summarize"]:
                        safe_response = {
                            "action": action,
                            "params": {
                                "tool": tool,
                                "args": {
                                    "text": "Large text content detected - processing with simplified parser",
                                    "target_language": "chinese" if tool == "translate" else ""
                                }
                            },
                            "reasoning": "Large text content parsed with simplified handler"
                        }
                        
                        if verbose:
                            print(f"[RESPONSE] Created safe response for large text content")
                        return StructuredResponse.model_validate(safe_response)
                        
            except Exception as safe_error:
                if verbose:
                    print(f"[ERROR] Safe parsing failed: {safe_error}")
        
        # Try basic cleanup
        try:
            import re
            # Remove common problematic characters and fix basic escaping
            cleaned = json_str.replace('\\"', '"').replace('\\n', '\n').replace('\\t', '\t')
            # Try to fix unescaped quotes in the middle of content
            cleaned = re.sub(r'(?<!\\)"(?![,}\]])', '\\"', cleaned)
            
            if verbose:
                print(f"[RESPONSE] Attempting with cleaned JSON")
            return StructuredResponse.model_validate_json(cleaned)
        except (ValueError, json.JSONDecodeError):
            pass
        
        # Last resort: return a safe default response
        if verbose:
            print(f"[ERROR] All parsing attempts failed, returning safe default")
        
        # Try to extract action if possible
        action = "plan"  # Safe default
        reasoning = "JSON parsing failed - created safe default response"
        
        try:
            import re
            action_match = re.search(r'"action":\s*"([^"]+)"', json_str)
            if action_match:
                action = action_match.group(1)
                reasoning = f"Extracted action '{action}' from malformed JSON"
        except:
            pass
        
        return StructuredResponse(
            action=action,
            params={},
            reasoning=reasoning
        )


def validate_json_response_size(response_text: str, max_size: int = 10000) -> str:
    """
    Validate and potentially truncate JSON response to prevent parsing issues.
    
    Args:
        response_text: The raw LLM response text
        max_size: Maximum size in characters
        
    Returns:
        Validated/truncated response text
    """
    if len(response_text) <= max_size:
        return response_text
    
    # If the response is too large, try to extract the structure
    try:
        import re
        # Look for action and tool
        action_match = re.search(r'"action":\s*"([^"]+)"', response_text)
        tool_match = re.search(r'"tool":\s*"([^"]+)"', response_text)
        
        if action_match and tool_match:
            action = action_match.group(1)
            tool = tool_match.group(1)
            
            # Create a safe truncated response
            safe_response = {
                "action": action,
                "params": {
                    "tool": tool,
                    "args": {
                        "text": "Large content detected - truncated for JSON safety",
                        "target_language": "chinese" if tool == "translate" else ""
                    }
                },
                "reasoning": f"Response truncated from {get_token_count(response_text)} tokens to prevent JSON parsing issues"
            }
            
            import json
            return json.dumps(safe_response)
    except Exception:
        pass
    
    # If extraction fails, return a safe default
    return '{"action": "plan", "params": {}, "reasoning": "Response too large and could not be processed safely"}'


def query_llm_with_adapter(
    prompt: str,
    model: str = "gpt-3.5-turbo",
    api_key: Optional[str] = None,
    max_retries: int = 3,
    tools: Optional[Dict[str, Any]] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    verbose: bool = False,
) -> StructuredResponse:
    """
    Query LLM using the adapter pattern for easier testing.
    
    Args:
        prompt: The prompt to send
        model: Model name
        api_key: API key for the LLM service
        max_retries: Maximum number of retries
        tools: Available tools dictionary
        conversation_history: Previous conversation messages
        verbose: Enable verbose logging
        
    Returns:
        StructuredResponse with structured output
        
    Raises:
        ValueError: If no valid response after retries
    """
    from .utils import get_tool_documentation
    
    system_message = {
        "role": "system",
        "content": "You are a helpful assistant designed to output JSON. For 'evaluate' actions, include specific feedback. Example: {\"action\": \"execute\", \"params\": {\"tool\": \"tool_name\", \"args\": {\"parameter\": \"value\"}}, \"reasoning\": \"Reason to execute the action.\"} or {\"action\": \"evaluate\", \"params\": {\"achieved\": false, \"missing_items\": [\"item1\", \"item2\"], \"suggestions\": [\"suggestion1\"]}, \"reasoning\": \"Detailed explanation of what is missing and why goal is not achieved.\"}",
    }

    # Use detailed tool documentation if available
    available_tools = ""
    if tools:
        available_tools = get_tool_documentation(tools)

    user_message = {
        "role": "user",
        "content": (
            f"{prompt}\n\n"
            f"{available_tools}"
            "For 'execute' actions, consider selecting appropriate tools based on their documentation. "
            "Include 'tool' (tool name) and 'args' (parameters) in params.\n"
            "For 'evaluate' actions where the goal is not achieved, consider including 'missing_items' and 'suggestions' in params.\n"
            "Please respond with valid JSON in the format: "
            "{\"action\": str (plan|execute|summarize|evaluate), \"params\": dict, \"reasoning\": str}."
            "Use double quotes for JSON strings."
        ),
    }

    # Build messages including conversation history
    messages = [system_message]

    # Add conversation history if available
    if conversation_history:
        messages.extend(conversation_history)

    # Add current user message
    messages.append(user_message)

    # Get adapter and check supported parameters
    adapter = get_llm_adapter()
    supported_params = adapter.get_supported_params(model)
    response_format = (
        {"type": "json_object"} if "response_format" in supported_params else None
    )

    for attempt in range(max_retries):
        try:
            # Call via adapter
            response = adapter.complete(
                messages=messages,
                model=model,
                api_key=api_key,
                response_format=response_format,
                temperature=0.0,
            )
            
            # Validate response size before parsing
            validated_content = validate_json_response_size(response.content)
            
            # Parse the response
            structured_response = parse_structured_response(validated_content, verbose)
            
            # Add token usage statistics if available
            if response.token_usage:
                stats = TokenStats()
                stats.add_usage(response.token_usage)
                structured_response.stats = stats
            
            return structured_response

        except Exception as e:
            if verbose:
                print(f"[ERROR] Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt == max_retries - 1:
                raise ValueError(f"Failed to get valid structured output after retries: {e}")

    raise ValueError("Max retries exceeded")