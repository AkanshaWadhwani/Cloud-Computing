import os
os.environ["API_KEY"] = "test-secret-key"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_is_public_and_model_loads():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model_loaded"] is True


def test_predict_requires_api_key():
    response = client.post("/predict", json={"text": "COVID vaccines contain microchips."})
    assert response.status_code == 401


def test_predict_rejects_wrong_api_key():
    response = client.post(
        "/predict",
        headers={"X-API-Key": "wrong-key"},
        json={"text": "COVID vaccines contain microchips."},
    )
    assert response.status_code == 401


def test_predict_accepts_correct_api_key():
    response = client.post(
        "/predict",
        headers={"X-API-Key": "test-secret-key"},
        json={"text": "COVID vaccines contain microchips."},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["prediction"] in {"accurate", "misinformation"}
    assert body["label"] in {0, 1}
    assert 0.0 <= body["confidence"] <= 1.0
