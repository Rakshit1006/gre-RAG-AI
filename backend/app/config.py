"""Configuration management for GRE Mentor backend."""
import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    api_host: str = Field(default="localhost", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        alias="CORS_ORIGINS"
    )
    
    # Gemini API
    gemini_api_key: str = Field(default="", alias="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-pro", alias="GEMINI_MODEL")
    gemini_embedding_model: str = Field(
        default="embedding-001",
        alias="GEMINI_EMBEDDING_MODEL"
    )
    
    # Database
    database_url: str = Field(
        default="sqlite:///./gre_mentor.db",
        alias="DATABASE_URL"
    )
    data_dir: str = Field(default="~/.gre-mentor", alias="DATA_DIR")
    
    # SRS Configuration
    default_new_words_per_day: int = Field(
        default=50,
        alias="DEFAULT_NEW_WORDS_PER_DAY"
    )
    default_ease_factor: float = Field(
        default=2.5,
        alias="DEFAULT_EASE_FACTOR"
    )
    
    # Feature Flags
    enable_voice_commands: bool = Field(
        default=True,
        alias="ENABLE_VOICE_COMMANDS"
    )
    enable_browser_clipper: bool = Field(
        default=True,
        alias="ENABLE_BROWSER_CLIPPER"
    )
    
    # Security
    secret_key: str = Field(
        default="your-secret-key-here-change-in-production",
        alias="SECRET_KEY"
    )
    algorithm: str = Field(default="HS256", alias="ALGORITHM")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def expanded_data_dir(self) -> Path:
        """Expand and return data directory path."""
        return Path(self.data_dir).expanduser()
    
    def ensure_data_dir(self) -> None:
        """Create data directory if it doesn't exist."""
        self.expanded_data_dir.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()
settings.ensure_data_dir()
