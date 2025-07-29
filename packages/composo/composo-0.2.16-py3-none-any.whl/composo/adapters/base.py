"""
Base adapter interface
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..client.types import MessagesType, ToolsType, ResultType


class FormatAdapter(ABC):
    """Abstract base class for format adapters"""

    @abstractmethod
    def process_result(
        self,
        messages: MessagesType,
        result: ResultType,
        system: Optional[str] = None,
        tools: ToolsType = None,
    ) -> tuple[List[Dict[str, Any]], Optional[str], Optional[List[Dict[str, Any]]]]:
        """
        Process LLM result and append to messages

        Returns:
            tuple: (updated_messages, system_message, tools)
        """
        pass

    @abstractmethod
    def can_handle(self, result: ResultType) -> bool:
        """Check if this adapter can handle the given result type"""
        pass
