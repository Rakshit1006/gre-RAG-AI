"""Session and Attempt models for tracking practice."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Integer
from app.database import Base


class Session(Base):
    """Session table for practice sessions."""
    
    __tablename__ = "sessions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, default="default_user")
    mode = Column(String)  # flashcard|multichoice|typed
    topics = Column(String)  # JSON array as string
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "mode": self.mode,
            "topics": self.topics,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "ended_at": self.ended_at.isoformat() if self.ended_at else None
        }


class Attempt(Base):
    """Attempt table for tracking individual question/word attempts."""
    
    __tablename__ = "attempts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, default="default_user")
    session_id = Column(String, nullable=True)
    item_id = Column(String, nullable=False)
    item_type = Column(String, nullable=False)  # word|question
    
    time_started = Column(DateTime, default=datetime.utcnow)
    time_ended = Column(DateTime, nullable=True)
    response = Column(String, nullable=True)
    correct = Column(Boolean, nullable=True)
    latency_ms = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)
    
    def to_dict(self):
        """Convert to dictionary matching the JSON schema."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "item_id": self.item_id,
            "item_type": self.item_type,
            "time_started": self.time_started.isoformat() if self.time_started else None,
            "time_ended": self.time_ended.isoformat() if self.time_ended else None,
            "response": self.response,
            "correct": self.correct,
            "latency_ms": self.latency_ms,
            "notes": self.notes
        }
