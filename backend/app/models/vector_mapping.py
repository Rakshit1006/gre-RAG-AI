"""Vector mapping model for FAISS index."""
from sqlalchemy import Column, Integer, String
from app.database import Base


class VectorMapping(Base):
    """Maps FAISS vector IDs to object IDs."""
    
    __tablename__ = "vector_mappings"
    
    vector_id = Column(Integer, primary_key=True, autoincrement=True)
    object_id = Column(String, nullable=False, index=True)
    object_type = Column(String, nullable=False)  # word|question
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "vector_id": self.vector_id,
            "object_id": self.object_id,
            "object_type": self.object_type
        }
