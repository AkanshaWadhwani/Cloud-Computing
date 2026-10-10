# API Documentation

Base URL locally: `http://127.0.0.1:8000`

## GET /health

Public health endpoint used by humans and cloud health checks.

### Response

```json
{
  "status": "ok",
  "model_loaded": true,
  "model_name": "CoAID TF-IDF + Logistic Regression"
}
```

## POST /predict

Classifies health-related text.

### Authentication

Send the runtime API key in:

```text
X-API-Key: YOUR_API_KEY
```

### Request

```json
{
  "text": "Vaccines contain microchips to track your location."
}
```

### Response

```json
{
  "prediction": "misinformation",
  "label": 1,
  "confidence": 0.75
}
```

`label=0` means accurate; `label=1` means misinformation.

The confidence is the model probability assigned to the predicted class. It is **not** a factuality guarantee.
