"""
Type definitions for chat session types
"""

from typing import List, Union
from typing_extensions import TypedDict, Required

# Import the actual types if available, otherwise use generic types
try:
    from openai.types.chat.chat_completion_message_param import (
        ChatCompletionMessageParam,
    )
    from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
except ImportError:
    # Fallback to generic types if OpenAI types are not available
    ChatCompletionMessageParam = dict
    ChatCompletionToolParam = dict

try:
    from anthropic.types.message_param import MessageParam
    from anthropic.types.text_block_param import TextBlockParam
    from anthropic.types.tool_union_param import ToolUnionParam
except ImportError:
    # Fallback to generic types if Anthropic types are not available
    MessageParam = dict
    TextBlockParam = dict
    ToolUnionParam = dict


class OpenAIChatSessionType(TypedDict):
    """Container for OpenAI messages with 'messages' key."""

    messages: Required[List[ChatCompletionMessageParam]]
    tools: List[ChatCompletionToolParam]


class AnthropicChatSessionType(TypedDict, total=False):
    """Container for Anthropic messages with 'messages' key."""

    messages: Required[List[MessageParam]]
    system: Union[str, List[TextBlockParam]]
    tools: List[ToolUnionParam]


# Union type for when you don't know the type of the chat session
ChatSessionType = Union[OpenAIChatSessionType, AnthropicChatSessionType]
