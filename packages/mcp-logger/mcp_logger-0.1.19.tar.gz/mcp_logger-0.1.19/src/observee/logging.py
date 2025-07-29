"""
Observee Python SDK - Tool and prompt usage logging
Copyright (C) 2025 Observee Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import json
import logging
import time
import asyncio
from typing import TypeVar, Callable, Awaitable, Any, List, Optional, Union
from functools import wraps
import httpx
from pydantic import BaseModel
from .config import API_ENDPOINT

# Configure logging
logger = logging.getLogger("observe-python-sdk")

# Global configuration
class ObserveeConfig:
    _mcp_server_name: str = None
    _api_key: Optional[str] = None

    @classmethod
    def set_mcp_server_name(cls, name: str) -> None:
        """Set the global MCP server name."""
        cls._mcp_server_name = name

    @classmethod
    def get_mcp_server_name(cls) -> str:
        """Get the global MCP server name."""
        if cls._mcp_server_name is None:
            raise ValueError("MCP server name not set. Call set_mcp_server_name() first.")
        return cls._mcp_server_name
        
    @classmethod
    def set_api_key(cls, api_key: str) -> None:
        """Set the global API key."""
        cls._api_key = api_key
        
    @classmethod
    def get_api_key(cls) -> Optional[str]:
        """Get the global API key if set."""
        return cls._api_key

class ToolUsageData(BaseModel):
    """Data model for tool usage logging."""
    mcp_server_name: str
    tool_name: str
    tool_input: Optional[str] = None
    tool_response: Optional[str] = None
    duration: float
    session_id: Optional[str] = None

class PromptUsageData(BaseModel):
    """Data model for prompt usage logging."""
    mcp_server_name: str
    prompt_name: str
    prompt_input: Optional[str] = None
    prompt_response: Optional[str] = None
    session_id: Optional[str] = None

async def log_usage(data: Union[ToolUsageData, PromptUsageData], api_endpoint: str = API_ENDPOINT) -> None:
    """
    Logs tool or prompt usage data to an external API endpoint.
    
    Args:
        data: ToolUsageData or PromptUsageData object containing usage information
        api_endpoint: API endpoint for logging (optional)
    """
    try:
        usage_type = "tool" if isinstance(data, ToolUsageData) else "prompt"
        identifier = data.tool_name if isinstance(data, ToolUsageData) else data.prompt_name
        logger.debug(f"log_usage called for {usage_type}: {identifier}")
        
        # Skip logging if no endpoint is configured
        if not api_endpoint:
            logger.info(f"{usage_type.title()} usage logging skipped: No API endpoint configured")
            return
        
        logger.debug(f"Sending request to: {api_endpoint}")
        
        try:
            # Prepare headers
            headers = {"Content-Type": "application/json"}
            
            # Add API key to header if available
            api_key = ObserveeConfig.get_api_key()
            if api_key:
                headers["X-API-Key"] = api_key
                
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    api_endpoint,
                    json=data.model_dump(),
                    headers=headers,
                    timeout=5.0  # 5 second timeout to avoid blocking
                )
            
            logger.info(f"{usage_type.title()} usage logged: {json.dumps(data.model_dump())} (status: {response.status_code})")
        except Exception as fetch_error:
            # Isolate request errors to prevent them from crashing the server
            logger.error(f"Failed to send log request: {str(fetch_error)}")
    except Exception as error:
        # Log error but don't fail the original operation
        logger.error(f"Exception in log_usage: {str(error)}")

def _safe_json_serialize(data: dict) -> str:
    """
    Safely serialize a dictionary to JSON, filtering out non-serializable objects.
    
    Args:
        data: Dictionary to serialize
        
    Returns:
        JSON string with only serializable values
    """
    def is_json_serializable(obj):
        """Check if an object is JSON serializable."""
        try:
            json.dumps(obj)
            return True
        except (TypeError, ValueError):
            return False
    
    # Filter out non-serializable values
    safe_data = {}
    for key, value in data.items():
        if is_json_serializable(value):
            safe_data[key] = value
        else:
            # Replace with a string representation for logging purposes
            safe_data[key] = f"<non-serializable: {type(value).__name__}>"
    
    return json.dumps(safe_data)

def observee_usage_logger(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    """
    A unified decorator that logs both tool and prompt usage for MCP functions.
    Automatically detects whether to log as tool or prompt based on function name.
    
    Args:
        func: The async function to decorate
        
    Returns:
        Decorated function with usage logging
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Auto-detect based on function name patterns
        func_name = func.__name__.lower()
        if any(keyword in func_name for keyword in ['prompt', 'template', 'message']):
            detected_type = "prompt"
        else:
            detected_type = "tool"
            
        # Extract name - for MCP servers, use the 'name' parameter if available
        usage_name = func.__name__
        arguments_dict = None
        
        # Check if this is an MCP call_tool or get_prompt pattern
        if func.__name__ == "call_tool" and len(args) >= 2:
            # First arg is 'name' (tool name), second arg is 'arguments' dict
            usage_name = args[0]  # Use actual tool name instead of function name
            arguments_dict = args[1]  # Get arguments dict for session ID extraction
        elif func.__name__ == "get_prompt" and len(args) >= 2:
            # First arg is 'name' (prompt name), second arg is 'arguments' dict
            usage_name = args[0]  # Use actual prompt name instead of function name
            arguments_dict = args[1]  # Get arguments dict
        elif func.__name__ in ["call_tool", "get_prompt"] and "name" in kwargs:
            # Handle case where name is passed as keyword argument
            usage_name = kwargs["name"]
            arguments_dict = kwargs.get("arguments")
        
        # Get MCP server name from global config
        server_name = ObserveeConfig.get_mcp_server_name()
        
        # Start timing for tools
        start_time = time.time() if detected_type == "tool" else None
        
        try:
            # Execute the original function
            response = await func(*args, **kwargs)
            
            # Prepare usage data based on type
            if detected_type == "tool":
                # Calculate execution time
                duration = (time.time() - start_time) * 1000
                
                # Initialize base usage data
                usage_data_dict = {
                    "mcp_server_name": server_name,
                    "tool_name": usage_name,
                    "duration": duration
                }
                
                # Extract session_id - check both direct kwargs and MCP arguments dict
                session_id = None
                if "session_id" in kwargs:
                    session_id = kwargs["session_id"]
                elif "server_session_id" in kwargs:
                    session_id = kwargs["server_session_id"]
                elif arguments_dict and isinstance(arguments_dict, dict):
                    # Check for MCP-style session ID in arguments dict
                    session_id = arguments_dict.get("server_session_id")
                
                if session_id:
                    usage_data_dict["session_id"] = session_id
                
                # Only include tool_input and tool_response if API key is set
                if ObserveeConfig.get_api_key():
                    # Convert response to string format for logging
                    if isinstance(response, list):
                        # Handle list of TextContent objects
                        response_str = "\n".join(
                            item.text if hasattr(item, 'text') else str(item)
                            for item in response
                        )
                    else:
                        # Handle other response types
                        response_str = str(response)
                    
                    # Use the extracted arguments_dict if available, otherwise fall back to kwargs
                    if arguments_dict is not None:
                        # Filter out MCP internal fields from tool input logging
                        mcp_internal_fields = {"server_session_id", "mcp_customer_id", "mcp_client_id"}
                        clean_arguments = {k: v for k, v in arguments_dict.items() if k not in mcp_internal_fields}
                        tool_input = _safe_json_serialize(clean_arguments)
                    else:
                        tool_input = _safe_json_serialize(kwargs)
                    usage_data_dict["tool_input"] = tool_input
                    usage_data_dict["tool_response"] = response_str
                
                usage_data = ToolUsageData(**usage_data_dict)
                
            else:  # prompt
                # Initialize base usage data
                usage_data_dict = {
                    "mcp_server_name": server_name,
                    "prompt_name": usage_name
                }
                
                # Extract session_id - check both direct kwargs and MCP arguments dict
                session_id = None
                if "session_id" in kwargs:
                    session_id = kwargs["session_id"]
                elif "server_session_id" in kwargs:
                    session_id = kwargs["server_session_id"]
                elif arguments_dict and isinstance(arguments_dict, dict):
                    # Check for MCP-style session ID in arguments dict
                    session_id = arguments_dict.get("server_session_id")
                
                if session_id:
                    usage_data_dict["session_id"] = session_id
                
                # Only include prompt_input and prompt_response if API key is set
                if ObserveeConfig.get_api_key():
                    # Convert response to string format for logging
                    if isinstance(response, list):
                        # Handle list of PromptMessage objects or similar
                        response_str = "\n".join(
                            item.content.text if hasattr(item, 'content') and hasattr(item.content, 'text')
                            else item.text if hasattr(item, 'text')
                            else str(item)
                            for item in response
                        )
                    else:
                        # Handle other response types
                        response_str = str(response)
                    
                    # Use the extracted arguments_dict if available, otherwise fall back to kwargs
                    if arguments_dict is not None:
                        # Filter out MCP internal fields from prompt input logging
                        mcp_internal_fields = {"server_session_id", "mcp_customer_id", "mcp_client_id"}
                        clean_arguments = {k: v for k, v in arguments_dict.items() if k not in mcp_internal_fields}
                        prompt_input = _safe_json_serialize(clean_arguments)
                    else:
                        prompt_input = _safe_json_serialize(kwargs)
                    usage_data_dict["prompt_input"] = prompt_input
                    usage_data_dict["prompt_response"] = response_str
                
                usage_data = PromptUsageData(**usage_data_dict)
            
            asyncio.create_task(log_usage(usage_data))
            
            return response
            
        except Exception as e:
            # Log error
            logger.error(f"Error in {usage_name}: {str(e)}")
            
            if detected_type == "tool":
                # Calculate execution time even for failed calls
                duration = (time.time() - start_time) * 1000
                
                # Initialize base usage data for error case
                usage_data_dict = {
                    "mcp_server_name": server_name,
                    "tool_name": usage_name,
                    "duration": duration
                }
                
                # Extract session_id - check both direct kwargs and MCP arguments dict
                session_id = None
                if "session_id" in kwargs:
                    session_id = kwargs["session_id"]
                elif "server_session_id" in kwargs:
                    session_id = kwargs["server_session_id"]
                elif arguments_dict and isinstance(arguments_dict, dict):
                    # Check for MCP-style session ID in arguments dict
                    session_id = arguments_dict.get("server_session_id")
                
                if session_id:
                    usage_data_dict["session_id"] = session_id
                
                # Only include tool_input and error response if API key is set
                if ObserveeConfig.get_api_key():
                    # Use the extracted arguments_dict if available, otherwise fall back to kwargs
                    if arguments_dict is not None:
                        # Filter out MCP internal fields from tool input logging
                        mcp_internal_fields = {"server_session_id", "mcp_customer_id", "mcp_client_id"}
                        clean_arguments = {k: v for k, v in arguments_dict.items() if k not in mcp_internal_fields}
                        tool_input = _safe_json_serialize(clean_arguments)
                    else:
                        tool_input = _safe_json_serialize(kwargs)
                    usage_data_dict["tool_input"] = tool_input
                    usage_data_dict["tool_response"] = str(e)
                
                usage_data = ToolUsageData(**usage_data_dict)
                
            else:  # prompt
                # Initialize base usage data for error case
                usage_data_dict = {
                    "mcp_server_name": server_name,
                    "prompt_name": usage_name
                }
                
                # Extract session_id - check both direct kwargs and MCP arguments dict
                session_id = None
                if "session_id" in kwargs:
                    session_id = kwargs["session_id"]
                elif "server_session_id" in kwargs:
                    session_id = kwargs["server_session_id"]
                elif arguments_dict and isinstance(arguments_dict, dict):
                    # Check for MCP-style session ID in arguments dict
                    session_id = arguments_dict.get("server_session_id")
                
                if session_id:
                    usage_data_dict["session_id"] = session_id
                
                # Only include prompt_input and error response if API key is set
                if ObserveeConfig.get_api_key():
                    # Use the extracted arguments_dict if available, otherwise fall back to kwargs
                    if arguments_dict is not None:
                        # Filter out MCP internal fields from prompt input logging
                        mcp_internal_fields = {"server_session_id", "mcp_customer_id", "mcp_client_id"}
                        clean_arguments = {k: v for k, v in arguments_dict.items() if k not in mcp_internal_fields}
                        prompt_input = _safe_json_serialize(clean_arguments)
                    else:
                        prompt_input = _safe_json_serialize(kwargs)
                    usage_data_dict["prompt_input"] = prompt_input
                    usage_data_dict["prompt_response"] = str(e)
                
                usage_data = PromptUsageData(**usage_data_dict)
            
            asyncio.create_task(log_usage(usage_data))
            raise
    
    return wrapper

