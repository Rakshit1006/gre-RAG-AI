"""Mnemonic generation endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.word import MnemonicRequest, MnemonicResponse, WordCreate, WordResponse
from app.services.gemini_client import get_gemini_client
from app.services.vector_store import get_vector_store
from app.prompts.mnemonic import create_mnemonic_prompt
from app.models.word import Word

router = APIRouter(prefix="/api/v1/mnemonic", tags=["mnemonic"])


@router.post("/generate", response_model=MnemonicResponse)
async def generate_mnemonic(
    request: MnemonicRequest,
    db: Session = Depends(get_db)
):
    """Generate mnemonic for a word."""
    try:
        # Get Gemini client
        client = get_gemini_client()
        
        # Create prompt
        prompt = create_mnemonic_prompt(
            word=request.word,
            pos=request.pos,
            style=request.style
        )
        
        # Generate mnemonic
        result = client.generate_json(prompt, temperature=request.temperature)
        
        return MnemonicResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate mnemonic: {str(e)}")


@router.post("/save", response_model=WordResponse)
async def save_mnemonic(
    word_data: WordCreate,
    db: Session = Depends(get_db)
):
    """Save generated mnemonic as a word."""
    try:
        # Check if word already exists
        existing = db.query(Word).filter(Word.word == word_data.word).first()
        if existing:
            raise HTTPException(status_code=400, detail="Word already exists")
        
        # Create word
        word = Word(
            word=word_data.word,
            pos=word_data.pos,
            gre_definition=word_data.gre_definition,
            pithy_definition=word_data.pithy_definition,
            base_word=word_data.base_word,
            associations=word_data.associations,
            examples=word_data.examples,
            easy_synonyms=word_data.easy_synonyms,
            gre_synonyms=word_data.gre_synonyms,
            story=word_data.story,
            tags=word_data.tags,
            source=word_data.source
        )
        
        db.add(word)
        db.commit()
        db.refresh(word)
        
        # Generate and store embedding
        try:
            client = get_gemini_client()
            vector_store = get_vector_store()
            
            # Create text for embedding
            embed_text = f"{word.word} {word.gre_definition or ''} {word.story or ''}"
            embedding = client.generate_embedding(embed_text)
            
            # Add to vector store
            vector_id = vector_store.add_vector(
                embedding,
                word.id,
                "word",
                db
            )
            
            word.embedding_vector_id = vector_id
            db.commit()
            db.refresh(word)
            
        except Exception as e:
            print(f"Warning: Failed to create embedding: {e}")
        
        return WordResponse(**word.to_dict())
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save word: {str(e)}")
