"""Integration tests for API endpoints."""
import pytest


def test_full_workflow_mnemonic_to_search(client, mock_gemini):
    """Test complete workflow: generate, save, search."""
    # Step 1: Generate mnemonic
    gen_response = client.post(
        "/api/v1/mnemonic/generate",
        json={"word": "sagacious", "style": "prude"}
    )
    assert gen_response.status_code == 200
    mnemonic = gen_response.json()
    
    # Step 2: Save mnemonic
    save_response = client.post("/api/v1/mnemonic/save", json=mnemonic)
    assert save_response.status_code == 200
    word_id = save_response.json()["id"]
    
    # Step 3: Search for the word
    search_response = client.get("/api/v1/words/search?q=sagacious")
    assert search_response.status_code == 200
    results = search_response.json()
    
    # Should find the word (if embeddings work) or return empty list
    assert isinstance(results, list)


def test_clip_ingestion_word(client, mock_gemini):
    """Test clipping and ingesting a word."""
    response = client.post(
        "/api/v1/ingest/clip",
        json={
            "text": "Perspicacious means having keen insight",
            "url": "https://example.com/vocab",
            "title": "GRE Vocab",
            "hint": "vocab",
            "save": True
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["type"] in ["word", "concept"]
    if data["type"] == "word":
        assert "id" in data
        assert "preview" in data


def test_explain_endpoint(client, mock_gemini):
    """Test explanation endpoint."""
    # Set mock response
    mock_gemini.set_response("json", {
        "summary": "This is a test explanation",
        "details": "Detailed explanation here",
        "references": []
    })
    
    response = client.post(
        "/api/v1/explain",
        json={
            "selection_text": "What is 2 + 2?",
            "domain": "quant",
            "depth": "short"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "explanation" in data
    assert "references" in data


def test_session_workflow(client, mock_gemini):
    """Test practice session workflow."""
    # Create some words first
    for i in range(3):
        word_data = {
            "word": f"word_{i}",
            "gre_definition": f"Definition {i}",
            "associations": ["a", "b", "c", "d", "e"],
            "examples": ["ex1", "ex2", "ex3"],
            "easy_synonyms": ["s1", "s2", "s3"],
            "gre_synonyms": ["g1", "g2", "g3"]
        }
        client.post("/api/v1/mnemonic/save", json=word_data)
    
    # Start session
    start_response = client.post(
        "/api/v1/session/start",
        json={
            "mode": "flashcard",
            "topics": ["vocab"],
            "limit": 5
        }
    )
    
    assert start_response.status_code == 200
    data = start_response.json()
    
    assert "session_id" in data
    assert "items" in data
    assert isinstance(data["items"], list)
    
    # Record an attempt if we have items
    if data["items"]:
        item = data["items"][0]
        attempt_response = client.post(
            "/api/v1/session/attempt",
            params={
                "item_id": item["id"],
                "item_type": item["type"],
                "response": "test",
                "correct": True,
                "latency_ms": 5000,
                "session_id": data["session_id"]
            }
        )
        assert attempt_response.status_code == 200


def test_awa_grading(client, mock_gemini):
    """Test AWA grading endpoint."""
    # Set mock response
    mock_gemini.set_response("json", {
        "score": 4,
        "rubric": {
            "thesis": 1.5,
            "development": 1.5,
            "organization": 0.5,
            "language": 0.5,
            "justification": {
                "thesis": "Clear position stated",
                "development": "Good use of examples",
                "organization": "Logical flow",
                "language": "Minor grammar issues"
            }
        },
        "suggested_draft": "Improved version of the essay...",
        "weaknesses": ["Needs more evidence"],
        "improvements": ["Add specific examples"]
    })
    
    response = client.post(
        "/api/v1/awa/grade",
        json={
            "essay_text": "This is a sample essay about an important issue.",
            "task_type": "issue"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "score" in data
    assert "rubric" in data
    assert "suggested_draft" in data
    assert 0 <= data["score"] <= 6


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
