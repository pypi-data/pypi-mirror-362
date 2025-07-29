"""
Type definitions for client parameters
"""

from typing import List, Union, Dict, Any, Optional
from typing_extensions import TypeAlias

# Import the actual types
from openai.types.chat.chat_completion_message_param import (
    ChatCompletionMessageParam,
)
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from openai.types.chat.chat_completion import ChatCompletion

from anthropic.types.message_param import MessageParam
from anthropic.types.tool_union_param import ToolUnionParam
from anthropic.types.message import Message

# Simple dictionary message format (text-based)
SimpleMessage = Dict[str, str]

# Union type for messages - can be OpenAI, Anthropic, or simple dict format
MessageType: TypeAlias = Union[ChatCompletionMessageParam, MessageParam, SimpleMessage]

# Union type for tools - can be OpenAI or Anthropic format
ToolType: TypeAlias = Union[
    ChatCompletionToolParam, ToolUnionParam, Dict[str, Any]  # Generic tool format
]

# Union type for results - can be OpenAI ChatCompletion, Anthropic Message, or any other format
ResultType: TypeAlias = Union[
    ChatCompletion,
    Message,
    Dict[str, Any],  # Generic result format
    str,  # Simple string result
    None,
]

# Type aliases for lists
MessagesType: TypeAlias = List[MessageType]
ToolsType: TypeAlias = Optional[List[ToolType]]
