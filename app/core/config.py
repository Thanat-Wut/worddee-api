"""
════════════════════════════════════════════════════════════════════
WORDDEE-API - Configuration Settings
════════════════════════════════════════════════════════════════════
"""
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Database
    DATABASE_URL: str
    
    # Security
    ADMIN_API_KEY: str
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"
    
    # External APIs (Optional)
    ENABLE_DICTIONARY_API: bool = False
    DICTIONARY_API_KEY: str = ""
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # App Info
    APP_NAME: str = "Worddee API"
    VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS_ORIGINS string to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

# Singleton instance
settings = Settings()
