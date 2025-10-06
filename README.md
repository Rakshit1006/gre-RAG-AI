# GRE Mentor

A comprehensive, local-only AI-powered GRE preparation assistant with intelligent mnemonics, spaced repetition, and practice features.

## Features

- 🧠 **AI-Powered Mnemonics** using Google Gemini API
- 📚 **Spaced Repetition System (SRS)** with SM-2 algorithm
- 🔍 **Semantic Search** via FAISS vector store
- ✍️ **AWA Grading** with ETS-aligned rubrics
- 📄 **PDF & Anki Import** for questions and vocabulary
- 🌐 **Browser Extension** to clip content from web pages
- 🔒 **100% Local** - all data stored on your machine

## Quick Start

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
python run.py
```

Backend runs at `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

### 3. Browser Extension (Optional)

1. Open Chrome/Edge: `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `browser-extension` folder

## Usage

1. **Add Words**: Import from Anki/PDF or add manually
2. **Generate Mnemonics**: Auto-generate memorable stories
3. **Practice**: Use flashcards with SRS scheduling
4. **Clip Content**: Use browser extension to save words from web

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests (when implemented)
cd frontend
npm test
```

## Architecture

```
Frontend (React + shadcn) ↔️ Backend (FastAPI) ↔️ Gemini API
                                    ↓
                          FAISS Vector Store
                                    ↓
                            SQLite Database
```

## Documentation

- [Backend README](backend/README.md)
- [Browser Extension README](browser-extension/README.md)

## Security & Privacy

- API keys stored only in local `.env`
- All data stored locally (default: `~/.gre-mentor/`)
- CORS restricted to localhost
- No telemetry or tracking

## License

MIT License
