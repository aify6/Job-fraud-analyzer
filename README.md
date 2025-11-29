# Job Fraud Analyzer (JobLegitimacyChecker)

A Streamlit-based utility that helps evaluate whether a job posting is legitimate or suspicious. It combines a lightweight rule-based engine, a small ML prediction fallback, and optional LLM aggregation to give a concise human-friendly verdict and explanation.

This repository contains the Streamlit app (`app.py`), the heuristic/ML analysis module (`joblegitchecker2.py`), and supporting utilities.

---

## Features

- Heuristic red-flag detection (common scam indicators such as upfront payment requests, vague job descriptions, personal bank requests, and poor grammar).
- Suspicious-pattern scoring with severity weights to calculate a numeric `risk_score`.
- URL validation (ensures domain has a valid TLD and basic checks).
- Optional integration with a generative LLM (Gemini) to produce a concise human-readable assessment.
- Deterministic post-processing: clear scam evidence forces `Prediction: Suspicious` and `Confidence: 0%` regardless of LLM output.
- Streamlit UI with a compact, neon-style presentation (app styling in `app.py`).

---

## Quick Demo (expected output format)

The app expects the final LLM output to be plain-text in exactly this format (three lines). When displayed in the UI it looks like:

Prediction: Suspicious
Confidence: 0%
Explanation: Requests upfront payment via bank transfer and uses a free webmail address.

Optional short evidence bullets can follow (each starting with `- `):

- Asks for bank details
- No interview / guaranteed hire language

---

## Repository layout

- `app.py` — Streamlit application and orchestration (builds prompt, calls LLM if configured, applies post-processing, renders UI).
- `joblegitchecker2.py` — Heuristic and ML helper (red flags, suspicious regexes with severity, `risk_score`, `validate_url`).
- `requirements.txt` — Python dependencies (Streamlit, scikit-learn, etc.).
- `model_pkl/` — Optional pre-trained model artifacts (if included).
- `job-fraud-prediction-eda-modeling.ipynb` — Notebook with EDA and modeling experiments.
- `test_improvements.py` — Small test harness used during development.
- `services/` — Utility modules (evidence, rules, core) used by the app.

---

## Prerequisites

- Python 3.8+ (3.10/3.11/3.12 recommended). The project was developed and tested on Windows.
- `pip` or another package manager.
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