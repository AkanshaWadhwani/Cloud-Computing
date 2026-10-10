from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000, description="Health-related text to classify")

class PredictResponse(BaseModel):
    prediction: str = Field(..., description="accurate or misinformation")
    label: int = Field(..., description="0 = accurate, 1 = misinformation")
    confidence: float = Field(..., ge=0.0, le=1.0)

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_name: str
