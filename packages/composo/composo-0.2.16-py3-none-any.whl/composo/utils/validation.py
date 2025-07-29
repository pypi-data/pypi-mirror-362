"""
Input validation utilities
"""

from typing import Any, Optional
from ..exceptions import MalformedError


def validate_api_key(api_key: Optional[str]) -> None:
    """Validate API key format"""
    if not api_key:
        raise MalformedError("API key is required")

    if not isinstance(api_key, str) or len(api_key.strip()) == 0:
        raise MalformedError("API key must be a non-empty string")


def validate_messages(messages: Any) -> None:
    """Validate messages input for correct structure and content"""
    if messages is None:
        raise ValueError("Messages cannot be None")
    if not isinstance(messages, list) or len(messages) == 0:
        raise ValueError("Messages cannot be empty")
    for message in messages:
        if not isinstance(message, dict):
            raise ValueError("Each message must be a dict")
        if "role" not in message:
            raise ValueError("Message must have 'role' field")
        if "content" not in message:
            raise ValueError("Message must have 'content' field")
        if message["role"] not in ["user", "assistant", "system"]:
            raise ValueError("Invalid role in message")
        if not isinstance(message["content"], str):
            raise ValueError("Message content must be a string")
