import re
import pickle
from typing import List, Dict
import urllib.parse
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
import numpy as np

class JobLegitimacyChecker:
    RED_FLAGS = [
        'no experience needed', 'guaranteed income', 'pay upfront',
        'wire transfer', 'too good to be true', 'urgent hiring',
        'no interview required', 'work from home, earn instantly',
        'easy money', 'no skills required', 'asap', 'immediately',
        'money back guarantee', 'confidential', 'private opportunity'
    ]
    
    SUSPICIOUS_PATTERNS = [
        (r'\$\d+k+.*per.*week', 2),  # Unrealistic salary claims (high severity)
        (r'earn.*\$\d+.*hour', 2),  # Suspicious hourly rate promises (high severity)
        (r'\b(western\s*union|money\s*gram)\b', 2),  # Suspicious payment methods
        (r'need.*bank.*details', 2),  # Requests for sensitive financial info
        (r'instant.*payment', 1),  # Instant payment promise
        (r'no.*investment', 1),  # No investment claim
        (r'(bitcoin|crypto|cryptocurrency)', 2),  # Crypto payment requests
        (r'upfront.*fee', 2),  # Upfront payment required
        (r'limited.*time.*offer', 1)  # Urgency tactic
    ]
    
    VERIFIED_JOB_BOARDS = [
        'linkedin.com/jobs', 'indeed.com', 'glassdoor.com', 'monster.com',
        'ziprecruiter.com', 'dice.com', 'careerbuilder.com', 'google.com/jobs',
        'hired.com', 'angel.co', 'simplyhired.com'
    ]

    def __init__(self, tfidf_path="tfidf_vectorizer.pkl", model_path="model.pkl"):
        try:
            with open(tfidf_path, "rb") as vec_file:
                self.tfidf_vectorizer = pickle.load(vec_file)
            with open(model_path, "rb") as model_file:
                self.model = pickle.load(model_file)
        except FileNotFoundError:
            # Fallback: Create a new vectorizer and train a dummy model if files not found
            self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
            from sklearn.linear_model import LogisticRegression
            self.model = LogisticRegression()

    def validate_url(self, url: str) -> bool:
        try:
            result = urllib.parse.urlparse(url)
            # Check scheme, netloc, and valid TLD
            has_valid_parts = all([result.scheme, result.netloc]) and len(result.netloc) > 3
            # Check for valid TLD (at least one dot in domain)
            has_valid_tld = '.' in result.netloc
            return has_valid_parts and has_valid_tld
        except Exception:
            return False

    def analyze_job_description(self, description: str) -> dict:
        description_lower = description.lower()
        analysis = {
            "red_flag_count": 0, 
            "red_flag_matches": [],
            "suspicious_pattern_count": 0,
            "suspicious_pattern_severity": 0,
            "risk_score": 0
        }
        
        # Check for red flags (whole word matching for accuracy)
        red_flag_matches = []
        for flag in self.RED_FLAGS:
            if re.search(r'\b' + re.escape(flag) + r'\b', description_lower):
                red_flag_matches.append(flag)
        analysis["red_flag_count"] = len(red_flag_matches)
        analysis["red_flag_matches"] = red_flag_matches
        
        # Check for suspicious patterns with severity scoring
        suspicious_severity = 0
        pattern_count = 0
        for pattern, severity in self.SUSPICIOUS_PATTERNS:
            if re.search(pattern, description_lower):
                pattern_count += 1
                suspicious_severity += severity
        analysis["suspicious_pattern_count"] = pattern_count
        analysis["suspicious_pattern_severity"] = suspicious_severity
        
        # Calculate risk score with weighted severity
        analysis["risk_score"] = min((analysis["red_flag_count"] * 15 + 
                                      suspicious_severity * 10), 90)
        
        return analysis

    def verify_job_source(self, job_url: str) -> bool:
        try:
            parsed_url = urllib.parse.urlparse(job_url)
            domain = parsed_url.netloc.lower().replace('www.', '')
            return any(board in domain for board in self.VERIFIED_JOB_BOARDS)
        except Exception:
            return False

    def preprocess_and_predict(self, data: Dict[str, str]) -> int:
        def preprocess_text(text: str) -> str:
            if not text:
                return ""
            text = text.lower()
            text = re.sub(r'\d+', '', text)
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'[^\w\s]', '', text)
            text = [word for word in text.split() if word not in stopwords.words('english')]
            return ' '.join(text)

        # Preprocess and combine text
        preprocessed_data = {key: preprocess_text(value) for key, value in data.items()}
        combined_text = ' '.join(preprocessed_data.values())
        
        # Predict using the ML model
        try:
            tfidf_features = self.tfidf_vectorizer.transform([combined_text])
            prediction = self.model.predict(tfidf_features)
            return prediction[0]
        except Exception:
            # Fallback prediction if model fails
            return 0  # Suspicious
        
