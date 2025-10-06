"""Clip schemas for browser clipper."""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class ClipRequest(BaseModel):
    """Request schema for ingesting clips."""
    text: str
    url: str
    title: Optional[str] = None
    hint: str = Field(default="auto", pattern="^(auto|vocab|quant|verbal|awa)$")
    save: bool = Field(default=True)


class ClipResponse(BaseModel):
    """Response schema for ingested clips."""
    type: str  # word|question|concept
    id: str
    preview: Dict[str, Any]
