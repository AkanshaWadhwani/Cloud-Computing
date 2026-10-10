from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from app.model import MODEL_NAME, load_model, predict
from app.schemas import HealthResponse, PredictRequest, PredictResponse
from app.security import require_api_key

@asynccontextmanager
async def lifespan(_app: FastAPI):
    load_model()
    yield

app = FastAPI(
    lifespan=lifespan,
    title="Medical Misinformation Detection API",
    description="CoAID-trained TF-IDF + Logistic Regression classifier exposed as a REST API.",
    version="1.0.0",
)

@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health():
    try:
        load_model()
        loaded = True
    except Exception:
        loaded = False
    return HealthResponse(status="ok" if loaded else "degraded", model_loaded=loaded, model_name=MODEL_NAME)

@app.post("/predict", response_model=PredictResponse, tags=["Prediction"])
def predict_endpoint(request: PredictRequest, _api_key: str = Depends(require_api_key)):
    prediction, label, confidence = predict(request.text)
    return PredictResponse(prediction=prediction, label=label, confidence=round(confidence, 6))
