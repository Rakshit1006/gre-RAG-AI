# Complete Setup Guide

## Prerequisites

1. **Python 3.10+**
2. **Node.js 18+**
3. **Gemini API Key** - Get free at https://makersuite.google.com/app/apikey

## Step-by-Step Setup

### 1. Clone/Download Repository

```bash
cd /Users/rakshitsharma/Downloads/GRE_mentor
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Edit .env and add your Gemini API key
nano .env  # or use your preferred editor
```

Required in `.env`:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Run Backend

```bash
python run.py
```

Server starts at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### 4. Frontend Setup (New Terminal)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend opens at `http://localhost:5173`

### 5. Browser Extension (Optional)

**Chrome/Edge:**
1. Navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top-right)
3. Click "Load unpacked"
4. Select `browser-extension` folder

**Firefox:**
1. Navigate to `about:debugging#/runtime/this-firefox`
2. Click "Load Temporary Add-on"
3. Select `browser-extension/manifest.json`

## Verify Setup

1. Open `http://localhost:5173` in browser
2. You should see the GRE Mentor dashboard
3. Try adding a word via Import page
4. Check that backend is responding at `http://localhost:8000/health`

## Troubleshooting

**Backend won't start:**
- Check Python version: `python --version` (needs 3.10+)
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check if port 8000 is available

**Frontend build errors:**
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check Node version: `node --version` (needs 18+)

**Gemini API errors:**
- Verify API key in `backend/.env`
- Check quota at Google AI Studio
- Test with mock client: Set `USE_MOCK_GEMINI=true` in `.env`

**FAISS errors:**
- Try reinstalling: `pip install --upgrade faiss-cpu`
- Delete index folder: `rm -rf ~/.gre-mentor/faiss_index/`

## Running Tests

**Backend:**
```bash
cd backend
pytest
```

**Frontend:**
```bash
cd frontend
npm test
```

## Data Location

All data stored in: `~/.gre-mentor/`
- Database: `backend/gre_mentor.db`
- FAISS index: `~/.gre-mentor/faiss_index/`

## Next Steps

1. Add your first word via Import page
2. Generate mnemonics automatically
3. Start a practice session
4. Install browser extension to clip content

## Support

- Check API documentation: `http://localhost:8000/docs`
- Review backend logs for errors
- Ensure both backend and frontend are running simultaneously
