"""Question model for practice questions."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, JSON
from app.database import Base


class Question(Base):
    """Question table for storing practice questions."""
    
    __tablename__ = "questions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    question_text = Column(String, nullable=False)
    choices = Column(JSON, nullable=True)  # List of choices or null
    answer = Column(String)
    explanation = Column(String)
    source = Column(String)
    source_url = Column(String)
    
    concepts = Column(JSON)  # List of concepts
    difficulty = Column(String)  # low|medium|high|unknown
    tags = Column(JSON)  # List of tags
    
    created_at = Column(DateTime, default=datetime.utcnow)
    embedding_vector_id = Column(Integer, nullable=True)
    
    def to_dict(self):
        """Convert to dictionary matching the JSON schema."""
        return {
            "id": self.id,
            "question_text": self.question_text,
            "choices": self.choices,
            "answer": self.answer,
            "explanation": self.explanation,
            "source": self.source,
            "source_url": self.source_url,
            "concepts": self.concepts or [],
            "difficulty": self.difficulty,
            "tags": self.tags or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "embedding_vector_id": self.embedding_vector_id
        }
