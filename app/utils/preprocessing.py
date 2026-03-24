import re
import nltk
from nltk.corpus import stopwords
from typing import Dict

# Download stopwords if not already downloaded
nltk.download('stopwords', quiet=True)

def preprocess_text(text: str) -> str:
    """Preprocess text for ML prediction."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = [word for word in text.split() if word not in stopwords.words('english')]
    return ' '.join(text)

def preprocess_job_data(data: Dict[str, str]) -> str:
    """Preprocess and combine job data for prediction."""
    preprocessed_data = {key: preprocess_text(value) for key, value in data.items()}
    combined_text = ' '.join(preprocessed_data.values())
    return combined_text