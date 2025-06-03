from pydantic_settings import BaseSettings
from typing import Optional
import torch

class Settings(BaseSettings):
    MODEL_NAME: str = "marsyas/gtzan-ft-music-speech-moods-fma-gtzan"  # Music genre classification
    DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: list = [".mp3", ".wav", ".flac", ".m4a"]
    MODEL_CACHE_DIR: Optional[str] = "./model_cache"
    
    # API Configuration
    API_TITLE: str = "HuggingFace Music Inference API"
    API_VERSION: str = "1.0.0"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    
    class Config:
        env_file = ".env"
