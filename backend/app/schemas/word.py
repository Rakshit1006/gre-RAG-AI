"""Word schemas for request/response validation."""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class SRSData(BaseModel):
    """SRS scheduling data."""
    ease: float = Field(default=2.5)
    interval_days: int = Field(default=0)
    next_due: Optional[str] = None
    repetitions: int = Field(default=0)
    last_result: Optional[bool] = None


class WordBase(BaseModel):
    """Base word schema."""
    word: str
    pos: Optional[str] = None
    gre_definition: Optional[str] = None
    pithy_definition: Optional[str] = None
    base_word: Optional[str] = None
    associations: List[str] = Field(default_factory=list)
    examples: List[str] = Field(default_factory=list)
    easy_synonyms: List[str] = Field(default_factory=list)
    gre_synonyms: List[str] = Field(default_factory=list)
    story: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    source: Optional[str] = None


class WordCreate(WordBase):
    """Schema for creating a word."""
    pass


class WordUpdate(BaseModel):
    """Schema for updating a word."""
    word: Optional[str] = None
    pos: Optional[str] = None
    gre_definition: Optional[str] = None
    pithy_definition: Optional[str] = None
    base_word: Optional[str] = None
    associations: Optional[List[str]] = None
    examples: Optional[List[str]] = None
    easy_synonyms: Optional[List[str]] = None
    gre_synonyms: Optional[List[str]] = None
    story: Optional[str] = None
    tags: Optional[List[str]] = None


class WordResponse(WordBase):
    """Schema for word responses."""
    id: str
    created_at: str
    updated_at: str
    embedding_vector_id: Optional[int] = None
    srs: SRSData
    
    class Config:
        from_attributes = True


class MnemonicRequest(BaseModel):
    """Request schema for generating mnemonics."""
    word: str
    pos: Optional[str] = None
    style: str = Field(default="prude", pattern="^(prude|compact|story)$")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class MnemonicResponse(WordBase):
    """Response schema for generated mnemonics."""
    pass
