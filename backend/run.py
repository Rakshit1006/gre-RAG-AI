"""Run script for GRE Mentor backend."""
import uvicorn
from app.config import settings

if __name__ == "__main__":
    print(f"""
    ╔════════════════════════════════════════╗
    ║       GRE Mentor Backend Server        ║
    ╚════════════════════════════════════════╝
    
    Starting server at: http://{settings.api_host}:{settings.api_port}
    API Documentation: http://{settings.api_host}:{settings.api_port}/docs
    
    Press CTRL+C to stop the server
    """)
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level="info"
    )
