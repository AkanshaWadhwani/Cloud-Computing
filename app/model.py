from pathlib import Path
import joblib

MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "model.pkl"
MODEL_NAME = "CoAID TF-IDF + Logistic Regression"
_model = None

def load_model():
    global _model
    if _model is None:
        if not MODEL_PATH.is_file():
            raise FileNotFoundError(f"Trained model file not found: {MODEL_PATH}")
        _model = joblib.load(MODEL_PATH)
    return _model

def predict(text: str):
    model = load_model()
    label = int(model.predict([text])[0])
    probabilities = model.predict_proba([text])[0]
    confidence = float(probabilities[label])
    prediction = "misinformation" if label == 1 else "accurate"
    return prediction, label, confidence
