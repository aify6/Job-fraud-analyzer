# Job Fraud Analyzer API

A FastAPI-based REST API that helps evaluate whether a job posting is legitimate or suspicious. It combines a lightweight rule-based engine, machine learning prediction, and optional LLM aggregation to provide comprehensive job legitimacy analysis.

---

## Features

- **Heuristic Analysis**: Red-flag detection for common scam indicators (upfront payments, vague descriptions, bank details requests, poor grammar)
- **ML Prediction**: Pre-trained model for binary classification of job legitimacy
- **URL Validation**: Domain validation with TLD checking
- **LLM Integration**: Optional Google Gemini AI for natural language explanations
- **RESTful API**: Clean FastAPI endpoints with Pydantic validation
- **Production Ready**: Logging, error handling, health checks, and containerization support

---

## Architecture

```
app/
├── main.py              # FastAPI application entry point
├── api/
│   └── routes.py        # API endpoints
├── services/
│   └── prediction.py    # Business logic service
├── models/
│   └── model_loader.py  # ML model management
├── schemas/
│   └── request.py       # Pydantic models
├── utils/
│   └── preprocessing.py # Text preprocessing utilities
└── core/
    └── config.py        # Application configuration

artifacts/
├── model.pkl            # Trained ML model
└── tfidf_vectorizer.pkl # Text vectorizer
```

---

## API Endpoints

### POST `/api/v1/analyze`
Analyze a job posting for legitimacy.

**Request Body:**
```json
{
  "company_name": "Acme Corporation",
  "job_title": "Software Engineer",
  "job_description": "Detailed job description...",
  "job_url": "https://example.com/job123",
  "company_profile": "Leading tech company",
  "requirements": "Job requirements...",
  "benefits": "Job benefits..."
}
```

**Response:**
```json
{
  "prediction": "Legitimate",
  "confidence": 85,
  "explanation": "Detailed analysis...",
  "risk_score": 15,
  "red_flags": ["guaranteed income"],
  "verified_source": true,
  "url_valid": true
}
```

### GET `/health`
Health check endpoint.

### GET `/`
API information.

---

## Prerequisites

- Python 3.8+
- pip package manager
- (Optional) GEMINI_API_KEY for LLM features

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/aify6/Job-fraud-analyzer.git
cd Job-fraud-analyzer
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
cp .env.example .env
# Edit .env with your GEMINI_API_KEY
```

---

## Running Locally

### Development
```bash
uvicorn app.main:app --reload
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### With Docker
```bash
docker-compose up --build
```

---

## Configuration

Environment variables:

- `GEMINI_API_KEY`: Google Gemini API key (optional)
- `DEBUG`: Enable debug mode (default: false)
- `MODEL_PATH`: Path to ML model (default: artifacts/model.pkl)
- `VECTORIZER_PATH`: Path to vectorizer (default: artifacts/tfidf_vectorizer.pkl)

---

## Testing

Run the test harness:
```bash
python test_improvements.py
```

---

## Deployment

### Docker
```bash
docker build -t job-fraud-analyzer .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key job-fraud-analyzer
```

### Docker Compose
```bash
docker-compose up -d
```

### Cloud Platforms
- **Railway**: Connect GitHub repo, set environment variables
- **Render**: Use Dockerfile, set environment variables
- **Heroku**: Use `uvicorn` command in Procfile

---

## API Documentation

When running locally, visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

---

## Security Notes

- Never commit API keys to the repository
- Use environment variables for sensitive configuration
- The API includes CORS middleware (configure origins for production)
- Input validation via Pydantic models
- Comprehensive error handling and logging

---

## Troubleshooting

- **Model loading errors**: Ensure `artifacts/` directory contains model files
- **API key errors**: Set `GEMINI_API_KEY` environment variable
- **Port conflicts**: Change port with `--port` parameter
- **Import errors**: Ensure all dependencies are installed

---

## License

See LICENSE file for details.
- (Optional) `GEMINI_API_KEY` to use Google Generative AI (Gemini) for natural-language aggregation.

---

## Installation (local)

1. Clone the repository:

```powershell
git clone https://github.com/aify6/Job-fraud-analyzer.git
cd "Job-fraud-analyzer"
```

2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. (Optional) Create a `.env` file or set environment variables for local testing. See the next section for secrets.

---

## Configuration & Secrets

This app can optionally call a generative LLM (Gemini). To enable that, provide your API key via one of these methods:

- Set an environment variable in PowerShell for the current session:

```powershell
$env:GEMINI_API_KEY = 'your_key_here'
```

- Or set it permanently for your user (Windows):

```powershell
setx GEMINI_API_KEY "your_key_here"
```

- When deploying to Streamlit Cloud, add `GEMINI_API_KEY` as a secret in your app settings (do not commit keys to the repo).

The app also supports `python-dotenv` if you prefer a `.env` file locally; add `GEMINI_API_KEY=...` to your `.env` and the app will load it.

Security note: Never commit API keys or private credentials to the repository.

---

## Running the app (local)

```powershell
streamlit run app.py
```

Open the local URL shown by Streamlit (usually `http://localhost:8501`). If `GEMINI_API_KEY` is not set the app will still run — LLM aggregation will be skipped and the heuristic/ML outputs will be used.

---

## How it works (short)

1. Input fields in the UI collect `job_title`, `company_name`, `job_url`, and the job description.
2. `joblegitchecker2.py` examines the description for known red flags and suspicious patterns and computes a `risk_score`.
3. An internal ML component (if model files are present) produces a simple `Legitimate`/`Suspicious` suggestion.
4. Optionally, the app constructs a concise prompt and calls the configured LLM to aggregate findings into a short human-friendly explanation.
5. Deterministic post-processing rules are applied: in cases of clear negative evidence (e.g., `risk_score >= 50` or explicit requests for payment), the app will force `Prediction: Suspicious` and `Confidence: 0%` regardless of LLM output.

---

## Testing

There is a small harness used during development:

```powershell
python test_improvements.py
```

This script runs several sample checks to validate `joblegitchecker2.py` scoring and URL validation.

---

## Deployment (Streamlit Cloud)

1. Push your repo to GitHub.
2. On Streamlit Cloud, create a new app and connect your repository/branch.
3. In the app settings, add `GEMINI_API_KEY` as a secret (if you want LLM-enabled behavior).
4. Provide the start command if needed: `streamlit run app.py`.

Notes:
- Ensure `requirements.txt` lists all runtime packages. Streamlit Cloud will install from it.
- Do not store secrets in the repo.

---

## Troubleshooting

- If the app crashes on startup, check the Python version and that your virtual environment is activated.
- If the LLM call fails, confirm `GEMINI_API_KEY` is set and that the network allows outbound requests.
- If ML model files are missing, the app falls back to heuristics but prints a warning in the logs.

---

## Contributing

Contributions are welcome. Suggested workflow:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feat/your-change`.
3. Make changes and add tests where appropriate.
4. Open a pull request describing the change.

Please avoid committing secrets or large binary model files to the repo.

---

## License

This project includes a `LICENSE` file in the repository root. Check that file for license terms.

---