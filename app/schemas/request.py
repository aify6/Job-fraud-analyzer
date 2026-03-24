from pydantic import BaseModel, Field
from typing import Optional, List

class JobAnalysisRequest(BaseModel):
    """Request model for job analysis."""
    company_name: str = Field(..., description="Name of the company posting the job")
    job_title: str = Field(..., description="Title of the job position")
    job_description: str = Field(..., description="Detailed job description")
    job_url: str = Field(..., description="URL of the job posting")
    company_profile: Optional[str] = Field("", description="Company profile information")
    requirements: Optional[str] = Field("", description="Job requirements")
    benefits: Optional[str] = Field("", description="Job benefits")

class JobAnalysisResponse(BaseModel):
    """Response model for job analysis."""
    prediction: str = Field(..., description="Prediction: Legitimate or Suspicious")
    confidence: int = Field(..., ge=0, le=100, description="Confidence score (0-100%)")
    explanation: str = Field(..., description="Detailed analysis explanation")
    risk_score: int = Field(..., description="Calculated risk score")
    red_flags: List[str] = Field(default_factory=list, description="Detected red flags")
    verified_source: bool = Field(..., description="Whether job is from verified source")
    url_valid: bool = Field(..., description="Whether URL is valid")