"""
Application configuration settings
Loads environment variables and provides app-wide settings
"""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    DATABASE_URL: str
    
    # JWT Authentication
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    
    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 5242880  # 5MB in bytes
    
    # Application
    PROJECT_NAME: str = "AI Resume Matcher"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Email Configuration
    EMAIL_METHOD: str = "gmail"
    GMAIL_USER: str = ""
    GMAIL_APP_PASSWORD: str = ""
    SENDGRID_API_KEY: str = ""
    SENDGRID_FROM_EMAIL: str = ""
    SENDGRID_FROM_NAME: str = "RecruitAI"

    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Create uploads directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)