from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    POSTGRES_HOST: str = "postgres"
    POSTGRES_DB: str = "academic_helper"
    POSTGRES_USER: str = "student"
    POSTGRES_PASSWORD: str = "secure_password"
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 1440
    N8N_WEBHOOK_URL: str = "http://n8n:5678/webhook/assignment"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
