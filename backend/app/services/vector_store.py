"""FAISS vector store implementation."""
import os
import pickle
from pathlib import Path
from typing import List, Tuple, Optional
import numpy as np
import faiss
from sqlalchemy.orm import Session
from app.config import settings
from app.models.vector_mapping import VectorMapping


class VectorStore:
    """FAISS-based vector store for semantic search."""
    
    def __init__(self, dimension: int = 768):
        """Initialize vector store."""
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.index_path = settings.expanded_data_dir / "faiss_index"
        self.index_file = self.index_path / "index.faiss"
        self.metadata_file = self.index_path / "metadata.pkl"
        self.load_index()
    
    def load_index(self):
        """Load existing FAISS index from disk."""
        self.index_path.mkdir(parents=True, exist_ok=True)
        
        if self.index_file.exists():
            try:
                self.index = faiss.read_index(str(self.index_file))
                print(f"Loaded FAISS index with {self.index.ntotal} vectors")
            except Exception as e:
                print(f"Failed to load index: {e}. Creating new index.")
                self.index = faiss.IndexFlatL2(self.dimension)
        else:
            print("No existing index found. Created new index.")
    
    def save_index(self):
        """Save FAISS index to disk."""
        try:
            faiss.write_index(self.index, str(self.index_file))
            print(f"Saved FAISS index with {self.index.ntotal} vectors")
        except Exception as e:
            print(f"Failed to save index: {e}")
    
    def add_vector(
        self, 
        vector: List[float], 
        object_id: str, 
        object_type: str,
        db: Session
    ) -> int:
        """Add a vector to the index and create mapping in DB."""
        # Convert to numpy array and normalize
        vec = np.array([vector], dtype=np.float32)
        
        # Add to FAISS index
        self.index.add(vec)
        vector_id = self.index.ntotal - 1
        
        # Create mapping in database
        mapping = VectorMapping(
            vector_id=vector_id,
            object_id=object_id,
            object_type=object_type
        )
        db.add(mapping)
        db.commit()
        
        # Periodically save index
        if self.index.ntotal % 100 == 0:
            self.save_index()
        
        return vector_id
    
    def search(
        self, 
        query_vector: List[float], 
        k: int = 10,
        db: Session = None,
        object_type: Optional[str] = None
    ) -> List[Tuple[str, str, float]]:
        """
        Search for similar vectors.
        
        Returns:
            List of (object_id, object_type, distance) tuples
        """
        if self.index.ntotal == 0:
            return []
        
        # Convert to numpy array
        query = np.array([query_vector], dtype=np.float32)
        
        # Search in FAISS
        distances, indices = self.index.search(query, min(k, self.index.ntotal))
        
        results = []
        if db:
            for idx, dist in zip(indices[0], distances[0]):
                if idx < 0:  # FAISS returns -1 for missing results
                    continue
                
                # Get mapping from database
                mapping = db.query(VectorMapping).filter(
                    VectorMapping.vector_id == int(idx)
                ).first()
                
                if mapping:
                    # Filter by object type if specified
                    if object_type is None or mapping.object_type == object_type:
                        results.append((
                            mapping.object_id,
                            mapping.object_type,
                            float(dist)
                        ))
        
        return results
    
    def delete_vector(self, vector_id: int, db: Session):
        """
        Delete a vector from the index.
        Note: FAISS doesn't support efficient deletion, so we mark it in DB.
        """
        mapping = db.query(VectorMapping).filter(
            VectorMapping.vector_id == vector_id
        ).first()
        
        if mapping:
            db.delete(mapping)
            db.commit()
    
    def rebuild_index(self, db: Session):
        """Rebuild the entire FAISS index from scratch."""
        # This is needed periodically to remove deleted items
        print("Rebuilding FAISS index...")
        
        # Create new index
        new_index = faiss.IndexFlatL2(self.dimension)
        
        # Get all mappings
        mappings = db.query(VectorMapping).all()
        
        # Note: This is a placeholder - in production, you'd need to 
        # re-fetch embeddings or store them separately
        print(f"Rebuild would process {len(mappings)} vectors")
        
        self.index = new_index
        self.save_index()


# Global vector store instance
_vector_store: Optional[VectorStore] = None


def get_vector_store() -> VectorStore:
    """Get vector store instance."""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store
