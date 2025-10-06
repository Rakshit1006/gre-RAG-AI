"""Word model for vocabulary items."""
import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, DateTime, Integer, Float, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class Word(Base):
    """Word table for storing vocabulary items with mnemonics and SRS data."""
    
    __tablename__ = "words"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    word = Column(String, nullable=False, index=True, unique=True)
    pos = Column(String)  # Part of speech
    gre_definition = Column(String)
    pithy_definition = Column(String)
    base_word = Column(String)
    
    # JSON arrays
    associations = Column(JSON)  # List of 5 strings
    examples = Column(JSON)  # List of 3 strings
    easy_synonyms = Column(JSON)  # List of 3 strings
    gre_synonyms = Column(JSON)  # List of 3 strings
    
    story = Column(String)  # Mnemonic story
    tags = Column(JSON)  # List of tags
    source = Column(String)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Vector reference
    embedding_vector_id = Column(Integer, nullable=True)
    
    # SRS data
    srs_ease = Column(Float, default=2.5)
    srs_interval_days = Column(Integer, default=0)
    srs_next_due = Column(DateTime, nullable=True)
    srs_repetitions = Column(Integer, default=0)
    srs_last_result = Column(Boolean, nullable=True)
    
    def to_dict(self):
        """Convert to dictionary matching the JSON schema."""
        return {
            "id": self.id,
            "word": self.word,
            "pos": self.pos,
            "gre_definition": self.gre_definition,
            "pithy_definition": self.pithy_definition,
            "base_word": self.base_word,
            "associations": self.associations or [],
            "examples": self.examples or [],
            "easy_synonyms": self.easy_synonyms or [],
            "gre_synonyms": self.gre_synonyms or [],
            "story": self.story,
            "tags": self.tags or [],
            "source": self.source,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "embedding_vector_id": self.embedding_vector_id,
            "srs": {
                "ease": self.srs_ease,
                "interval_days": self.srs_interval_days,
                "next_due": self.srs_next_due.isoformat() if self.srs_next_due else None,
                "repetitions": self.srs_repetitions,
                "last_result": self.srs_last_result
            }
        }
