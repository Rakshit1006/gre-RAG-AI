"""Tests for SRS engine."""
import pytest
from datetime import datetime, timedelta
from app.services.srs_engine import SRSEngine
from app.models.word import Word


def test_calculate_next_review_success(db):
    """Test SM-2 algorithm with successful review."""
    engine = SRSEngine()
    
    # First review (quality 4)
    ease, interval, reps = engine.calculate_next_review(
        ease=2.5,
        interval=0,
        repetitions=0,
        quality=4
    )
    
    assert reps == 1
    assert interval == 1
    assert ease >= 2.5  # Ease should increase with quality 4


def test_calculate_next_review_failure(db):
    """Test SM-2 algorithm with failed review."""
    engine = SRSEngine()
    
    # Failed review (quality 2)
    ease, interval, reps = engine.calculate_next_review(
        ease=2.5,
        interval=7,
        repetitions=3,
        quality=2
    )
    
    assert reps == 0  # Reset repetitions
    assert interval == 1  # Reset interval
    assert ease < 2.5  # Ease should decrease


def test_update_word_srs(db, mock_gemini):
    """Test updating word SRS data."""
    engine = SRSEngine()
    
    # Create a word
    word = Word(
        word="test",
        associations=["a", "b", "c", "d", "e"],
        examples=["ex1", "ex2", "ex3"],
        easy_synonyms=["s1", "s2", "s3"],
        gre_synonyms=["g1", "g2", "g3"]
    )
    db.add(word)
    db.commit()
    
    # Update SRS with quality 4 (good)
    updated_word = engine.update_word_srs(word, quality=4, db=db)
    
    assert updated_word.srs_repetitions == 1
    assert updated_word.srs_last_result == True
    assert updated_word.srs_next_due is not None


def test_get_due_words(db, mock_gemini):
    """Test getting due words."""
    engine = SRSEngine()
    
    # Create words with different due dates
    word1 = Word(
        word="due_now",
        srs_next_due=datetime.utcnow() - timedelta(days=1),
        associations=["a", "b", "c", "d", "e"],
        examples=["ex1", "ex2", "ex3"],
        easy_synonyms=["s1", "s2", "s3"],
        gre_synonyms=["g1", "g2", "g3"]
    )
    
    word2 = Word(
        word="due_later",
        srs_next_due=datetime.utcnow() + timedelta(days=7),
        associations=["a", "b", "c", "d", "e"],
        examples=["ex1", "ex2", "ex3"],
        easy_synonyms=["s1", "s2", "s3"],
        gre_synonyms=["g1", "g2", "g3"]
    )
    
    word3 = Word(
        word="new_word",
        srs_next_due=None,
        associations=["a", "b", "c", "d", "e"],
        examples=["ex1", "ex2", "ex3"],
        easy_synonyms=["s1", "s2", "s3"],
        gre_synonyms=["g1", "g2", "g3"]
    )
    
    db.add_all([word1, word2, word3])
    db.commit()
    
    # Get due words
    due_words = engine.get_due_words(db, limit=10, include_new=True)
    
    # Should include word1 (past due) and word3 (new)
    due_word_names = [w.word for w in due_words]
    assert "due_now" in due_word_names
    assert "new_word" in due_word_names
    assert "due_later" not in due_word_names


def test_get_review_stats(db, mock_gemini):
    """Test getting review statistics."""
    engine = SRSEngine()
    
    # Create test words
    for i in range(5):
        word = Word(
            word=f"word_{i}",
            srs_next_due=None if i < 2 else datetime.utcnow() - timedelta(days=1),
            associations=["a", "b", "c", "d", "e"],
            examples=["ex1", "ex2", "ex3"],
            easy_synonyms=["s1", "s2", "s3"],
            gre_synonyms=["g1", "g2", "g3"]
        )
        db.add(word)
    
    db.commit()
    
    stats = engine.get_review_stats(db)
    
    assert stats["total_words"] == 5
    assert stats["new_words"] == 2
    assert stats["due_words"] == 3
