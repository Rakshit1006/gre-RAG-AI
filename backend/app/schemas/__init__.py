"""Pydantic schemas for request/response validation."""
from app.schemas.word import WordCreate, WordUpdate, WordResponse, MnemonicRequest
from app.schemas.question import QuestionCreate, QuestionResponse
from app.schemas.clip import ClipRequest, ClipResponse
from app.schemas.explain import ExplainRequest, ExplainResponse
from app.schemas.session import SessionStartRequest, SessionResponse
from app.schemas.awa import AWAGradeRequest, AWAGradeResponse

__all__ = [
    "WordCreate", "WordUpdate", "WordResponse", "MnemonicRequest",
    "QuestionCreate", "QuestionResponse",
    "ClipRequest", "ClipResponse",
    "ExplainRequest", "ExplainResponse",
    "SessionStartRequest", "SessionResponse",
    "AWAGradeRequest", "AWAGradeResponse"
]
