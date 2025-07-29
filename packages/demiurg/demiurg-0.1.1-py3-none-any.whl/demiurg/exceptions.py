"""
Custom exceptions for Demiurg framework.
"""


class DemiurgError(Exception):
    """Base exception for all Demiurg errors."""
    pass


class ConfigurationError(DemiurgError):
    """Raised when there's a configuration problem."""
    pass


class MessagingError(DemiurgError):
    """Raised when messaging operations fail."""
    pass


class ProviderError(DemiurgError):
    """Raised when LLM provider operations fail."""
    pass


class FileError(DemiurgError):
    """Raised when file operations fail."""
    pass


class ToolError(DemiurgError):
    """Raised when tool execution fails."""
    pass