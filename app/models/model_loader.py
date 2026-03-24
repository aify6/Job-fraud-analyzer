import pickle
import os
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Tuple, Any
from app.core.config import settings

class ModelLoader:
    """Handles loading of ML model and vectorizer."""

    def __init__(self, model_path: str = None, vectorizer_path: str = None):
        self.model_path = model_path or settings.model_path
        self.vectorizer_path = vectorizer_path or settings.vectorizer_path
        self.model = None
        self.vectorizer = None

    def load_model(self) -> Tuple[Any, Any]:
        """Load model and vectorizer. Returns (model, vectorizer)."""
        try:
            with open(self.model_path, "rb") as model_file:
                self.model = pickle.load(model_file)
            with open(self.vectorizer_path, "rb") as vec_file:
                self.vectorizer = pickle.load(vec_file)
        except FileNotFoundError:
            # Fallback: Create dummy model and vectorizer if files not found
            print("Warning: Model files not found, using fallback dummy models")
            self.vectorizer = TfidfVectorizer(stop_words='english')
            self.model = LogisticRegression()

        return self.model, self.vectorizer

    def get_model(self) -> Any:
        """Get the loaded model."""
        if self.model is None:
            self.load_model()
        return self.model

    def get_vectorizer(self) -> Any:
        """Get the loaded vectorizer."""
        if self.vectorizer is None:
            self.load_model()
        return self.vectorizer