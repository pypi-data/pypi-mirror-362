"""
Message handling and processing
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class Message:
    """Represents a chat message"""

    role: str
    content: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None
    name: Optional[str] = None
