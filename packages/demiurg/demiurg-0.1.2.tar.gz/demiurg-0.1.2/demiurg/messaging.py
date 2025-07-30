"""
Messaging Client for Demiurg Agents

This module provides simple functions for agents to communicate with users.
It handles all the complexity of interacting with the Demiurg backend.
Includes message queue to prevent race conditions with rapid successive messages.
"""

import asyncio
import base64
import logging
import mimetypes
import os
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable, Awaitable

import httpx
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class MessageHistory(BaseModel):
    """Message history response."""
    success: Optional[bool] = None
    messages: List[Dict[str, Any]] = []
    hasMore: bool = False  # camelCase to match API response
    limit: Optional[int] = None
    offset: Optional[int] = None


class MessageQueue:
    """Queue to handle messages sequentially per conversation to prevent race conditions."""
    
    def __init__(self):
        """Initialize the message queue system."""
        self.queues: Dict[str, asyncio.Queue] = defaultdict(asyncio.Queue)
        self.processing: Dict[str, bool] = defaultdict(bool)
        self.processors: Dict[str, asyncio.Task] = {}
        
        logger.info("Message queue system initialized")
    
    async def enqueue_message(
        self, 
        conversation_id: str, 
        message_handler: Callable[[Dict[str, Any]], Awaitable[Any]], 
        payload: Dict[str, Any]
    ) -> None:
        """
        Add message to the queue for sequential processing.
        
        Args:
            conversation_id: The conversation ID
            message_handler: The async function to handle the message
            payload: The message payload
        """
        # Add message to conversation-specific queue
        await self.queues[conversation_id].put((message_handler, payload))
        
        logger.info(f"Message enqueued for conversation {conversation_id}. Queue size: {self.queues[conversation_id].qsize()}")
        
        # Start processing task if not already running for this conversation
        if not self.processing[conversation_id]:
            self.processing[conversation_id] = True
            
            # Cancel any existing processor task for this conversation
            if conversation_id in self.processors:
                self.processors[conversation_id].cancel()
            
            # Start new processor task
            self.processors[conversation_id] = asyncio.create_task(
                self._process_conversation_queue(conversation_id)
            )
    
    async def _process_conversation_queue(self, conversation_id: str):
        """
        Process all messages in queue for a specific conversation sequentially.
        
        Args:
            conversation_id: The conversation ID to process
        """
        queue = self.queues[conversation_id]
        
        try:
            logger.info(f"Started processing queue for conversation {conversation_id}")
            
            # Keep processing until queue is empty
            while True:
                try:
                    # Wait for a message with timeout to avoid hanging forever
                    handler, payload = await asyncio.wait_for(queue.get(), timeout=1.0)
                    
                    try:
                        logger.info(f"Processing message in queue for conversation {conversation_id}")
                        await handler(payload)
                        logger.info(f"Successfully processed message for conversation {conversation_id}")
                    except Exception as e:
                        logger.error(f"Error processing message in queue for conversation {conversation_id}: {e}", exc_info=True)
                    finally:
                        queue.task_done()
                        
                except asyncio.TimeoutError:
                    # No more messages in queue, break the loop
                    break
                    
        except Exception as e:
            logger.error(f"Error in queue processor for conversation {conversation_id}: {e}", exc_info=True)
        finally:
            # Mark processing as complete
            self.processing[conversation_id] = False
            if conversation_id in self.processors:
                del self.processors[conversation_id]
            
            logger.info(f"Finished processing queue for conversation {conversation_id}")
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get status of all queues for debugging."""
        return {
            "active_conversations": list(self.processing.keys()),
            "processing_conversations": [cid for cid, processing in self.processing.items() if processing],
            "queue_sizes": {cid: queue.qsize() for cid, queue in self.queues.items() if queue.qsize() > 0},
            "active_processors": len(self.processors)
        }


class MessagingClient:
    """Client for interacting with Demiurg messaging system."""
    
    def __init__(self):
        """Initialize the messaging client with environment configuration."""
        self.backend_url = os.getenv("DEMIURG_BACKEND_URL", "http://backend:3000")
        self.agent_token = os.getenv("DEMIURG_AGENT_TOKEN", "")
        self.agent_id = os.getenv("DEMIURG_AGENT_ID", "")
        
        if not self.agent_token:
            raise ValueError("DEMIURG_AGENT_TOKEN environment variable is required")
        if not self.agent_id:
            raise ValueError("DEMIURG_AGENT_ID environment variable is required")
        
        self.headers = {
            "Authorization": f"Bearer {self.agent_token}",
            "Content-Type": "application/json"
        }
        
        # Initialize message queue
        self.message_queue = MessageQueue()
        
        logger.info(f"Messaging client initialized for agent {self.agent_id}")
    
    async def send_text_message(
        self, 
        conversation_id: str, 
        text: str, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send a text message to a conversation.
        
        Args:
            conversation_id: The channel/conversation ID
            text: The message text
            metadata: Optional metadata
            
        Returns:
            True if successful, False otherwise
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.backend_url}/api/agent-messaging/send",
                    headers=self.headers,
                    json={
                        "agentId": self.agent_id,
                        "channelId": conversation_id,
                        "content": text,
                        "messageType": "text",
                        "metadata": metadata or {}
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                return True
                
        except Exception as e:
            logger.error(f"Failed to send text message: {e}")
            return False
    
    async def send_file_message(
        self, 
        conversation_id: str, 
        file_path: str, 
        caption: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send a file to a conversation.
        
        Args:
            conversation_id: The channel/conversation ID
            file_path: Path to the file
            caption: Optional caption
            metadata: Optional metadata
            
        Returns:
            True if successful, False otherwise
        """
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                logger.error(f"File not found: {file_path}")
                return False
            
            # Check file size (10MB limit)
            file_size = file_path_obj.stat().st_size
            if file_size > 10 * 1024 * 1024:
                logger.error(f"File too large: {file_size} bytes (max 10MB)")
                return False
            
            # Read and encode file
            file_data = file_path_obj.read_bytes()
            
            # Detect MIME type
            mime_type, _ = mimetypes.guess_type(str(file_path))
            if not mime_type:
                mime_type = "application/octet-stream"
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.backend_url}/api/agent-messaging/send",
                    headers=self.headers,
                    json={
                        "agentId": self.agent_id,
                        "channelId": conversation_id,
                        "content": caption or f"Sent file: {file_path_obj.name}",
                        "messageType": "file",
                        "metadata": metadata or {},
                        "fileAttachment": {
                            "fileName": file_path_obj.name,
                            "mimeType": mime_type,
                            "base64Data": base64.b64encode(file_data).decode()
                        }
                    },
                    timeout=60.0
                )
                response.raise_for_status()
                return True
                
        except Exception as e:
            logger.error(f"Failed to send file: {e}")
            return False
    
    async def get_conversation_history(
        self, 
        conversation_id: str, 
        limit: int = 50, 
        offset: int = 0,
        provider: str = "openai"
    ) -> Optional[List[Dict[str, str]]]:
        """
        Get message history from a conversation formatted for the specified LLM provider.
        
        Args:
            conversation_id: The channel/conversation ID
            limit: Maximum messages to retrieve
            offset: Number of messages to skip
            provider: LLM provider format ("openai", "anthropic", "google", etc.)
            
        Returns:
            List of formatted messages for the provider or None
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.backend_url}/api/agent-messaging/history/{conversation_id}",
                    headers=self.headers,
                    params={"limit": limit, "offset": offset},
                    timeout=30.0
                )
                response.raise_for_status()
                history = MessageHistory(**response.json())
                
                # Format messages for the specified provider
                if not history or not history.messages:
                    return []
                
                # Sort messages by timestamp chronologically
                sorted_messages = sorted(history.messages, key=lambda x: x.get('timestamp', 0))
                
                if provider == "openai":
                    return self._format_for_openai(sorted_messages)
                elif provider == "anthropic":
                    # TODO: Implement Anthropic Claude format
                    # return self._format_for_anthropic(sorted_messages)
                    raise NotImplementedError(f"Provider '{provider}' formatting not yet implemented")
                elif provider == "google":
                    # TODO: Implement Google Gemini format
                    # return self._format_for_google(sorted_messages)
                    raise NotImplementedError(f"Provider '{provider}' formatting not yet implemented")
                elif provider == "cohere":
                    # TODO: Implement Cohere format
                    # return self._format_for_cohere(sorted_messages)
                    raise NotImplementedError(f"Provider '{provider}' formatting not yet implemented")
                else:
                    raise ValueError(f"Unknown provider: {provider}")
                
        except Exception as e:
            logger.error(f"Failed to get conversation history: {e}")
            return None
    
    def _format_for_openai(self, messages: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Format messages for OpenAI chat completion API."""
        formatted_messages = []
        
        for msg in messages:
            sender_type = msg.get('senderType', '')
            content = msg.get('content', '')
            
            if sender_type == 'user' and content:
                formatted_messages.append({
                    "role": "user",
                    "content": content
                })
            elif sender_type == 'agent' and content:
                formatted_messages.append({
                    "role": "assistant", 
                    "content": content
                })
            # Skip messages with unknown sender types or empty content
        
        return formatted_messages
    
    async def register_agent(self, endpoint_url: str) -> bool:
        """
        Register agent with the messaging system.
        
        Args:
            endpoint_url: URL where agent can be reached
            
        Returns:
            True if successful, False otherwise
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.backend_url}/api/agent-messaging/register",
                    headers=self.headers,
                    json={
                        "agentId": self.agent_id,
                        "endpointUrl": endpoint_url
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                logger.info(f"Agent registered with endpoint {endpoint_url}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to register agent: {e}")
            return False
    
    async def enqueue_message_for_processing(
        self, 
        conversation_id: str, 
        message_handler: Callable[[Dict[str, Any]], Awaitable[Any]], 
        payload: Dict[str, Any]
    ) -> None:
        """
        Enqueue a message for sequential processing to prevent race conditions.
        
        Args:
            conversation_id: The conversation ID
            message_handler: The async function to handle the message
            payload: The message payload
        """
        await self.message_queue.enqueue_message(conversation_id, message_handler, payload)
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get status of message queues for debugging."""
        return self.message_queue.get_queue_status()


