from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # MongoDB connection (from environment variables)
    mongodb_username: str
    mongodb_pw: str  
    mongodb_uri: str
    mongodb_database: str = "myCGMitc"
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False
    
    # CORS settings
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()