"""
Composo SDK - A Python SDK for Composo evaluation services

This package provides both synchronous and asynchronous clients for evaluating
LLM conversations with support for OpenAI and Anthropic formats.
"""

__version__ = "0.1.0"
__author__ = "Composo Team"
__email__ = "support@composo.ai"
__description__ = "A Python SDK for Composo evaluation services"

from .client import Composo, AsyncComposo
from .exceptions import (
    ComposoError,
    RateLimitError,
    MalformedError,
    APIError,
    AuthenticationError,
)
from .validation import validate_raw_chat_conforms_to_type
from .chat_types import OpenAIChatSessionType, AnthropicChatSessionType, ChatSessionType
from .models import CriteriaSet


# Create a criteria module-like object for backward compatibility
class CriteriaModule:
    """Module-like object for accessing predefined criteria sets"""

    @property
    def basic(self):
        return CriteriaSet.basic

    @property
    def rag(self):
        return CriteriaSet.rag


# Create a singleton instance
criteria = CriteriaModule()


# Package exports
__all__ = [
    # Main clients
    "Composo",
    "AsyncComposo",
    # Exceptions
    "ComposoError",
    "RateLimitError",
    "MalformedError",
    "APIError",
    "AuthenticationError",
    # Validation
    "validate_raw_chat_conforms_to_type",
    # Types
    "OpenAIChatSessionType",
    "AnthropicChatSessionType",
    "ChatSessionType",
    # Criteria libraries
    "CriteriaSet",
    "criteria",
    # Metadata
    "__version__",
]


# Welcome message - removed for performance
# print(f"🚀 Composo SDK v{__version__} loaded successfully!")
