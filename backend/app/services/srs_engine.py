"""Spaced Repetition System (SRS) engine using SM-2 algorithm."""
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from app.models.word import Word
from app.config import settings


class SRSEngine:
    """SM-2 algorithm implementation for spaced repetition."""
    
    def __init__(self, default_ease: float = None):
        """Initialize SRS engine."""
        self.default_ease = default_ease or settings.default_ease_factor
    
    def calculate_next_review(
        self,
        ease: float,
        interval: int,
        repetitions: int,
        quality: int
    ) -> tuple[float, int, int]:
        """
        Calculate next review using SM-2 algorithm.
        
        Args:
            ease: Current ease factor
            interval: Current interval in days
            repetitions: Number of successful repetitions
            quality: Quality of recall (0-5, where 3+ is success)
        
        Returns:
            Tuple of (new_ease, new_interval, new_repetitions)
        """
        # Update ease factor
        new_ease = ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        new_ease = max(1.3, new_ease)  # Minimum ease factor
        
        # Calculate new interval
        if quality < 3:
            # Failed - restart
            new_interval = 1
            new_repetitions = 0
        else:
            # Success
            new_repetitions = repetitions + 1
            
            if new_repetitions == 1:
                new_interval = 1
            elif new_repetitions == 2:
                new_interval = 3
            else:
                new_interval = int(interval * new_ease)
        
        return new_ease, new_interval, new_repetitions
    
    def update_word_srs(
        self,
        word: Word,
        quality: int,
        db: Session
    ) -> Word:
        """
        Update SRS data for a word after review.
        
        Args:
            word: Word to update
            quality: Quality of recall (0-5)
            db: Database session
        
        Returns:
            Updated word
        """
        # Calculate next review
        new_ease, new_interval, new_repetitions = self.calculate_next_review(
            word.srs_ease or self.default_ease,
            word.srs_interval_days or 0,
            word.srs_repetitions or 0,
            quality
        )
        
        # Update word
        word.srs_ease = new_ease
        word.srs_interval_days = new_interval
        word.srs_repetitions = new_repetitions
        word.srs_last_result = quality >= 3
        word.srs_next_due = datetime.utcnow() + timedelta(days=new_interval)
        
        db.commit()
        db.refresh(word)
        
        return word
    
    def get_due_words(
        self,
        db: Session,
        limit: int = 50,
        include_new: bool = True
    ) -> list[Word]:
        """
        Get words due for review.
        
        Args:
            db: Database session
            limit: Maximum number of words to return
            include_new: Whether to include new words (never reviewed)
        
        Returns:
            List of due words
        """
        now = datetime.utcnow()
        query = db.query(Word)
        
        if include_new:
            # Include words with no review date or due date in past
            query = query.filter(
                (Word.srs_next_due == None) | (Word.srs_next_due <= now)
            )
        else:
            # Only words with past due date
            query = query.filter(
                (Word.srs_next_due != None) & (Word.srs_next_due <= now)
            )
        
        # Order by due date (nulls first for new words)
        query = query.order_by(Word.srs_next_due.asc().nullsfirst())
        
        return query.limit(limit).all()
    
    def get_new_words(
        self,
        db: Session,
        limit: int = None
    ) -> list[Word]:
        """
        Get new words (never reviewed).
        
        Args:
            db: Database session
            limit: Maximum number of words to return
        
        Returns:
            List of new words
        """
        limit = limit or settings.default_new_words_per_day
        
        return db.query(Word).filter(
            Word.srs_next_due == None
        ).limit(limit).all()
    
    def get_review_stats(self, db: Session) -> dict:
        """
        Get review statistics.
        
        Returns:
            Dictionary with stats
        """
        now = datetime.utcnow()
        
        total_words = db.query(Word).count()
        new_words = db.query(Word).filter(Word.srs_next_due == None).count()
        due_words = db.query(Word).filter(
            (Word.srs_next_due != None) & (Word.srs_next_due <= now)
        ).count()
        
        return {
            "total_words": total_words,
            "new_words": new_words,
            "due_words": due_words,
            "upcoming_words": total_words - new_words - due_words
        }


# Global SRS engine instance
_srs_engine: Optional[SRSEngine] = None


def get_srs_engine() -> SRSEngine:
    """Get SRS engine instance."""
    global _srs_engine
    if _srs_engine is None:
        _srs_engine = SRSEngine()
    return _srs_engine
