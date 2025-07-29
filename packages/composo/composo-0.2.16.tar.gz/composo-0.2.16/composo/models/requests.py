from typing import List
from enum import Enum
from pydantic import BaseModel, Field

from .message_data import StandardMessageData


class ModelCore(str, Enum):
    ALIGN_20250529 = "align-20250529"


class RequestBase(BaseModel):
    messages: List[StandardMessageData] = Field(
        ..., description="A list of chat messages", min_items=2
    )
    model_core: ModelCore = Field(
        default=ModelCore.ALIGN_20250529,
        description="The model core for reward evaluation. Defaults to align-20250503 if not specified.",
    )


class RewardRequest(RequestBase):
    """
    Request model for reward score evaluation of LLM responses against specified criteria.
    """

    evaluation_criteria: str = Field(
        ...,
        description="Criteria used for evaluation. Begins with 'Reward responses' or 'Penalize responses'",
    )


class BinaryEvaluationRequest(RequestBase):
    """
    Request model for binary evaluation of LLM responses against specified criteria.
    """

    evaluation_criteria: str = Field(
        ...,
        description="Criteria used for evaluation. Begins with 'Response passes if' or 'Response fails if'",
    )
