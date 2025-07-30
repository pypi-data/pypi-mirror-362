"""
Tool integration utilities for Demiurg agents.

Supports multiple tool providers (Composio, MCP, etc.)
"""

import json
import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ..exceptions import ToolError

logger = logging.getLogger(__name__)


class ToolProvider(ABC):
    """Abstract base class for tool providers."""
    
    @abstractmethod
    def init_tools(
        self, 
        user_id: Optional[str] = None,
        enabled_tools: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Initialize and return available tools."""
        pass
    
    @abstractmethod
    async def execute_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute a single tool and return results."""
        pass


class ComposioProvider(ToolProvider):
    """Composio tool provider implementation."""
    
    def __init__(self):
        """Initialize Composio provider."""
        try:
            from composio import Composio
            self.client = Composio()
            self.available = True
        except ImportError:
            logger.warning("Composio not available")
            self.client = None
            self.available = False
    
    def init_tools(
        self, 
        user_id: Optional[str] = None,
        enabled_tools: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Initialize Composio tools."""
        if not self.available:
            return []
        
        try:
            # Get user ID
            if user_id is None:
                user_id = os.getenv("COMPOSIO_USER_ID", "default")
            
            # Get enabled tools list
            if enabled_tools is None:
                tools_env = os.getenv("COMPOSIO_TOOLS", "")
                enabled_tools = [t.strip() for t in tools_env.split(",") if t.strip()]
            
            if not enabled_tools:
                logger.info("No Composio tools configured")
                return []
            
            # Get tools from Composio
            tools = self.client.tools.get(
                user_id=user_id,
                toolkits=enabled_tools
            )
            
            logger.info(f"Loaded {len(tools)} Composio tools")
            return tools
            
        except Exception as e:
            logger.error(f"Failed to initialize Composio tools: {e}")
            raise ToolError(f"Composio initialization failed: {str(e)}")
    
    async def execute_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute a Composio tool."""
        if not self.available:
            raise ToolError("Composio not available")
        
        if user_id is None:
            user_id = os.getenv("COMPOSIO_USER_ID", "default")
        
        try:
            result = self.client.tools.execute(
                slug=tool_name,
                arguments=arguments,
                user_id=user_id
            )
            return result
        except Exception as e:
            logger.error(f"Error executing Composio tool {tool_name}: {e}")
            raise ToolError(f"Tool execution failed: {str(e)}")


# Registry of tool providers
_PROVIDERS: Dict[str, type] = {
    "composio": ComposioProvider,
}

# Cached provider instances
_provider_instances: Dict[str, ToolProvider] = {}


def get_tool_provider(name: str = "composio") -> ToolProvider:
    """
    Get a tool provider instance by name.
    
    Args:
        name: Provider name (e.g., "composio", "mcp")
        
    Returns:
        ToolProvider instance
        
    Raises:
        ToolError: If provider not found
    """
    if name not in _PROVIDERS:
        available = ", ".join(_PROVIDERS.keys())
        raise ToolError(
            f"Tool provider '{name}' not found. Available providers: {available}"
        )
    
    # Return cached instance if available
    if name not in _provider_instances:
        provider_class = _PROVIDERS[name]
        _provider_instances[name] = provider_class()
    
    return _provider_instances[name]


def register_tool_provider(name: str, provider_class: type):
    """
    Register a new tool provider.
    
    Args:
        name: Provider name
        provider_class: Provider class (must inherit from ToolProvider)
    """
    if not issubclass(provider_class, ToolProvider):
        raise ValueError("Provider class must inherit from ToolProvider")
    
    _PROVIDERS[name] = provider_class
    logger.info(f"Registered tool provider: {name}")


# High-level convenience functions

def init_tools(
    provider: str = "composio",
    user_id: Optional[str] = None,
    enabled_tools: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Initialize tools using the specified provider.
    
    Args:
        provider: Tool provider name
        user_id: User ID for provider
        enabled_tools: List of tools to enable
        
    Returns:
        List of tool definitions for LLM
    """
    tool_provider = get_tool_provider(provider)
    return tool_provider.init_tools(user_id, enabled_tools)


async def execute_tools(
    tool_calls: List[Any],
    provider: str = "composio",
    user_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Execute tool calls using the specified provider.
    
    Args:
        tool_calls: List of tool calls from LLM
        provider: Tool provider name
        user_id: User ID for provider
        
    Returns:
        List of tool results with 'tool_call_id' and 'output'
    """
    tool_provider = get_tool_provider(provider)
    results = []
    
    for tool_call in tool_calls:
        try:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            logger.info(f"Executing tool: {function_name} via {provider}")
            
            # Execute via provider
            result = await tool_provider.execute_tool(
                tool_name=function_name,
                arguments=arguments,
                user_id=user_id
            )
            
            results.append({
                "tool_call_id": tool_call.id,
                "output": result
            })
            
        except Exception as e:
            logger.error(f"Error executing tool {function_name}: {e}")
            results.append({
                "tool_call_id": tool_call.id,
                "output": {"error": str(e)}
            })
    
    return results


def format_tool_results(
    tool_results: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Format tool results for inclusion in LLM messages.
    
    Args:
        tool_results: List of tool execution results
        
    Returns:
        List of formatted messages for LLM
    """
    messages = []
    
    for result in tool_results:
        messages.append({
            "role": "tool",
            "tool_call_id": result["tool_call_id"],
            "content": json.dumps(result["output"])
        })
    
    return messages