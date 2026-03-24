import re
import urllib.parse
from typing import Dict, List, Tuple
from app.models.model_loader import ModelLoader
from app.utils.preprocessing import preprocess_job_data

class JobPredictionService:
    """Service for job legitimacy prediction and analysis."""

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

    def __init__(self):
        self.model_loader = ModelLoader()
        self.model = None
        self.vectorizer = None

    def _ensure_model_loaded(self):
        """Ensure model and vectorizer are loaded."""
        if self.model is None or self.vectorizer is None:
            self.model, self.vectorizer = self.model_loader.load_model()

    def validate_url(self, url: str) -> bool:
        """Validate if URL is properly formatted."""
        try:
            result = urllib.parse.urlparse(url)
            # Check scheme, netloc, and valid TLD
            has_valid_parts = all([result.scheme, result.netloc]) and len(result.netloc) > 3
            # Check for valid TLD (at least one dot in domain)
            has_valid_tld = '.' in result.netloc
            return has_valid_parts and has_valid_tld
        except Exception:
            return False

    def analyze_job_description(self, description: str) -> Dict:
        """Analyze job description for red flags and suspicious patterns."""
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
        """Verify if job is posted on a verified job board."""
        try:
            parsed_url = urllib.parse.urlparse(job_url)
            domain = parsed_url.netloc.lower().replace('www.', '')
            return any(board in domain for board in self.VERIFIED_JOB_BOARDS)
        except Exception:
            return False

    def preprocess_and_predict(self, data: Dict[str, str]) -> int:
        """Preprocess job data and make ML prediction."""
        self._ensure_model_loaded()

        # Preprocess and combine text
        combined_text = preprocess_job_data(data)

        # Predict using the ML model
        try:
            tfidf_features = self.vectorizer.transform([combined_text])
            prediction = self.model.predict(tfidf_features)
            return prediction[0]
        except Exception:
            # Fallback prediction if model fails
            return 0  # Suspicious