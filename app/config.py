"""Application configuration"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "Issue Tracker"
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALLOWED_HOSTS: str = "localhost,127.0.0.1"

    # Database
    DATABASE_URL: str = "sqlite:///./issue_tracker.db"

    # JWT
    JWT_SECRET_KEY: str = "dev-jwt-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
