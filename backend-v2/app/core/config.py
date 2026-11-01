"""
Configuration settings for HintAI V2 using Pydantic Settings.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, HttpUrl
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/hintai_v2",
        env="DATABASE_URL"
    )
    
    # Security
    SECRET_KEY: str = Field(
        default="your-secret-key-here-use-argon2-to-generate",
        env="SECRET_KEY"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Mistral AI
    MISTRAL_API_KEY: str = Field(
        default="your-mistral-api-key-here",
        env="MISTRAL_API_KEY"
    )
    MISTRAL_MODEL: str = "pixtral-12b"
    MISTRAL_EMBEDDING_MODEL: str = "mistral-embed"
    MISTRAL_API_URL: str = "https://api.mistral.ai/v1"
    
    # Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        env="REDIS_URL"
    )
    
    # File Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_FILE_TYPES: List[str] = [".pdf", ".jpg", ".jpeg", ".png"]
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:3001"],
        env="CORS_ORIGINS"
    )
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_MINUTES: int = 1
    
    # Payment
    TMONEY_API_KEY: Optional[str] = None
    TMONEY_API_URL: Optional[str] = None
    MOMO_API_KEY: Optional[str] = None
    MOMO_API_URL: Optional[str] = None
    
    # Sentry
    SENTRY_DSN: Optional[str] = None
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
