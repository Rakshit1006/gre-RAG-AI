"""AWA grading schemas."""
from typing import Dict
from pydantic import BaseModel, Field


class AWAGradeRequest(BaseModel):
    """Request schema for AWA grading."""
    essay_text: str
    task_type: str = Field(pattern="^(issue|argument)$")


class RubricScore(BaseModel):
    """Rubric scoring breakdown."""
    thesis: float = Field(ge=0.0, le=2.0)
    development: float = Field(ge=0.0, le=2.0)
    organization: float = Field(ge=0.0, le=1.0)
    language: float = Field(ge=0.0, le=1.0)
    justification: Dict[str, str]


class AWAGradeResponse(BaseModel):
    """Response schema for AWA grading."""
    score: int = Field(ge=0, le=6)
    rubric: RubricScore
    suggested_draft: str
    weaknesses: list[str] = Field(default_factory=list)
    improvements: list[str] = Field(default_factory=list)
