# GRE Mentor Backend

Local-only FastAPI backend for GRE preparation with AI-powered mnemonics, SRS scheduling, and practice.

## Features

- 🧠 **AI-Powered Mnemonics**: Generate memorable mnemonics using Gemini API
- 📚 **Smart Vocabulary Management**: Store and search words with semantic similarity
- 🔄 **Spaced Repetition (SRS)**: SM-2 algorithm for optimal learning
- 📝 **Practice Sessions**: Flashcards, multiple choice, and typed responses
- ✍️ **AWA Grading**: ETS-aligned essay grading with rubrics
- 📄 **PDF Import**: Extract questions from PDF files
- 📦 **Anki Import**: Import existing Anki decks
- 🔍 **Semantic Search**: FAISS-powered vector search
- 🌐 **Browser Clipper**: Ingest content from web pages

## Quick Start

### Prerequisites

- Python 3.10+
- Gemini API key

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

3. **Run the server:**
```bash
python run.py
```

The API will be available at `http://localhost:8000`

### API Documentation

Interactive API docs available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Mnemonic Generation
- `POST /api/v1/mnemonic/generate` - Generate mnemonic for a word
- `POST /api/v1/mnemonic/save` - Save mnemonic as a word

### Word Management
- `GET /api/v1/words/search` - Search words (semantic + keyword)
- `GET /api/v1/words/{word_id}` - Get specific word
- `PUT /api/v1/words/{word_id}` - Update word
- `DELETE /api/v1/words/{word_id}` - Delete word

### Ingestion
- `POST /api/v1/ingest/clip` - Ingest clipped content from browser

### Explanations
- `POST /api/v1/explain` - Get ETS-aligned explanation

### Practice Sessions
- `POST /api/v1/session/start` - Start practice session
- `POST /api/v1/session/attempt` - Record attempt
- `GET /api/v1/session/stats` - Get statistics
- `POST /api/v1/session/{session_id}/end` - End session

### AWA Grading
- `POST /api/v1/awa/grade` - Grade AWA essay

### Import
- `POST /api/v1/import/pdf` - Import questions from PDF
- `POST /api/v1/import/anki` - Import Anki deck

## Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_mnemonic.py

# Run in verbose mode
pytest -v
```

## Project Structure

```
backend/
├── app/
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── routers/         # API endpoints
│   ├── services/        # Business logic
│   │   ├── gemini_client.py    # Gemini API wrapper
│   │   ├── vector_store.py     # FAISS integration
│   │   └── srs_engine.py       # SRS scheduling
│   ├── prompts/         # LLM prompt templates
│   ├── config.py        # Configuration
│   ├── database.py      # Database setup
│   └── main.py          # FastAPI app
├── tests/               # Test suite
├── requirements.txt     # Dependencies
└── run.py              # Run script
```

## Configuration

Edit `.env` file:

```env
# Gemini API
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-pro
GEMINI_EMBEDDING_MODEL=embedding-001

# Database
DATABASE_URL=sqlite:///./gre_mentor.db
DATA_DIR=~/.gre-mentor

# API
API_HOST=localhost
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# SRS
DEFAULT_NEW_WORDS_PER_DAY=50
DEFAULT_EASE_FACTOR=2.5
```

## Data Storage

All data is stored locally:
- **Database**: SQLite at `./gre_mentor.db`
- **FAISS Index**: `~/.gre-mentor/faiss_index/`
- **No remote backups** by default

## Security

- ✅ API keys stored only in `.env` (never committed)
- ✅ CORS restricted to localhost origins
- ✅ All data stored locally
- ✅ No authentication required (local-only app)

## Development

### Adding New Endpoints

1. Create router in `app/routers/`
2. Define schemas in `app/schemas/`
3. Add business logic in `app/services/`
4. Include router in `app/main.py`
5. Write tests in `tests/`

### Mock Gemini for Testing

Set environment variable:
```bash
export USE_MOCK_GEMINI=true
pytest
```

## Troubleshooting

**FAISS index not loading:**
- Delete `~/.gre-mentor/faiss_index/` to rebuild

**Database errors:**
- Delete `gre_mentor.db` to reset

**Gemini API errors:**
- Check API key in `.env`
- Verify API quota and billing

## License

MIT License - See LICENSE file for details
