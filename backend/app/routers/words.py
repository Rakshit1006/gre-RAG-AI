"""Word management endpoints."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.word import WordResponse, WordUpdate
from app.models.word import Word
from app.services.gemini_client import get_gemini_client
from app.services.vector_store import get_vector_store

router = APIRouter(prefix="/api/v1/words", tags=["words"])


@router.get("/search", response_model=List[WordResponse])
async def search_words(
    q: str = Query(default="", description="Search query"),
    tags: Optional[str] = Query(default=None, description="Comma-separated tags"),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Search words using semantic and keyword search.
    
    If query is provided, uses semantic search via FAISS.
    Can also filter by tags.
    """
    try:
        query = db.query(Word)
        
        # Filter by tags if provided
        if tags:
            tag_list = [t.strip() for t in tags.split(",")]
            # Filter words that have any of the specified tags
            for tag in tag_list:
                query = query.filter(Word.tags.contains([tag]))
        
        # If search query provided, use semantic search
        if q:
            client = get_gemini_client()
            vector_store = get_vector_store()
            
            # Generate query embedding
            query_embedding = client.generate_embedding(q)
            
            # Search in vector store
            results = vector_store.search(
                query_embedding,
                k=limit,
                db=db,
                object_type="word"
            )
            
            # Get word IDs from results
            word_ids = [r[0] for r in results]
            
            if word_ids:
                # Fetch words maintaining order
                words = []
                for word_id in word_ids:
                    word = db.query(Word).filter(Word.id == word_id).first()
                    if word:
                        words.append(word)
                
                return [WordResponse(**w.to_dict()) for w in words]
            else:
                return []
        
        # Otherwise return recent words
        words = query.order_by(Word.created_at.desc()).limit(limit).all()
        return [WordResponse(**w.to_dict()) for w in words]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/{word_id}", response_model=WordResponse)
async def get_word(word_id: str, db: Session = Depends(get_db)):
    """Get a specific word by ID."""
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    return WordResponse(**word.to_dict())


@router.put("/{word_id}", response_model=WordResponse)
async def update_word(
    word_id: str,
    word_update: WordUpdate,
    db: Session = Depends(get_db)
):
    """Update a word."""
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    # Update fields
    update_data = word_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(word, field, value)
    
    db.commit()
    db.refresh(word)
    
    # Update embedding if content changed
    if any(k in update_data for k in ['word', 'gre_definition', 'story']):
        try:
            client = get_gemini_client()
            embed_text = f"{word.word} {word.gre_definition or ''} {word.story or ''}"
            embedding = client.generate_embedding(embed_text)
            
            vector_store = get_vector_store()
            
            # Delete old vector if exists
            if word.embedding_vector_id:
                vector_store.delete_vector(word.embedding_vector_id, db)
            
            # Add new vector
            vector_id = vector_store.add_vector(embedding, word.id, "word", db)
            word.embedding_vector_id = vector_id
            db.commit()
            
        except Exception as e:
            print(f"Warning: Failed to update embedding: {e}")
    
    return WordResponse(**word.to_dict())


@router.delete("/{word_id}")
async def delete_word(word_id: str, db: Session = Depends(get_db)):
    """Delete a word."""
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    # Delete vector if exists
    if word.embedding_vector_id:
        try:
            vector_store = get_vector_store()
            vector_store.delete_vector(word.embedding_vector_id, db)
        except Exception as e:
            print(f"Warning: Failed to delete vector: {e}")
    
    db.delete(word)
    db.commit()
    
    return {"message": "Word deleted successfully"}
