"""Practice session endpoints."""
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.session import SessionStartRequest, SessionResponse
from app.models.session import Session as SessionModel, Attempt
from app.models.word import Word
from app.models.question import Question
from app.services.srs_engine import get_srs_engine

router = APIRouter(prefix="/api/v1/session", tags=["session"])


@router.post("/start", response_model=SessionResponse)
async def start_session(
    request: SessionStartRequest,
    db: Session = Depends(get_db)
):
    """Start a new practice session."""
    try:
        # Create session
        session = SessionModel(
            mode=request.mode,
            topics=",".join(request.topics)
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        # Get items based on topics
        items = []
        
        if not request.topics or "vocab" in request.topics:
            # Get due words from SRS
            srs_engine = get_srs_engine()
            words = srs_engine.get_due_words(db, limit=request.limit)
            
            for word in words:
                items.append({
                    "type": "word",
                    "id": word.id,
                    "content": word.to_dict()
                })
        
        if not request.topics or any(t in request.topics for t in ["quant", "verbal"]):
            # Get questions
            query = db.query(Question)
            
            if request.topics:
                # Filter by tags
                for topic in request.topics:
                    if topic != "vocab":
                        query = query.filter(Question.tags.contains([topic]))
            
            questions = query.limit(request.limit - len(items)).all()
            
            for question in questions:
                items.append({
                    "type": "question",
                    "id": question.id,
                    "content": question.to_dict()
                })
        
        return SessionResponse(
            session_id=session.id,
            items=items[:request.limit]
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to start session: {str(e)}")


@router.post("/attempt")
async def record_attempt(
    item_id: str,
    item_type: str,
    response: str,
    correct: bool,
    latency_ms: int,
    session_id: str = None,
    db: Session = Depends(get_db)
):
    """Record an attempt for a word or question."""
    try:
        # Create attempt record
        attempt = Attempt(
            session_id=session_id,
            item_id=item_id,
            item_type=item_type,
            response=response,
            correct=correct,
            latency_ms=latency_ms,
            time_ended=datetime.utcnow()
        )
        db.add(attempt)
        db.commit()
        
        # Update SRS if it's a word
        if item_type == "word":
            word = db.query(Word).filter(Word.id == item_id).first()
            if word:
                srs_engine = get_srs_engine()
                # Convert correct to quality score (0-5)
                quality = 4 if correct else 2
                srs_engine.update_word_srs(word, quality, db)
        
        return {"message": "Attempt recorded successfully"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to record attempt: {str(e)}")


@router.get("/stats")
async def get_session_stats(db: Session = Depends(get_db)):
    """Get overall session statistics."""
    try:
        srs_engine = get_srs_engine()
        stats = srs_engine.get_review_stats(db)
        
        # Add attempt statistics
        total_attempts = db.query(Attempt).count()
        correct_attempts = db.query(Attempt).filter(Attempt.correct == True).count()
        
        stats["total_attempts"] = total_attempts
        stats["correct_attempts"] = correct_attempts
        stats["accuracy"] = correct_attempts / total_attempts if total_attempts > 0 else 0
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@router.post("/{session_id}/end")
async def end_session(session_id: str, db: Session = Depends(get_db)):
    """End a practice session."""
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.ended_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Session ended successfully"}
