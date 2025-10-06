"""Tests for FAISS vector store."""
import pytest
from app.services.vector_store import VectorStore
from app.models.vector_mapping import VectorMapping


def test_add_vector(db):
    """Test adding a vector to the store."""
    store = VectorStore(dimension=768)
    
    # Create a test vector
    vector = [0.1] * 768
    
    # Add vector
    vector_id = store.add_vector(vector, "test-object-1", "word", db)
    
    assert vector_id >= 0
    assert store.index.ntotal == 1
    
    # Check mapping was created
    mapping = db.query(VectorMapping).filter(
        VectorMapping.vector_id == vector_id
    ).first()
    
    assert mapping is not None
    assert mapping.object_id == "test-object-1"
    assert mapping.object_type == "word"


def test_search_vectors(db):
    """Test searching for similar vectors."""
    store = VectorStore(dimension=768)
    
    # Add multiple vectors
    vector1 = [0.1] * 768
    vector2 = [0.2] * 768
    vector3 = [0.9] * 768
    
    store.add_vector(vector1, "obj1", "word", db)
    store.add_vector(vector2, "obj2", "word", db)
    store.add_vector(vector3, "obj3", "question", db)
    
    # Search for similar to vector1
    query = [0.11] * 768
    results = store.search(query, k=2, db=db)
    
    assert len(results) > 0
    # First result should be obj1 (most similar)
    assert results[0][0] == "obj1"


def test_search_with_type_filter(db):
    """Test searching with object type filter."""
    store = VectorStore(dimension=768)
    
    # Add vectors of different types
    vector = [0.1] * 768
    store.add_vector(vector, "word1", "word", db)
    store.add_vector(vector, "question1", "question", db)
    
    # Search only for words
    results = store.search(vector, k=10, db=db, object_type="word")
    
    # All results should be words
    for obj_id, obj_type, dist in results:
        assert obj_type == "word"


def test_delete_vector(db):
    """Test deleting a vector."""
    store = VectorStore(dimension=768)
    
    # Add a vector
    vector = [0.1] * 768
    vector_id = store.add_vector(vector, "to-delete", "word", db)
    
    # Delete it
    store.delete_vector(vector_id, db)
    
    # Check mapping was deleted
    mapping = db.query(VectorMapping).filter(
        VectorMapping.vector_id == vector_id
    ).first()
    
    assert mapping is None
