"""Browser clipper ingestion endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.clip import ClipRequest, ClipResponse
from app.schemas.word import WordCreate
from app.schemas.question import QuestionCreate
from app.services.gemini_client import get_gemini_client
from app.services.vector_store import get_vector_store
from app.prompts.extraction import create_clip_classifier_prompt, create_extraction_prompt
from app.prompts.mnemonic import create_mnemonic_prompt
from app.models.word import Word
from app.models.question import Question

router = APIRouter(prefix="/api/v1/ingest", tags=["ingest"])


@router.post("/clip", response_model=ClipResponse)
async def ingest_clip(
    request: ClipRequest,
    db: Session = Depends(get_db)
):
    """Ingest clipped content from browser."""
    try:
        client = get_gemini_client()
        
        # Step 1: Classify the content
        classifier_prompt = create_clip_classifier_prompt(request.text, request.hint)
        classification = client.generate_json(classifier_prompt)
        
        content_type = classification.get("type", "concept")
        
        # Step 2: Process based on type
        if content_type == "word" and request.save:
            # Extract or generate mnemonic for word
            # Try to extract word from text
            words = request.text.split()
            target_word = words[0] if words else request.text
            
            # Check if already exists
            existing = db.query(Word).filter(Word.word == target_word).first()
            if existing:
                return ClipResponse(
                    type="word",
                    id=existing.id,
                    preview=existing.to_dict()
                )
            
            # Generate mnemonic
            mnemonic_prompt = create_mnemonic_prompt(target_word)
            mnemonic_data = client.generate_json(mnemonic_prompt)
            
            # Save word
            word = Word(
                word=mnemonic_data.get("word", target_word),
                pos=mnemonic_data.get("pos"),
                gre_definition=mnemonic_data.get("gre_definition"),
                pithy_definition=mnemonic_data.get("pithy_definition"),
                base_word=mnemonic_data.get("base_word"),
                associations=mnemonic_data.get("associations", []),
                examples=mnemonic_data.get("examples", []),
                easy_synonyms=mnemonic_data.get("easy_synonyms", []),
                gre_synonyms=mnemonic_data.get("gre_synonyms", []),
                story=mnemonic_data.get("story"),
                tags=["clipper"],
                source=f"Clipper: {request.url}"
            )
            
            db.add(word)
            db.commit()
            db.refresh(word)
            
            # Generate embedding
            try:
                embed_text = f"{word.word} {word.gre_definition or ''} {word.story or ''}"
                embedding = client.generate_embedding(embed_text)
                vector_store = get_vector_store()
                vector_id = vector_store.add_vector(embedding, word.id, "word", db)
                word.embedding_vector_id = vector_id
                db.commit()
            except Exception as e:
                print(f"Warning: Failed to create embedding: {e}")
            
            return ClipResponse(
                type="word",
                id=word.id,
                preview=word.to_dict()
            )
        
        elif content_type == "question" and request.save:
            # Extract question data
            extraction_prompt = create_extraction_prompt(request.text)
            questions_data = client.generate_json(extraction_prompt)
            
            # Handle both single object and array
            if not isinstance(questions_data, list):
                questions_data = [questions_data]
            
            if questions_data and len(questions_data) > 0:
                q_data = questions_data[0]  # Take first question
                
                question = Question(
                    question_text=q_data.get("question_text", request.text),
                    choices=q_data.get("choices"),
                    answer=q_data.get("answer", ""),
                    explanation=q_data.get("explanation"),
                    source="Clipper",
                    source_url=request.url,
                    concepts=[],
                    difficulty=q_data.get("difficulty", "unknown"),
                    tags=["clipper", q_data.get("detected_type", "unknown")]
                )
                
                db.add(question)
                db.commit()
                db.refresh(question)
                
                # Generate embedding
                try:
                    embed_text = f"{question.question_text} {question.explanation or ''}"
                    embedding = client.generate_embedding(embed_text)
                    vector_store = get_vector_store()
                    vector_id = vector_store.add_vector(embedding, question.id, "question", db)
                    question.embedding_vector_id = vector_id
                    db.commit()
                except Exception as e:
                    print(f"Warning: Failed to create embedding: {e}")
                
                return ClipResponse(
                    type="question",
                    id=question.id,
                    preview=question.to_dict()
                )
        
        # Default: return as concept (not saved)
        return ClipResponse(
            type="concept",
            id="",
            preview={
                "text": request.text,
                "url": request.url,
                "classification": classification
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest clip: {str(e)}")
