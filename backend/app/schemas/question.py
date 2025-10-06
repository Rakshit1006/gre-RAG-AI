"""Question schemas for request/response validation."""
from typing import List, Optional
from pydantic import BaseModel, Field


class QuestionBase(BaseModel):
    """Base question schema."""
    question_text: str
    choices: Optional[List[str]] = None
    answer: str
    explanation: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    concepts: List[str] = Field(default_factory=list)
    difficulty: str = Field(default="unknown", pattern="^(low|medium|high|unknown)$")
    tags: List[str] = Field(default_factory=list)


class QuestionCreate(QuestionBase):
    """Schema for creating a question."""
    pass


class QuestionResponse(QuestionBase):
    """Schema for question responses."""
    id: str
    created_at: str
    embedding_vector_id: Optional[int] = None
    
    class Config:
        from_attributes = True


class FlagQuestionRequest(BaseModel):
    """Request schema for flagging a question."""
    question_id: str
    reason: str
