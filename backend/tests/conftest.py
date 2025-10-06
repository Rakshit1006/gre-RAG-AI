"""Pytest configuration and fixtures."""
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Set environment for testing
os.environ["USE_MOCK_GEMINI"] = "true"
os.environ["DATABASE_URL"] = "sqlite:///./test_gre_mentor.db"

from app.main import app
from app.database import Base, get_db
from app.services.gemini_client import MockGeminiClient, set_gemini_client

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_gre_mentor.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with overridden database."""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def mock_gemini():
    """Create and configure mock Gemini client."""
    mock_client = MockGeminiClient()
    set_gemini_client(mock_client)
    yield mock_client
    # Reset to None after test
    set_gemini_client(None)
