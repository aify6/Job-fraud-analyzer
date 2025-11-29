import streamlit as st
import google.generativeai as genai
import re
import json
from joblegitchecker2 import JobLegitimacyChecker
import os

# Configure Generative AI
def setup_generative_ai(api_key):
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please set it in Streamlit secrets or .env file.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-pro')
    return model

# Configure page settings
st.set_page_config(
    page_title="Job Legitimacy Checker",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS styling - Neon Cyberpunk Theme
st.markdown("""
    <style>
        body {
            background-color: #0A0A0A;
            color: #E0E0E0;
        }
        
        /* Main container styling */
        .main {
            background-color: #0A0A0A;
        }
        
        /* Neon Title Badge */
        .neon-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #00E5FF;
            text-shadow: 0 0 12px #00E5FF, 0 0 20px #00A8A8;
            margin-bottom: 20px;
            letter-spacing: 2px;
        }
        
        /* Neon Badge - for predictions and labels */
        .neon-badge {
            display: inline-block;
            padding: 12px 24px;
            background: linear-gradient(135deg, #00E5FF, #00FF9C);
            color: #0A0A0A;
            border-radius: 8px;
            font-weight: bold;
            font-size: 1.1rem;
            box-shadow: 0 0 20px #00E5FF, 0 0 40px #00FF9C;
            letter-spacing: 1px;
            margin: 10px 0;
        }
        
        /* Score Bar Container */
        .score-bar {
            width: 100%;
            height: 12px;
            background-color: #1a1a1a;
            border-radius: 6px;
            overflow: hidden;
            margin: 15px 0;
            box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.5);
        }
        
        /* Score Bar Fill - animated gradient */
        .score-fill {
            height: 100%;
            background: linear-gradient(90deg, #00FF9C, #00E5FF);
            border-radius: 6px;
            box-shadow: 0 0 15px #00E5FF, 0 0 25px #00FF9C;
            animation: glow 2s ease-in-out infinite;
            transition: width 0.5s ease-in-out;
        }
        
        @keyframes glow {
            0%, 100% { box-shadow: 0 0 15px #00E5FF, 0 0 25px #00FF9C; }
            50% { box-shadow: 0 0 20px #00E5FF, 0 0 35px #00FF9C; }
        }
        
        /* Section headers */
        .section-header {
            font-size: 1.8rem;
            font-weight: bold;
            color: #00E5FF;
            text-shadow: 0 0 10px #00E5FF;
            margin-top: 25px;
            margin-bottom: 15px;
            letter-spacing: 1px;
        }
        
        /* Confidence Score */
        .confidence-score {
            font-size: 1.4rem;
            font-weight: bold;
            color: #00FF9C;
            text-shadow: 0 0 10px #00FF9C;
            letter-spacing: 1px;
        }
        
        /* Expandable sections */
        .streamlit-expanderHeader {
            background-color: #1a1a1a;
            border: 1px solid #00E5FF;
            border-radius: 6px;
            color: #00E5FF;
            box-shadow: 0 0 10px #00E5FF;
        }
        
        /* Banner image */
        .banner-image {
            width: 100%;
            object-fit: cover;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 0 20px #00E5FF;
        }
        
        /* Footer */
        footer {
            text-align: center;
            padding: 10px;
            font-size: 0.85rem;
            color: #00A8A8;
            text-shadow: 0 0 5px #00E5FF;
        }
        
        /* Responsive text */
        p, span {
            color: #E0E0E0;
        }
    </style>
    """, unsafe_allow_html=True)

# Main functionality
def main(): 
    # Neon Title Banner
    st.markdown('<div class="neon-title">JOB FRAUD ANALYZER </div>', unsafe_allow_html=True)
    st.write("Analyze job postings for legitimacy using AI and data-driven techniques.")
    st.image(r"762887_Job1-01.jpg", caption="Ensure safe job applications!", use_column_width=True)

    with st.sidebar:
        st.header("Input Job Details")
        company_name = st.text_input("Company Name", placeholder="e.g., Acme Corporation")
        job_title = st.text_input("Job Title", placeholder="e.g., Software Engineer")
        job_description = st.text_area("Job Description", placeholder="Paste the job description here...")
        job_url = st.text_input("Job URL", placeholder="e.g., https://example.com/job123")
        company_profile = st.text_input("Company Profile", placeholder="Leading tech company")
        requirements = st.text_area("Job Requirements", placeholder="Enter the job requirements")
        benefits = st.text_area("Job Benefits", placeholder="Enter the job benefits")
        
        analyze_button = st.button("Analyze Job")

    # Main analysis logic
    if analyze_button:
        # Validate inputs
        if not all([company_name, job_title, job_description, job_url]):
            st.warning("Please fill in all required fields.")
            return

        try:
            # Initialize services
            job_verifier = JobLegitimacyChecker()
            
            # Setup Generative AI with validation
            api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
            if not api_key:
                st.error("⚠️ GEMINI_API_KEY not configured. Please set it in Streamlit Secrets or .env file.")
                return
                
            gemini_model = setup_generative_ai(api_key)

            # Run checks
            validate_url = job_verifier.validate_url(job_url)
            desc_analysis = job_verifier.analyze_job_description(job_description)
            in_verified_job_board = job_verifier.verify_job_source(job_url)

            # Prepare ML prediction data
            ml_data = {
                "title": job_title,
                "company_profile": company_profile,
                "description": job_description,
                "requirements": requirements,
                "benefits": benefits,
            }
            ml_prediction = job_verifier.preprocess_and_predict(ml_data)

            # Format red flags for prompt
            red_flags_display = ", ".join(desc_analysis["red_flag_matches"]) if desc_analysis["red_flag_matches"] else "None detected"

            # Comprehensive analysis prompt (original plain-text)
            prompt = f"""Carefully analyze this job posting for legitimacy:

Job Details:
- Job Title: {job_title}
- Company: {company_name}
- Job URL: {job_url}

Technical Verification:
- URL Validation: {validate_url}
- Verified Job Board: {in_verified_job_board}

Risk Indicators:
- Red Flags Detected: {desc_analysis.get('red_flag_count', 0)}
- Suspicious Patterns: {desc_analysis.get('suspicious_pattern_count', 0)}
- Calculated Risk Score: {desc_analysis.get('risk_score', 0)}

Machine Learning Prediction: {'Legitimate' if ml_prediction == 1 else 'Suspicious'}

Comprehensive Analysis Request:
1. Provide a detailed assessment of the job posting's legitimacy.
2. Explain the reasoning behind your assessment.
3. Generate a confidence percentage (0-100%) based on the strength of evidence.
    - If the prediction is LEGITIMATE, the confidence should naturally tend towards a higher percentage (reflecting higher certainty)
    - If the prediction is SUSPICIOUS, the confidence should naturally tend towards a lower percentage (reflecting lower certainty)
4. Highlight specific red flags or positive indicators.
5. Recommend actions for the job seeker.

Output Format:
Prediction: [Legitimate/Suspicious]
Confidence: [XX%]
Explanation: [Your detailed reasoning here]

Your response should be Accurate, Clear, Concise and straight to the point. 
Your tone should be friendly but professional.
"""

            # Generate analysis
            response = gemini_model.generate_content(prompt)
            response_text = response.text
            
            # Try to parse a JSON object from the model response first (preferred)
            confidence = None
            prediction = "Unknown"
            positive_indicators = []
            negative_indicators = []
            explanation = response_text

            # Look for the first JSON object in the response
            json_obj = None
            m = re.search(r"(\{[\s\S]*\})", response_text)
            if m:
                try:
                    json_obj = json.loads(m.group(1))
                except Exception:
                    json_obj = None

            if json_obj:
                # Safely extract fields
                prediction = str(json_obj.get("prediction", "Unknown")).capitalize()
                try:
                    confidence = int(json_obj.get("confidence", 0))
                except Exception:
                    confidence = 0
                positive_indicators = json_obj.get("positive_indicators", []) or []
                negative_indicators = json_obj.get("negative_indicators", []) or []
                explanation = json_obj.get("explanation", explanation)
                # Enforce confidence bounds
                confidence = max(0, min(100, confidence))
                # Enforce critical rule: if Calculated Risk Score >=50 or obvious negatives present, force 0
                obvious_negative_terms = ["pay_upfront","wire_transfer","western_union","money_gram","no_interview","no_experience","guaranteed_income","bank_details","upfront_fee","bitcoin","crypto","send_money"]
                if desc_analysis.get('risk_score', 0) >= 50 or any(term in ",".join(negative_indicators).lower() for term in obvious_negative_terms):
                    confidence = 0
                    prediction = "Suspicious"
            else:
                # Fallback to regex extraction if JSON not provided
                prediction_match = re.search(r'Prediction:\s*(Legitimate|Suspicious)', response_text, re.IGNORECASE)
                confidence_match = re.search(r'Confidence:\s*(\d+)\s*%', response_text, re.IGNORECASE)
                prediction = prediction_match.group(1).capitalize() if prediction_match else "Unknown"
                if confidence_match:
                    confidence = int(confidence_match.group(1))
                    confidence = max(0, min(100, confidence))
                else:
                    # Fallback heuristic: derive confidence from risk_score
                    risk_score = desc_analysis.get('risk_score', 0)
                    if prediction.lower() == "suspicious":
                        confidence = 0 if risk_score >= 50 else max(10, 50 - (risk_score // 2))
                    elif prediction.lower() == "legitimate":
                        # Only increase confidence when there are positive indicators
                        pos = []
                        if in_verified_job_board:
                            pos.append('verified_job_board')
                        if desc_analysis.get('red_flag_count', 0) == 0 and desc_analysis.get('suspicious_pattern_severity', 0) == 0:
                            pos.append('no_flags')
                        confidence = 60 + min(40, len(pos) * 20)
                    else:
                        confidence = 50

            # Ensure final safety bounds
            if confidence is None:
                confidence = 0
            confidence = int(max(0, min(100, confidence)))

            # Display results
            st.markdown('<div class="section-header"> ANALYSIS RESULTS</div>', unsafe_allow_html=True)

            # Prediction visualization with neon badge
            col1, col2 = st.columns(2)
            
            with col1:
                if prediction.lower() == "legitimate":
                    st.success("✅ Job Appears Legitimate")
                    st.markdown(f'<span class="neon-badge">LEGITIMATE — Confidence: {confidence}%</span>', unsafe_allow_html=True)
                    confidence_color = "green"
                elif prediction.lower() == "suspicious":
                    st.warning("⚠️ Potential Job Scam Detected")
                    st.markdown(f'<span class="neon-badge">SUSPICIOUS — Risk: {100-confidence}%</span>', unsafe_allow_html=True)
                    confidence_color = "red"
                else:
                    st.error("⚠️ Unable to determine legitimacy.")
                    st.markdown(f'<span class="neon-badge">UNKNOWN — Confidence: {confidence}%</span>', unsafe_allow_html=True)
                    confidence_color = "gray"

            with col2:
                # Confidence score display
                st.markdown(f'<div class="confidence-score">Confidence Score: {confidence}%</div>', unsafe_allow_html=True)
                
                # Animated score bar
                st.markdown(f"""
                    <div class="score-bar">
                        <div class="score-fill" style="width:{confidence}%;"></div>
                    </div>
                    """, unsafe_allow_html=True)

            # Explanation section with expander
            with st.expander("Detailed Analysis", expanded=True):
                st.markdown('<div class="section-header">Detailed Thoughts</div>', unsafe_allow_html=True)
                st.write(response_text)  # Display the explanation directly

        except ValueError as ve:
            st.error(f"⚠️ Configuration Error: {str(ve)}")
        except Exception as e:
            st.error(f"❌ An error occurred during analysis: {str(e)}")
            with st.expander("Debug Information"):
                st.code(str(e), language="python")

if __name__ == "__main__":
    main()