# Global client instance
_client: Optional[MessagingClient] = None


def get_messaging_client() -> MessagingClient:
    """Get or create the global messaging client."""
    global _client
    if _client is None:
        _client = MessagingClient()
    return _client


# Convenience functions for easy use

async def send_text_message(
    conversation_id: str, 
    text: str, 
    metadata: Optional[Dict[str, Any]] = None
) -> bool:
    """Send a text message to a conversation."""
    client = get_messaging_client()
    return await client.send_text_message(conversation_id, text, metadata)


async def send_file_message(
    conversation_id: str, 
    file_path: str, 
    caption: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> bool:
    """Send a file to a conversation."""
    client = get_messaging_client()
    return await client.send_file_message(conversation_id, file_path, caption, metadata)


async def get_conversation_history(
    conversation_id: str, 
    limit: int = 50, 
    offset: int = 0,
    provider: str = "openai"
) -> Optional[List[Dict[str, str]]]:
    """Get message history from a conversation formatted for the specified LLM provider."""
    client = get_messaging_client()
    return await client.get_conversation_history(conversation_id, limit, offset, provider)


async def register_agent(endpoint_url: str) -> bool:
    """Register agent with the messaging system."""
    client = get_messaging_client()
    return await client.register_agent(endpoint_url)


async def enqueue_message_for_processing(
    conversation_id: str, 
    message_handler: Callable[[Dict[str, Any]], Awaitable[Any]], 
    payload: Dict[str, Any]
) -> None:
    """
    Enqueue a message for sequential processing to prevent race conditions.
    
    Args:
        conversation_id: The conversation ID
        message_handler: The async function to handle the message
        payload: The message payload
    """
    client = get_messaging_client()
    await client.enqueue_message_for_processing(conversation_id, message_handler, payload)


def get_queue_status() -> Dict[str, Any]:
    """Get status of message queues for debugging."""
    client = get_messaging_client()
    return client.get_queue_status()