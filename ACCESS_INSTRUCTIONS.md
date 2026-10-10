# Access Instructions — Member 1 Medical Misinformation Detection API

## What this project contains
- `app/`: FastAPI application, input/output schemas, model loader, and API-key validation.
- `model/model.pkl`: trained TF-IDF + Logistic Regression pipeline.
- `03_PROCESSED_DATASET/`: bundled training, validation, and test CSV splits.
- `05_API_TESTS/`: API endpoint tests.
- `06_MODEL_TRAINING_SCRIPT.py`: optional retraining script.
- `requirements.txt`: Python dependencies.
- `11_HANDOFF_TO_MEMBER_2.md`: Docker handoff requirements.

This is a text classifier, not a clinical fact-checker. Its output is not medical advice or proof that a claim is true or false.

## Run on Windows using VS Code
1. Extract this ZIP.
2. In VS Code, open the extracted project folder (the folder containing `app`, `model`, and `requirements.txt`).
3. Open **Terminal → New Terminal** and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
$env:API_KEY = (python -c "import secrets; print(secrets.token_urlsafe(32))")
uvicorn app.main:app --reload
```

If PowerShell blocks virtual-environment activation, use this for the current terminal only, then activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

4. Keep the server terminal open. Visit `http://127.0.0.1:8000/docs` for Swagger UI or `http://127.0.0.1:8000/health` for the health endpoint.
5. In Swagger, open `POST /predict`, click **Try it out**, and enter a JSON body such as:

```json
{"text":"Vaccines contain microchips to track your location."}
```

6. Click **Authorize** in Swagger and enter the same API key generated in the terminal. Then execute `POST /predict`.

The key is held in the terminal environment variable `API_KEY`; the request header is `X-API-Key`. Generate a new key for each new terminal/session and use the same value in Swagger. Do not commit real keys to GitHub or bake them into a Docker image.

## Run the tests
With the virtual environment activated, run:

```powershell
pytest -q
```

## Important implementation details
- API entry point: `app.main:app`
- Model path: `model/model.pkl`
- `GET /health` is public.
- `POST /predict` requires a valid `X-API-Key` header.
- The response contains `prediction`, `label`, and `confidence`. Confidence is a model probability, not a guarantee of correctness.
- Retraining is optional. The pre-trained model is included, so the API can run without retraining.
