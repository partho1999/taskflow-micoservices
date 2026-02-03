import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Gateway Settings
    APP_NAME: str = "Taskflow API Gateway"
    APP_VERSION: str = "1.0.0"
    GATEWAY_PORT: int = int(os.getenv("GATEWAY_PORT", 8080))

    # Microservice URLs (from docker-compose service names)
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8001")
    ORG_SERVICE_URL: str = os.getenv("ORG_SERVICE_URL", "http://organization_service:8002")
    PROJECT_SERVICE_URL: str = os.getenv("PROJECT_SERVICE_URL", "http://project_service:8003")

    # JWT Key (public key will be read from auth service or file)
    JWT_PUBLIC_KEY_PATH: str = os.getenv("JWT_PUBLIC_KEY_PATH", "/app/public_key.pem")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "RS256")

    # Redis Settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))

    # Rate Limiting
    RATE_LIMIT_PER_MIN: int = int(os.getenv("RATE_LIMIT_PER_MIN", 60))

settings = Settings()
