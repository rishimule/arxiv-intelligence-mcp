
import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Base paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    
    # Specific data directories
    PAPERS_DIR: Path = DATA_DIR / "papers"
    VECTOR_DB_DIR: Path = DATA_DIR / "vector_db"
    CACHE_DIR: Path = DATA_DIR / "cache"
    
    # External API Tokens
    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None
    
    # App Config
    USER_AGENT: str = "ArXivIntelligence/0.1.0"
    MAX_SEARCH_RESULTS: int = 5
    
    # Model Config
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2" # Default sentence-transformer
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = Settings()

# Ensure directories exist
os.makedirs(settings.PAPERS_DIR, exist_ok=True)
os.makedirs(settings.VECTOR_DB_DIR, exist_ok=True)
os.makedirs(settings.CACHE_DIR, exist_ok=True)
