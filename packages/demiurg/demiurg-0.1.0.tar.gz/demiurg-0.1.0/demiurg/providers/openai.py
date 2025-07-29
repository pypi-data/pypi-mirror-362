"""
OpenAI provider implementation for Demiurg agents.
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

from ..exceptions import ProviderError
from .base import Provider

logger = logging.getLogger(__name__)


class OpenAIProvider(Provider):
    """OpenAI LLM provider implementation."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        try:
            self.client = OpenAI(
                default_headers={
                    'X-Session-Id': os.getenv('DEMIURG_SESSION_ID'),
                    'X-Agent-Id': os.getenv('DEMIURG_AGENT_ID'),
                    'X-User-Id': os.getenv('DEMIURG_USER_ID'),
                }
            )
            self.available = True
        except Exception as e:
            logger.warning(f"OpenAI client initialization failed: {e}")
            self.client = None
            self.available = False
    
    async def process(
        self,
        messages: List[Dict[str, Any]],
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> str:
        """
        Process messages using OpenAI's chat completion API.
        
        Args:
            messages: List of messages in OpenAI format
            model: OpenAI model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            tools: Optional list of tools for function calling
            **kwargs: Additional OpenAI-specific parameters
            
        Returns:
            Generated response text
            
        Raises:
            ProviderError: If OpenAI is not available or request fails
        """
        if not self.available or not self.client:
            raise ProviderError("OpenAI client is not available")
        
        try:
            # Log request details
            logger.info("=== SENDING TO OPENAI ===")
            logger.info(f"Model: {model}")
            logger.info(f"Temperature: {temperature}")
            logger.info(f"Max tokens: {max_tokens}")
            logger.info(f"Number of messages: {len(messages)}")
            
            for i, msg in enumerate(messages):
                content_preview = str(msg.get('content', ''))[:200]
                if len(str(msg.get('content', ''))) > 200:
                    content_preview += '...'
                logger.info(f"Message {i} ({msg.get('role', 'unknown')}): {content_preview}")
            
            if tools:
                logger.info(f"Tools available: {len(tools)}")
            
            logger.info("=== END OPENAI REQUEST ===")
            
            # Prepare request
            request_params = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                **kwargs  # Allow additional parameters
            }
            
            if tools:
                request_params["tools"] = tools
            
            # Make API call
            completion = self.client.chat.completions.create(**request_params)
            
            # Handle response
            response_message = completion.choices[0].message
            
            # Log response
            logger.info("=== OPENAI RESPONSE ===")
            logger.info(f"Response content: {response_message.content}")
            if response_message.tool_calls:
                logger.info(f"Tool calls: {len(response_message.tool_calls)}")
                for tool_call in response_message.tool_calls:
                    logger.info(f"Tool: {tool_call.function.name} with args: {tool_call.function.arguments}")
            logger.info("=== END OPENAI RESPONSE ===")
            
            # Return content (tool handling should be done by the agent)
            return response_message.content or ""
            
        except Exception as e:
            logger.error(f"Error calling OpenAI: {e}")
            raise ProviderError(f"OpenAI request failed: {str(e)}")
    
    def format_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format messages for OpenAI's expected format.
        
        OpenAI expects messages with 'role' and 'content' fields.
        Roles can be: 'system', 'user', 'assistant', 'tool'
        
        Args:
            messages: Generic message format
            
        Returns:
            OpenAI-formatted messages
        """
        formatted = []
        for msg in messages:
            # If already in OpenAI format, use as-is
            if 'role' in msg and 'content' in msg:
                formatted.append(msg)
            # Convert from generic format
            elif 'sender_type' in msg:
                if msg['sender_type'] == 'user':
                    formatted.append({
                        'role': 'user',
                        'content': msg.get('content', '')
                    })
                elif msg['sender_type'] == 'agent':
                    formatted.append({
                        'role': 'assistant',
                        'content': msg.get('content', '')
                    })
                elif msg['sender_type'] == 'system':
                    formatted.append({
                        'role': 'system',
                        'content': msg.get('content', '')
                    })
        
        return formatted
    
    async def transcribe_audio(self, file_path: str) -> str:
        """
        Transcribe audio using OpenAI's Whisper model.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Transcribed text
            
        Raises:
            ProviderError: If transcription fails
        """
        if not self.available or not self.client:
            raise ProviderError("OpenAI client is not available")
        
        try:
            with open(file_path, 'rb') as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
                return transcription
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            raise ProviderError(f"Audio transcription failed: {str(e)}")
    
    def is_vision_model(self, model: str) -> bool:
        """Check if a model supports vision capabilities."""
        vision_models = ['gpt-4o', 'gpt-4o-mini', 'gpt-4-vision-preview']
        return any(model.startswith(vm) for vm in vision_models)