"""Session schemas for practice sessions."""
from typing import List, Dict, Any
from pydantic import BaseModel, Field


class SessionStartRequest(BaseModel):
    """Request schema for starting a practice session."""
    mode: str = Field(pattern="^(flashcard|multichoice|typed)$")
    topics: List[str] = Field(default_factory=list)
    limit: int = Field(default=20, ge=1, le=100)


class SessionResponse(BaseModel):
    """Response schema for session start."""
    session_id: str
    items: List[Dict[str, Any]]
