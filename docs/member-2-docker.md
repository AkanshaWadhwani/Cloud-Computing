# Handoff to Member 2 — Docker

The project root now has a standard Python layout. The API entry point is `app.main:app`; the trained model is `model/model.pkl`; dependencies are in `requirements.txt`.

Run locally before containerizing:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:API_KEY="your-test-key"
uvicorn app.main:app --reload
```

Verify `http://127.0.0.1:8000/health` and `http://127.0.0.1:8000/docs`. `POST /predict` requires `X-API-Key` to match the runtime `API_KEY` environment variable.

Containerization requirements:
- Copy `app/`, `model/`, and `requirements.txt` into the image.
- Expose port 8000 and start with `uvicorn app.main:app --host 0.0.0.0 --port 8000`.
- Supply `API_KEY` at runtime through an environment variable/secret, not a Dockerfile literal.
- Keep `GET /health` public for health checks and `POST /predict` authenticated.
