"""
Base Agent class for Demiurg framework.
"""

import logging
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# FastAPI is optional - only needed if using with FastAPI server
try:
    from fastapi.responses import JSONResponse
except ImportError:
    JSONResponse = None

from .exceptions import DemiurgError
from .llm import process_message as llm_process_message
from .messaging import (
    MessagingClient,
    enqueue_message_for_processing,
    get_messaging_client,
    send_text_message,
)
from .models import Config, Message, Response
from .providers import get_provider
from .utils.files import (
    create_file_content,
    download_file,
    encode_file_base64,
    get_file_info,
    get_file_type,
    is_file_message,
)
from .utils.tools import execute_tools, format_tool_results, init_tools

logger = logging.getLogger(__name__)


class Agent:
    """
    Base Demiurg AI Agent class.
    
    This provides the foundation for AI agents with:
    - Multi-provider LLM integration
    - Built-in messaging system
    - Conversation management
    - File handling capabilities
    - Tool execution support
    - Message queue to prevent race conditions
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the agent.
        
        Args:
            config: Agent configuration (uses defaults if not provided)
        """
        self.config = config or Config()
        self.agent_id = f"agent_{self.config.name.lower().replace(' ', '_')}"
        
        # Set up system prompt
        self.system_prompt = self.config.system_prompt or self._get_default_system_prompt()
        
        # Initialize messaging
        self._init_messaging()
        
        # Initialize file handling
        self.file_cache_dir = Path(tempfile.gettempdir()) / "demiurg_agent_files"
        self.file_cache_dir.mkdir(exist_ok=True)
        
        # Initialize tools
        self.tools = []
        self.tool_provider = None
        self._init_tools()
        
        # Initialize provider
        self._init_provider()
        
        logger.info(f"Initialized {self.config.name} v{self.config.version}")
        logger.info(f"Provider: {self.config.provider}")
        logger.info(f"Tools: {len(self.tools)} available")
    
    def _get_default_system_prompt(self) -> str:
        """Get the default system prompt for the agent."""
        return f"""You are {self.config.name}, a helpful AI assistant.

{self.config.description}

You should:
- Be helpful, polite, and professional
- Provide accurate and relevant information
- Ask for clarification when needed
- Use available tools when appropriate

File handling capabilities:
- You CAN view and analyze images (PNG, JPEG, WEBP, GIF)
- You CAN transcribe audio files (MP3, WAV, etc.)
- You CAN read text files (TXT, JSON, XML, etc.)
- You CANNOT analyze PDF content yet (you'll receive a notification when PDFs are sent)
- When you receive an image, describe what you see clearly and accurately

Current date: {datetime.now().strftime("%Y-%m-%d")}"""
    
    def _init_messaging(self):
        """Initialize messaging client."""
        try:
            self.messaging_client = get_messaging_client()
            self.messaging_enabled = True
            logger.info("Messaging client initialized")
        except Exception as e:
            logger.warning(f"Messaging client initialization failed: {e}")
            self.messaging_enabled = False
            self.messaging_client = None
    
    def _init_provider(self):
        """Initialize LLM provider."""
        try:
            self.provider = get_provider(self.config.provider)
            self.provider_available = True
        except Exception as e:
            logger.warning(f"Provider '{self.config.provider}' initialization failed: {e}")
            self.provider = None
            self.provider_available = False
    
    def _init_tools(self):
        """Initialize tools."""
        try:
            # Try to initialize tools with configured provider
            tool_provider_name = os.getenv("TOOL_PROVIDER", "composio")
            self.tools = init_tools(provider=tool_provider_name)
            self.tool_provider = tool_provider_name if self.tools else None
            
            if self.tools:
                logger.info(f"Loaded {len(self.tools)} tools via {tool_provider_name}")
            
        except Exception as e:
            logger.warning(f"Failed to load tools: {e}")
            self.tools = []
            self.tool_provider = None
    
    async def handle_message(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main message handler that queues messages for sequential processing.
        
        Args:
            payload: The incoming message payload
            
        Returns:
            Response dictionary or JSONResponse object
        """
        try:
            # Validate payload first
            message = Message(**payload)
            
            logger.info(f"Received {message.message_type} from {message.user_id} for conversation {message.conversation_id}")
            
            # Enqueue the message for sequential processing
            await enqueue_message_for_processing(
                message.conversation_id,
                self._process_message_internal,
                payload
            )
            
            # Return immediate acknowledgment
            return {
                "status": "queued",
                "message": "Message queued for processing",
                "conversation_id": message.conversation_id,
                "agent_id": self.agent_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error handling message: {str(e)}", exc_info=True)
            
            error_response = {
                "status": "error",
                "message": "Failed to queue message for processing",
                "error": str(e),
                "agent_id": self.agent_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            if JSONResponse:
                return JSONResponse(
                    status_code=500,
                    content=error_response
                )
            else:
                # Return dict if FastAPI not available
                return error_response
    
    async def _process_message_internal(self, payload: Dict[str, Any]) -> None:
        """
        Internal message processing method.
        This processes messages sequentially per conversation to prevent race conditions.
        
        Args:
            payload: The incoming message payload
        """
        start_time = time.time()
        
        try:
            # Validate payload
            message = Message(**payload)
            
            logger.info(f"Processing {message.message_type} from {message.user_id} for conversation {message.conversation_id}")
            
            # Process the message
            if is_file_message(message.message_type, message.metadata):
                response_content = await self.process_file_message(message)
            else:
                response_content = await self.process_message(message)
            
            # Calculate processing time
            processing_time_ms = int((time.time() - start_time) * 1000)
            processing_speed = "fast" if processing_time_ms < 1000 else "normal" if processing_time_ms < 3000 else "slow"
            
            # Create response
            response = Response(
                content=response_content,
                agent_id=self.agent_id,
                conversation_id=message.conversation_id,
                metadata={
                    "processing_time": processing_speed,
                    "processing_time_ms": processing_time_ms,
                    "confidence": 0.9,
                    "agent_version": self.config.version,
                    "messaging_enabled": self.messaging_enabled,
                    "provider": self.config.provider,
                    "model": self.config.model
                }
            )
            
            # Send response if messaging enabled
            if self.messaging_enabled and self.messaging_client:
                await self._send_response(message, response)
            
            logger.info(f"Successfully processed message for conversation {message.conversation_id} in {processing_time_ms}ms")
            
        except Exception as e:
            logger.error(f"Error processing message internally: {str(e)}", exc_info=True)
            
            # Send error response
            try:
                if self.messaging_enabled and self.messaging_client:
                    error_message = "I apologize, but I encountered an error processing your message. Please try again."
                    await send_text_message(
                        message.conversation_id, 
                        error_message,
                        {"error": True, "error_details": str(e)}
                    )
            except Exception as send_error:
                logger.error(f"Failed to send error response: {send_error}")
    
    async def process_message(
        self, 
        message: Message, 
        content: Optional[Union[str, List[Dict[str, Any]]]] = None
    ) -> str:
        """
        Process message using configured LLM provider.
        
        Args:
            message: The message to process
            content: Optional custom content (can be string or content array for multimodal)
            
        Returns:
            Response content
        """
        if not self.provider_available or not self.provider:
            return f"I'm currently unable to process your request as the {self.config.provider} service is unavailable."
        
        try:
            # Get conversation history
            from .messaging import get_conversation_history
            history = await get_conversation_history(
                message.conversation_id, 
                limit=10, 
                provider=self.config.provider
            )
            
            # Build messages list
            messages = []
            
            # Add system prompt
            messages.append({
                "role": "system",
                "content": self.system_prompt
            })
            
            # Add history
            if history:
                messages.extend(history)
            
            # Add current message
            if content is not None:
                messages.append({
                    "role": "user",
                    "content": content
                })
            else:
                messages.append({
                    "role": "user",
                    "content": message.content
                })
            
            # Process with provider
            response = await self.provider.process(
                messages=messages,
                model=self.config.model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                tools=self.tools if self.tools else None
            )
            
            # Check if we need to handle tool calls
            # (This is a simplified version - real implementation would need the full response object)
            # For now, just return the response
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return f"I encountered an error while processing your request: {str(e)}"
    
    async def process_file_message(self, message: Message) -> str:
        """
        Process messages containing files.
        
        Args:
            message: Message with file metadata
            
        Returns:
            Response content
        """
        try:
            file_info = get_file_info(message.metadata)
            if not file_info:
                return "I received a file but couldn't extract its information."
            
            # Download the file
            file_path = await download_file(
                file_info['url'],
                file_info['name'],
                self.file_cache_dir
            )
            
            if not file_path:
                return f"I received your file '{file_info['name']}' but had trouble downloading it."
            
            # Get file type
            file_type = get_file_type(file_info['mime_type'])
            user_text = message.content or "What's in this file?"
            
            # Handle different file types
            if file_type == 'image':
                # For images, create multimodal content
                base64_data, mime_type = encode_file_base64(file_path)
                content = [
                    {"type": "text", "text": user_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_data}"
                        }
                    }
                ]
                
                # Ensure we're using a vision-capable model
                if self.config.provider == "openai" and hasattr(self.provider, 'is_vision_model'):
                    if not self.provider.is_vision_model(self.config.model):
                        # Switch to vision model
                        original_model = self.config.model
                        self.config.model = "gpt-4o-mini"
                        response = await self.process_message(message, content)
                        self.config.model = original_model  # Restore
                        return response
                
            elif file_type == 'audio':
                # Handle audio transcription
                if self.config.provider == "openai" and hasattr(self.provider, 'transcribe_audio'):
                    try:
                        transcription = await self.provider.transcribe_audio(str(file_path))
                        content = f"{user_text}\n\nTranscription of audio file '{file_info['name']}':\n\n{transcription}"
                    except Exception as e:
                        logger.error(f"Error transcribing audio: {e}")
                        content = f"{user_text}\n\n[Audio file '{file_info['name']}' - transcription failed]"
                else:
                    content = f"{user_text}\n\n[Audio file '{file_info['name']}' - transcription not available for {self.config.provider}]"
            
            else:
                # For other file types, create text content
                content = create_file_content(file_path, file_info['mime_type'], user_text)
            
            # Process with LLM
            return await self.process_message(message, content)
            
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            return "I received your file but encountered an error processing it."
    
    async def health_check(self) -> Dict[str, Any]:
        """Get agent health status."""
        return {
            "status": "healthy",
            "agent_name": self.config.name,
            "agent_version": self.config.version,
            "services": {
                "provider": self.provider_available,
                "provider_name": self.config.provider,
                "tools": len(self.tools) > 0,
                "tool_provider": self.tool_provider,
                "messaging": self.messaging_enabled
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def get_queue_status(self) -> Dict[str, Any]:
        """Get status of message queues for debugging."""
        try:
            from .messaging import get_queue_status
            return get_queue_status()
        except Exception as e:
            logger.error(f"Error getting queue status: {e}")
            return {"error": str(e)}
    
    async def _send_response(self, original_message: Message, response: Response):
        """Send response back to conversation."""
        try:
            metadata = {
                "response_type": "agent_response",
                "agent_id": self.agent_id,
            }
            
            if original_message.metadata and "messageId" in original_message.metadata:
                metadata["in_reply_to"] = original_message.metadata["messageId"]
            
            await send_text_message(
                original_message.conversation_id,
                response.content,
                metadata
            )
        except Exception as e:
            logger.error(f"Failed to send response: {e}")


# Add missing import
import os