"""
Base provider interface for LLM integrations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class Provider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    async def process(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> str:
        """
        Process messages using the LLM provider.
        
        Args:
            messages: List of messages in provider format
            model: Model identifier
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            tools: Optional list of tools for function calling
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Generated response text
        """
        pass
    
    @abstractmethod
    def format_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format messages for the specific provider.
        
        Args:
            messages: Generic message format
            
        Returns:
            Provider-specific message format
        """
        pass