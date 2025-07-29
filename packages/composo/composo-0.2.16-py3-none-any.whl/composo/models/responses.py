import math
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException, status


class ScoreResponse(BaseModel):
    """
    Response model for evaluation scores.
    """

    score: Optional[float] = Field(
        None,
        description="Evaluation score between 0 and 1. If null, the criteria was deemed not applicable.",
    )
    explanation: str = Field(description="Explanation of the evaluation score")

    @field_validator("score")
    def validate_score(cls, value):
        if value is None:
            return value
        if math.isnan(value):
            return None
        if not 0 <= value <= 1:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Score must be between 0 and 1.",
            )
        return value


class BinaryEvaluationResponse(BaseModel):
    """
    Response model for binary evaluation results.
    """

    passed: Optional[bool] = Field(
        ...,
        description="Whether the evaluation passed. If null, the criteria was deemed not applicable.",
    )
    explanation: str = Field(None, description="Explanation of the evaluation score")
