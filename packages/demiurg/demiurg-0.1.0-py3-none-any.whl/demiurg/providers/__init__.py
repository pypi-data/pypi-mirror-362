"""
LLM Provider implementations for Demiurg agents.
"""

from typing import Optional

from ..exceptions import ProviderError
from .base import Provider
from .openai import OpenAIProvider

__all__ = [
    "Provider",
    "OpenAIProvider",
    "get_provider",
]

# Registry of available providers
_PROVIDERS = {
    "openai": OpenAIProvider,
}


def get_provider(name: str) -> Provider:
    """
    Get a provider instance by name.
    
    Args:
        name: Provider name (e.g., "openai", "anthropic")
        
    Returns:
        Provider instance
        
    Raises:
        ProviderError: If provider is not found or not implemented
    """
    if name not in _PROVIDERS:
        available = ", ".join(_PROVIDERS.keys())
        raise ProviderError(
            f"Provider '{name}' not found. Available providers: {available}"
        )
    
    provider_class = _PROVIDERS[name]
    return provider_class()