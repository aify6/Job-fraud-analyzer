import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings."""

    # API Keys
    gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
    print(f"DEBUG: GEMINI_API_KEY loaded: {gemini_api_key is not None}, value starts with: {gemini_api_key[:10] if gemini_api_key else 'None'}")  # Debug

    # Model paths
    model_path: str = "artifacts/model.pkl"
    vectorizer_path: str = "artifacts/tfidf_vectorizer.pkl"

    # App settings
    app_name: str = "Job Fraud Analyzer"
    version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

# Global settings instance
settings = Settings()