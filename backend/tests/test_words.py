"""Tests for word management endpoints."""
import pytest


def test_search_words_empty(client):
    """Test searching with no words in database."""
    response = client.get("/api/v1/words/search?q=test")
    assert response.status_code == 200
    assert response.json() == []


def test_get_word(client, mock_gemini):
    """Test getting a specific word."""
    # First create a word
    word_data = {
        "word": "ubiquitous",
        "gre_definition": "Present everywhere",
        "associations": ["a", "b", "c", "d", "e"],
        "examples": ["ex1", "ex2", "ex3"],
        "easy_synonyms": ["s1", "s2", "s3"],
        "gre_synonyms": ["g1", "g2", "g3"]
    }
    
    create_response = client.post("/api/v1/mnemonic/save", json=word_data)
    word_id = create_response.json()["id"]
    
    # Get the word
    response = client.get(f"/api/v1/words/{word_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["word"] == "ubiquitous"
    assert data["gre_definition"] == "Present everywhere"


def test_get_nonexistent_word(client):
    """Test getting a word that doesn't exist."""
    response = client.get("/api/v1/words/nonexistent-id")
    assert response.status_code == 404


def test_update_word(client, mock_gemini):
    """Test updating a word."""
    # Create a word
    word_data = {
        "word": "original",
        "gre_definition": "Original definition",
        "associations": ["a", "b", "c", "d", "e"],
        "examples": ["ex1", "ex2", "ex3"],
        "easy_synonyms": ["s1", "s2", "s3"],
        "gre_synonyms": ["g1", "g2", "g3"]
    }
    
    create_response = client.post("/api/v1/mnemonic/save", json=word_data)
    word_id = create_response.json()["id"]
    
    # Update the word
    update_data = {
        "gre_definition": "Updated definition",
        "tags": ["updated"]
    }
    
    response = client.put(f"/api/v1/words/{word_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["gre_definition"] == "Updated definition"
    assert "updated" in data["tags"]


def test_delete_word(client, mock_gemini):
    """Test deleting a word."""
    # Create a word
    word_data = {
        "word": "deleteme",
        "associations": ["a", "b", "c", "d", "e"],
        "examples": ["ex1", "ex2", "ex3"],
        "easy_synonyms": ["s1", "s2", "s3"],
        "gre_synonyms": ["g1", "g2", "g3"]
    }
    
    create_response = client.post("/api/v1/mnemonic/save", json=word_data)
    word_id = create_response.json()["id"]
    
    # Delete the word
    response = client.delete(f"/api/v1/words/{word_id}")
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/words/{word_id}")
    assert get_response.status_code == 404
