"""
High-level LLM processing functions.
"""

from typing import Any, Dict, List, Optional

from .models import Message
from .providers import get_provider


async def process_message(
    message: Message,
    messages: Optional[List[Dict[str, Any]]] = None,
    provider: str = "openai",
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    system_prompt: Optional[str] = None,
    **kwargs
) -> str:
    """
    Process a message using the specified LLM provider.
    
    This is a high-level convenience function that handles provider selection
    and message formatting.
    
    Args:
        message: The message to process
        messages: Optional conversation history
        provider: LLM provider name (default: "openai")
        model: Model to use (provider-specific)
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        system_prompt: Optional system prompt
        **kwargs: Additional provider-specific parameters
        
    Returns:
        Generated response text
    """
    # Get the provider
    llm_provider = get_provider(provider)
    
    # Build message list
    msg_list = []
    
    # Add system prompt if provided
    if system_prompt:
        msg_list.append({
            "role": "system",
            "content": system_prompt
        })
    
    # Add conversation history if provided
    if messages:
        msg_list.extend(messages)
    
    # Add the current message
    msg_list.append({
        "role": "user",
        "content": message.content
    })
    
    # Use provider-specific formatting
    formatted_messages = llm_provider.format_messages(msg_list)
    
    # Process with the provider
    response = await llm_provider.process(
        messages=formatted_messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs
    )
    
    return response