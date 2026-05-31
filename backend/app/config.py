from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Google Gemini
    GEMINI_API_KEY: str
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@postgres:5432/checkitug"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379"
    
    # Twilio (WhatsApp)
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_WHATSAPP_FROM: Optional[str] = None
    
    # Africa's Talking (SMS)
    AT_API_KEY: Optional[str] = None
    AT_USERNAME: Optional[str] = None
    
    # Admin JWT
    JWT_SECRET: str = "your-secret-key-change-this"
    JWT_ALGORITHM: str = "HS256"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "changeme123"
    
    # App
    ENVIRONMENT: str = "development"
    CACHE_TTL: int = 21600  # 6 hours
    
    class Config:
        env_file = ".env"

settings = Settings()