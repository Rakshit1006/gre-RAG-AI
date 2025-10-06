"""Tests for mnemonic generation endpoints."""
import pytest
from app.services.gemini_client import get_gemini_client


def test_generate_mnemonic(client, mock_gemini):
    """Test mnemonic generation."""
    response = client.post(
        "/api/v1/mnemonic/generate",
        json={
            "word": "perspicacious",
            "style": "prude",
            "temperature": 0.7
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check required fields
    assert "word" in data
    assert "pos" in data
    assert "gre_definition" in data
    assert "associations" in data
    assert len(data["associations"]) == 5
    assert "examples" in data
    assert len(data["examples"]) == 3
    assert "story" in data


def test_save_mnemonic(client, mock_gemini):
    """Test saving a mnemonic as a word."""
    word_data = {
        "word": "ephemeral",
        "pos": "adjective",
        "gre_definition": "Lasting for a very short time",
        "pithy_definition": "Short-lived",
        "base_word": "ephemeral",
        "associations": ["temporary", "fleeting", "brief", "transient", "momentary"],
        "examples": [
            "The ephemeral nature of fame",
            "An ephemeral beauty",
            "Ephemeral joy"
        ],
        "easy_synonyms": ["temporary", "brief", "short"],
        "gre_synonyms": ["transient", "fleeting", "evanescent"],
        "story": "Think 'e-FEMUR-al' - a femur bone that lasts only briefly before dissolving.",
        "tags": ["vocab", "hard"],
        "source": "test"
    }
    
    response = client.post("/api/v1/mnemonic/save", json=word_data)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["word"] == "ephemeral"
    assert "id" in data
    assert "created_at" in data
    assert "srs" in data


def test_save_duplicate_word(client, mock_gemini):
    """Test that saving a duplicate word returns error."""
    word_data = {
        "word": "test_word",
        "gre_definition": "Test definition",
        "associations": ["a", "b", "c", "d", "e"],
        "examples": ["ex1", "ex2", "ex3"],
        "easy_synonyms": ["s1", "s2", "s3"],
        "gre_synonyms": ["g1", "g2", "g3"]
    }
    
    # First save should succeed
    response1 = client.post("/api/v1/mnemonic/save", json=word_data)
    assert response1.status_code == 200
    
    # Second save should fail
    response2 = client.post("/api/v1/mnemonic/save", json=word_data)
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"]
