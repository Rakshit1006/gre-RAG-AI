"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.routers import mnemonic, words, clip, explain, session, awa, import_routes

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="GRE Mentor API",
    description="Local-only GRE preparation assistant with AI-powered mnemonics, SRS, and practice",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(mnemonic.router)
app.include_router(words.router)
app.include_router(clip.router)
app.include_router(explain.router)
app.include_router(session.router)
app.include_router(awa.router)
app.include_router(import_routes.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "GRE Mentor API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
