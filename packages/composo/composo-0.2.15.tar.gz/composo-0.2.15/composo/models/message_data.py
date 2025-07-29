from typing import Literal
from pydantic import BaseModel, Field


class StandardMessageData(BaseModel):
    content: str | None = Field(None, description="The text content of the message")
    role: Literal["user", "assistant", "system", "tool"] = Field(
        ..., description="The message role"
    )
    tool_calls: list | None = Field(
        None, description="List of tool calls (OpenAI function calling)"
    )
    tool_call_id: str | None = Field(
        None, description="Tool call ID (for tool role messages)"
    )
    name: str | None = Field(
        None, description="Name of the function or tool (if applicable)"
    )
