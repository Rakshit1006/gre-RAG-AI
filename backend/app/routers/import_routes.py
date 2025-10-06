"""Import endpoints for PDF and Anki files."""
import io
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.gemini_client import get_gemini_client
from app.services.vector_store import get_vector_store
from app.prompts.extraction import create_extraction_prompt
from app.models.question import Question
from app.models.word import Word

router = APIRouter(prefix="/api/v1/import", tags=["import"])


@router.post("/pdf")
async def import_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Import questions from PDF file."""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        import pdfplumber
        
        # Read PDF content
        content = await file.read()
        pdf_file = io.BytesIO(content)
        
        extracted_questions = []
        
        with pdfplumber.open(pdf_file) as pdf:
            text_chunks = []
            
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    # Split into chunks (simple paragraph-based chunking)
                    paragraphs = text.split('\n\n')
                    text_chunks.extend(paragraphs)
        
        # Process chunks to extract questions
        client = get_gemini_client()
        
        for chunk in text_chunks:
            # Skip very short chunks
            if len(chunk.strip()) < 50:
                continue
            
            try:
                # Try to extract questions
                extraction_prompt = create_extraction_prompt(chunk)
                questions_data = client.generate_json(extraction_prompt)
                
                if not isinstance(questions_data, list):
                    questions_data = [questions_data] if questions_data else []
                
                for q_data in questions_data:
                    if q_data.get("question_text"):
                        question = Question(
                            question_text=q_data.get("question_text", ""),
                            choices=q_data.get("choices"),
                            answer=q_data.get("answer", ""),
                            explanation=q_data.get("explanation"),
                            source=f"PDF: {file.filename}",
                            difficulty=q_data.get("difficulty", "unknown"),
                            tags=["pdf_import", q_data.get("detected_type", "unknown")]
                        )
                        
                        db.add(question)
                        extracted_questions.append(question)
                
            except Exception as e:
                print(f"Warning: Failed to extract from chunk: {e}")
                continue
        
        db.commit()
        
        # Generate embeddings for extracted questions
        vector_store = get_vector_store()
        for question in extracted_questions:
            try:
                embed_text = f"{question.question_text} {question.explanation or ''}"
                embedding = client.generate_embedding(embed_text)
                vector_id = vector_store.add_vector(embedding, question.id, "question", db)
                question.embedding_vector_id = vector_id
            except Exception as e:
                print(f"Warning: Failed to create embedding for question: {e}")
        
        db.commit()
        
        return {
            "message": f"Successfully imported {len(extracted_questions)} questions",
            "questions_extracted": len(extracted_questions),
            "chunks_processed": len(text_chunks)
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to import PDF: {str(e)}")


@router.post("/anki")
async def import_anki(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Import Anki deck (.apkg file)."""
    if not file.filename.endswith('.apkg'):
        raise HTTPException(status_code=400, detail="File must be an Anki package (.apkg)")
    
    try:
        # Read file content
        content = await file.read()
        
        # Save temporarily
        import tempfile
        import zipfile
        import sqlite3
        import os
        
        with tempfile.TemporaryDirectory() as tmpdir:
            apkg_path = os.path.join(tmpdir, "deck.apkg")
            
            with open(apkg_path, "wb") as f:
                f.write(content)
            
            # Extract apkg (it's a zip file)
            with zipfile.ZipFile(apkg_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)
            
            # Read collection.anki2 database
            db_path = os.path.join(tmpdir, "collection.anki2")
            
            if not os.path.exists(db_path):
                raise HTTPException(status_code=400, detail="Invalid Anki package")
            
            anki_conn = sqlite3.connect(db_path)
            cursor = anki_conn.cursor()
            
            # Query notes
            cursor.execute("SELECT flds, tags FROM notes")
            notes = cursor.fetchall()
            
            imported_words = []
            client = get_gemini_client()
            vector_store = get_vector_store()
            
            for note in notes:
                fields = note[0].split('\x1f')  # Anki field separator
                tags = note[1].split()
                
                if len(fields) >= 2:
                    # Assume first field is word, second is definition
                    word_text = fields[0].strip()
                    definition = fields[1].strip() if len(fields) > 1 else ""
                    
                    # Check if word already exists
                    existing = db.query(Word).filter(Word.word == word_text).first()
                    if existing:
                        continue
                    
                    # Create word entry
                    word = Word(
                        word=word_text,
                        gre_definition=definition,
                        pithy_definition=definition[:100] if len(definition) > 100 else definition,
                        tags=["anki_import"] + tags,
                        source=f"Anki: {file.filename}"
                    )
                    
                    db.add(word)
                    imported_words.append(word)
            
            db.commit()
            
            # Generate embeddings
            for word in imported_words:
                try:
                    embed_text = f"{word.word} {word.gre_definition or ''}"
                    embedding = client.generate_embedding(embed_text)
                    vector_id = vector_store.add_vector(embedding, word.id, "word", db)
                    word.embedding_vector_id = vector_id
                except Exception as e:
                    print(f"Warning: Failed to create embedding for word: {e}")
            
            db.commit()
            anki_conn.close()
        
        return {
            "message": f"Successfully imported {len(imported_words)} words from Anki deck",
            "words_imported": len(imported_words)
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to import Anki deck: {str(e)}")
