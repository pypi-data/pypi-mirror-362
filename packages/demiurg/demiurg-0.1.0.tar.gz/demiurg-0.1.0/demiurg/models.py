"""
Data models for Demiurg agents.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class Config(BaseModel):
    """Configuration for an agent."""
    name: str = "Demiurg Agent"
    version: str = "1.0.0"
    description: str = "An AI-powered conversational agent"
    model: str = "gpt-4o-mini"
    provider: str = "openai"  # LLM provider
    temperature: float = 0.7
    max_tokens: int = 1000
    system_prompt: Optional[str] = None


class Message(BaseModel):
    """Structure of messages."""
    content: str = Field(..., min_length=1, max_length=10000)
    user_id: str
    conversation_id: str
    message_type: str = "user_message"
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None


class Response(BaseModel):
    """Structure for agent responses."""
    content: str
    agent_id: str
    conversation_id: str
    response_type: str = "agent_response"
    metadata: Optional[Dict[str, Any]] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def dict(self, **kwargs) -> Dict[str, Any]:
        """Ensure JSON serializable output."""
        data = super().model_dump(**kwargs)
        if isinstance(data.get('timestamp'), datetime):
            data['timestamp'] = data['timestamp'].isoformat()
        return data