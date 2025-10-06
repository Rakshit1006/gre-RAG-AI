"""Explain schemas for on-the-fly explanations."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Reference(BaseModel):
    """Reference schema."""
    title: str
    url: str


class ExplainRequest(BaseModel):
    """Request schema for explanations."""
    selection_text: str
    domain: str = Field(pattern="^(quant|verbal|vocab|awa)$")
    depth: str = Field(default="short", pattern="^(short|detailed|step-by-step)$")
    save: bool = Field(default=False)


class ExplainResponse(BaseModel):
    """Response schema for explanations."""
    explanation: str
    references: List[Reference] = Field(default_factory=list)
    saved_id: Optional[str] = None
