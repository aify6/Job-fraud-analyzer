import os
import re
import json
import logging
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.request import JobAnalysisRequest, JobAnalysisResponse
from app.services.prediction import JobPredictionService
import google.generativeai as genai
from app.core.config import settings

print("DEBUG: Routes module loaded")  # Debug

logger = logging.getLogger(__name__)
router = APIRouter()

def get_prediction_service() -> JobPredictionService:
    """Dependency injection for prediction service."""
    return JobPredictionService()

def setup_generative_ai(api_key: str):
    """Setup Google Generative AI."""
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-pro')
    return model

@router.post("/analyze", response_model=JobAnalysisResponse)
async def analyze_job(
    request: JobAnalysisRequest,
    service: JobPredictionService = Depends(get_prediction_service)
):
    """Analyze a job posting for legitimacy."""
    logger.info(f"Analyzing job: {request.job_title} at {request.company_name}")
    try:
        api_key = settings.gemini_api_key
        logger.debug(f"API key configured: {api_key is not None}")

        # Run technical checks
        url_valid = service.validate_url(request.job_url)
        verified_source = service.verify_job_source(request.job_url)
        desc_analysis = service.analyze_job_description(request.job_description)

        # Prepare ML prediction data
        ml_data = {
            "title": request.job_title,
            "company_profile": request.company_profile or "",
            "description": request.job_description,
            "requirements": request.requirements or "",
            "benefits": request.benefits or "",
        }
        ml_prediction = service.preprocess_and_predict(ml_data)

        # Default fallback response text
        response_text = (
            f"ML Prediction: {'Legitimate' if ml_prediction == 1 else 'Suspicious'}; "
            f"Risk Score: {desc_analysis.get('risk_score', 0)}; "
            f"Red Flags: {', '.join(desc_analysis.get('red_flag_matches', [])) or 'None'}"
        )

        # Optional Gemini analysis if key is available
        if api_key:
            try:
                gemini_model = setup_generative_ai(api_key)
                prompt = f"""Carefully analyze this job posting for legitimacy:\n\nJob Details:\n- Job Title: {request.job_title}\n- Company: {request.company_name}\n- Job URL: {request.job_url}\n\nTechnical Verification:\n- URL Validation: {url_valid}\n- Verified Job Board: {verified_source}\n\nRisk Indicators:\n- Red Flags Detected: {desc_analysis.get('red_flag_count', 0)}\n- Suspicious Patterns: {desc_analysis.get('suspicious_pattern_count', 0)}\n- Calculated Risk Score: {desc_analysis.get('risk_score', 0)}\n\nMachine Learning Prediction: {'Legitimate' if ml_prediction == 1 else 'Suspicious'}\n\nPlease provide a concise JSON with prediction, confidence and explanation."""
                response = gemini_model.generate_content(prompt)
                response_text = response.text
            except Exception as llm_exc:
                logger.warning(f"Gemini LLM analysis failed: {llm_exc}; continuing with fallback")

        # Extract prediction and confidence from response_text
        prediction = 'Legitimate' if ml_prediction == 1 else 'Suspicious'
        confidence = 80 if prediction == 'Legitimate' else 30
        explanation = response_text

        logger.info(
            f"Analysis completed: prediction={prediction}, confidence={confidence}, risk_score={desc_analysis.get('risk_score', 0)}"
        )

        return JobAnalysisResponse(
            prediction=prediction,
            confidence=confidence,
            explanation=explanation,
            risk_score=desc_analysis.get('risk_score', 0),
            red_flags=desc_analysis.get('red_flag_matches', []),
            verified_source=verified_source,
            url_valid=url_valid
        )

    except ValueError as ve:
        logger.error(f"Configuration error: {ve}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(ve))
    except Exception as e:
        logger.error(f"Error analyzing job {request.job_title}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")