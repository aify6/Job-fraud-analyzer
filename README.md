# Job Fraud Analyzer API

A production-ready FastAPI REST API that evaluates job postings for legitimacy using heuristic analysis, machine learning, and optional LLM integration.

## Features

- **Heuristic Analysis**: Red-flag detection (upfront payments, vague descriptions, suspicious phrases)
- **ML Prediction**: Pre-trained model for binary job legitimacy classification
- **URL Validation**: Domain validation with TLD checking
- **Optional LLM**: Google Gemini AI for enhanced analysis
- **RESTful API**: Clean endpoints with Pydantic validation
- **Production Ready**: Logging, error handling, health checks, Docker support

## Quick Start

### Local Development

```bash
# Clone and setup
git clone https://github.com/aify6/Job-fraud-analyzer.git
cd Job-fraud-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment (optional: for Gemini LLM)
cp .env.example .env
# Edit .env with your GEMINI_API_KEY

# Run server
uvicorn app.main:app --reload
```

API available at: `http://localhost:8000`

### Docker

```bash
docker-compose up --build
```

## API Endpoints

### POST `/api/v1/analyze`
Analyze a job posting.

**Request:**
```json
{
  "company_name": "Acme Corp",
  "job_title": "Software Engineer",
  "job_description": "Build secure applications...",
  "job_url": "https://jobs.example.com/123",
  "company_profile": "Tech leader",
  "requirements": "5+ years experience",
  "benefits": "Competitive salary, remote"
}
```

**Response:**
```json
{
  "prediction": "Legitimate",
  "confidence": 85,
  "explanation": "Analysis details...",
  "risk_score": 15,
  "red_flags": [],
  "verified_source": true,
  "url_valid": true
}
```

### GET `/health`
Health check.

### GET `/`
API info.

### GET `/docs`
Interactive Swagger UI (when server running).

## Architecture

```
app/
├── main.py            # FastAPI application
├── api/routes.py      # REST endpoints
├── services/          # Business logic
├── models/            # ML model management
├── schemas/           # Request/response models
├── utils/             # Text preprocessing
└── core/config.py     # Configuration

artifacts/            # ML model files
```

## Configuration

Environment variables:

- `GEMINI_API_KEY`: Google Gemini API key (optional)
- `DEBUG`: Debug mode (default: false)
- `MODEL_PATH`: Path to model (default: artifacts/model.pkl)
- `VECTORIZER_PATH`: Path to vectorizer (default: artifacts/tfidf_vectorizer.pkl)

## Deployment

### Docker
```bash
docker build -t job-fraud-analyzer .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key job-fraud-analyzer
```

### Cloud (Railway, Render, etc.)
1. Connect GitHub repo
2. Set environment variables in platform dashboard
3. Deploy

## Notes

- Model files required in `artifacts/` directory
- API key is optional (local ML fallback works without it)
- Comprehensive logging and error handling built-in
- CORS configured for cross-origin requests

## License

See LICENSE file.

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