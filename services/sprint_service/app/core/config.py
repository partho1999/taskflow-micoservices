from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # -----------------------------
    # Service Configuration
    # -----------------------------
    SERVICE_NAME: str = "task_service"

    # -----------------------------
    # Database
    # -----------------------------
    DATABASE_URL: str | None = None
    TASK_SERVICE_URL: str | None = None

    # -----------------------------
    # JWT (RS256)
    # -----------------------------
    # KEYS FOLDER IS OUTSIDE APP
    JWT_PUBLIC_KEY_PATH: str = "/keys/public.pem"  
    JWT_AUDIENCE: str = "taskflow"
    JWT_ISSUER: str = "auth_service"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Singleton instance
settings = Settings()
