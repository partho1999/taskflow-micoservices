from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # -----------------------------
    # Service & DB
    # -----------------------------
    SERVICE_NAME: str = "project_service"
    DATABASE_URL: str
    ORG_SERVICE_URL: str

    # -----------------------------
    # JWT (RS256)
    # -----------------------------
    JWT_PUBLIC_KEY_PATH: str = "/app/keys/public.pem"
    JWT_AUDIENCE: str = "taskflow"
    JWT_ISSUER: str = "auth_service"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton instance
settings = Settings()
