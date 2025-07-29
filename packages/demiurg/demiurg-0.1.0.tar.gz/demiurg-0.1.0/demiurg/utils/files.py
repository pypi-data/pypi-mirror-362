"""
File handling utilities for Demiurg agents.
"""

import base64
import logging
import mimetypes
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import httpx

from ..exceptions import FileError

logger = logging.getLogger(__name__)


async def download_file(
    url: str, 
    filename: str, 
    cache_dir: Optional[Path] = None,
    timeout: float = 30.0
) -> Path:
    """
    Download a file from a URL.
    
    Args:
        url: URL to download from
        filename: Name to save the file as
        cache_dir: Directory to save file in (default: temp directory)
        timeout: Request timeout in seconds
        
    Returns:
        Path to downloaded file
        
    Raises:
        FileError: If download fails
    """
    try:
        # Use temp directory if no cache dir specified
        if cache_dir is None:
            cache_dir = Path(tempfile.gettempdir()) / "demiurg_files"
        
        # Ensure cache directory exists
        cache_dir.mkdir(exist_ok=True)
        
        # Download file
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=timeout)
            response.raise_for_status()
            
            # Save file with timestamp prefix to avoid conflicts
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            safe_name = f"{timestamp}_{filename}"
            file_path = cache_dir / safe_name
            
            file_path.write_bytes(response.content)
            logger.info(f"Downloaded file to: {file_path}")
            
            return file_path
            
    except Exception as e:
        logger.error(f"Error downloading file from {url}: {e}")
        raise FileError(f"Failed to download file: {str(e)}")


def get_file_info(metadata: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """
    Extract file information from message metadata.
    
    Args:
        metadata: Message metadata dictionary
        
    Returns:
        Dictionary with 'url', 'name', and 'mime_type' or None
    """
    if not metadata:
        return None
    
    attachments = metadata.get("attachments", [])
    
    if attachments and len(attachments) > 0:
        attachment = attachments[0]
        return {
            "url": attachment.get("filePath") or attachment.get("url"),
            "name": attachment.get("originalName", "file"),
            "mime_type": attachment.get("mimeType", "application/octet-stream")
        }
    
    # Check for legacy fileInfo format
    file_info = metadata.get("fileInfo")
    if file_info:
        return {
            "url": file_info.get("url"),
            "name": file_info.get("name", "file"),
            "mime_type": file_info.get("mimeType", "application/octet-stream")
        }
    
    return None


def encode_file_base64(file_path: Path) -> Tuple[str, str]:
    """
    Read a file and encode it to base64.
    
    Args:
        file_path: Path to file
        
    Returns:
        Tuple of (base64_data, mime_type)
        
    Raises:
        FileError: If file cannot be read
    """
    try:
        # Read file
        file_data = file_path.read_bytes()
        
        # Encode to base64
        base64_data = base64.b64encode(file_data).decode('utf-8')
        
        # Detect MIME type
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if not mime_type:
            mime_type = "application/octet-stream"
        
        return base64_data, mime_type
        
    except Exception as e:
        logger.error(f"Error encoding file {file_path}: {e}")
        raise FileError(f"Failed to encode file: {str(e)}")


def is_file_message(message_type: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
    """
    Check if a message contains files.
    
    Args:
        message_type: Type of message
        metadata: Message metadata
        
    Returns:
        True if message contains files
    """
    if message_type == "file":
        return True
    
    if metadata:
        return bool(metadata.get("attachments") or metadata.get("fileInfo"))
    
    return False


def get_file_type(mime_type: str) -> str:
    """
    Get simplified file type from MIME type.
    
    Args:
        mime_type: MIME type string
        
    Returns:
        Simplified type: 'image', 'audio', 'text', 'pdf', or 'other'
    """
    mime_lower = mime_type.lower()
    
    if mime_lower.startswith('image/'):
        return 'image'
    elif mime_lower.startswith('audio/'):
        return 'audio'
    elif mime_lower.startswith('text/') or mime_lower in ['application/json', 'application/xml']:
        return 'text'
    elif mime_lower == 'application/pdf':
        return 'pdf'
    else:
        return 'other'


def create_file_content(
    file_path: Path,
    mime_type: str,
    user_text: str = "What's in this file?"
) -> str:
    """
    Create appropriate content for different file types.
    
    This is used for non-image files to create text content that describes
    the file for LLM processing.
    
    Args:
        file_path: Path to file
        mime_type: MIME type of file
        user_text: User's message about the file
        
    Returns:
        Formatted content string
    """
    file_type = get_file_type(mime_type)
    filename = file_path.name
    
    if file_type == 'pdf':
        return f"{user_text}\n\n[PDF file '{filename}' received - PDF content analysis is not yet supported]"
    
    elif file_type == 'text':
        try:
            text_content = file_path.read_text('utf-8')
            # Limit text size to avoid token limits
            if len(text_content) > 10000:
                text_content = text_content[:10000] + "\n\n[Content truncated...]"
            return f"{user_text}\n\nContent of '{filename}':\n\n{text_content}"
        except Exception as e:
            logger.error(f"Error reading text file: {e}")
            return f"{user_text}\n\n[Text file '{filename}' - couldn't read content]"
    
    elif file_type == 'audio':
        # Audio transcription should be handled by the provider
        return f"{user_text}\n\n[Audio file '{filename}' - transcription required]"
    
    else:
        return f"{user_text}\n\n[File '{filename}' of type '{mime_type}' - file type not supported for content analysis]"