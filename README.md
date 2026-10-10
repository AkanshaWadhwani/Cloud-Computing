# Member 1 — Medical Misinformation Detection API

This is the Member 1 handoff for the team project: a trained text-classification model exposed through FastAPI. It is a **text classifier, not a clinical fact-checker**; predictions must not be treated as medical advice or definitive verification of claims.

## Contents

- `app/`: importable FastAPI application, schemas, model loader and API-key security
- `model/model.pkl`: trained TF-IDF + Logistic Regression pipeline used by the API
- `model/metrics.json`: model evaluation metadata copied from the supplied final package
- `03_PROCESSED_DATASET/`: training, validation and test CSV files
- `06_MODEL_TRAINING_SCRIPT.py`: retraining script that uses the bundled processed splits (no hard-coded local file paths)
- `05_API_TESTS/`: endpoint tests
- `requirements.txt`: Python dependencies
- `08_SAMPLE_API_REQUESTS.json`: sample request payload
- `09_ENVIRONMENT_VARIABLE_TEMPLATE.env`: API key template; it does not contain a real secret
- `11_HANDOFF_TO_MEMBER_2.md`: handoff instructions

## Run on Windows (PowerShell)

From the extracted project root (the folder containing `app`, `model`, and `requirements.txt`):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
$env:API_KEY = (python -c "import secrets; print(secrets.token_urlsafe(32))")
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`. `GET /health` is public. `POST /predict` requires the `X-API-Key` header. In Swagger, click **Authorize** and enter the same value stored in `$env:API_KEY`.

## API contract

### `GET /health`
Returns `status`, `model_loaded`, and `model_name`. No API key required, so deployment health checks can use it.

### `POST /predict`
Header: `X-API-Key: <the API_KEY environment variable>`

Request body:

```json
{
  "text": "Vaccines contain microchips to track your location."
}
```

Response fields: `prediction` (`accurate` or `misinformation`), `label` (`0` or `1`), and `confidence` (0–1). Confidence is the model's predicted-class probability, not a guarantee of correctness.

## Tests

In a second PowerShell terminal, activate the same virtual environment and run:

```powershell
pytest -q
```

The API key in the tests is a test-only value set inside the test module. Never hard-code a real API key in source control.

## Retraining (optional)

```powershell
python 06_MODEL_TRAINING_SCRIPT.py
```

This rewrites `model/model.pkl` and `model/metrics.json` using the bundled training and validation data and evaluates against the held-out test split. The included pre-trained model is already available; retraining is not required to start the API.

## Handoff boundaries

Member 1 provides the model and API. Member 2 can now build a Docker image from this root folder. Preserve `GET /health`, `POST /predict`, `API_KEY`, `X-API-Key`, and port 8000. Member 3 owns CI/CD and Member 4 owns cloud deployment and monitoring. Do not put a real secret in the Dockerfile or repository.
