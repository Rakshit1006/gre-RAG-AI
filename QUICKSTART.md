# Quick Start Guide

## 1. Get Gemini API Key (Free)

1. Visit https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

## 2. Start Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env and paste your API key
python run.py
```

✅ Backend running at http://localhost:8000

## 3. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

✅ Open http://localhost:5173 in your browser

## 4. Try It Out

1. Go to Import page
2. Type a word like "perspicacious"
3. Click "Add Word"
4. View generated mnemonic
5. Start a practice session

## 5. Optional: Browser Extension

1. Chrome: `chrome://extensions/`
2. Enable Developer mode
3. Load unpacked → select `browser-extension` folder
4. Test by selecting text on any webpage

## Troubleshooting

**Port already in use?**
- Backend: Change `API_PORT` in `.env`
- Frontend: Change port in `vite.config.ts`

**Gemini API not working?**
- Set `USE_MOCK_GEMINI=true` in `.env` for testing

**Need help?**
- Check SETUP.md for detailed instructions
- Review API docs at http://localhost:8000/docs
