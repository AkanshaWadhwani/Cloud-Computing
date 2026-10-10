"""Retrain the TF-IDF + Logistic Regression model from the bundled processed splits.
Run from the extracted project root: python 06_MODEL_TRAINING_SCRIPT.py
The held-out test split is used for evaluation only; final model fits train + validation.
"""
from pathlib import Path
import json
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (accuracy_score, f1_score, precision_score, recall_score,
                             roc_auc_score, classification_report, confusion_matrix)

BASE = Path(__file__).resolve().parent
DATA_DIR = BASE.parent / "data" / "processed"
MODEL_DIR = BASE.parent / "model"
MODEL_DIR.mkdir(exist_ok=True)
train = pd.read_csv(DATA_DIR / "TRAINING_DATA.csv")
val = pd.read_csv(DATA_DIR / "VALIDATION_DATA.csv")
test = pd.read_csv(DATA_DIR / "TEST_DATA.csv")
for name, frame in (("training", train), ("validation", val), ("test", test)):
    if not {"text", "label"}.issubset(frame.columns):
        raise ValueError(f"{name} CSV must contain 'text' and 'label' columns")
    frame["text"] = frame["text"].fillna("").astype(str)
    frame["label"] = frame["label"].astype(int)

def build_model():
    return Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=50000, sublinear_tf=True)),
        ("lr", LogisticRegression(class_weight="balanced", C=1.0, max_iter=2000, random_state=42)),
    ])

# Validate on validation split; evaluate final train+validation model on untouched test split.
validation_model = build_model().fit(train.text, train.label)
validation_predictions = validation_model.predict(val.text)
production = build_model().fit(pd.concat([train, val]).text, pd.concat([train, val]).label)
test_predictions = production.predict(test.text)
test_probabilities = production.predict_proba(test.text)[:, 1]
metrics = {
    "dataset": "Bundled processed CoAID COVID-19 news splits",
    "train_rows": int(len(train)), "validation_rows": int(len(val)), "test_rows": int(len(test)),
    "validation_accuracy": float(accuracy_score(val.label, validation_predictions)),
    "test_accuracy": float(accuracy_score(test.label, test_predictions)),
    "test_macro_f1": float(f1_score(test.label, test_predictions, average="macro")),
    "test_macro_precision": float(precision_score(test.label, test_predictions, average="macro", zero_division=0)),
    "test_macro_recall": float(recall_score(test.label, test_predictions, average="macro", zero_division=0)),
    "test_roc_auc": float(roc_auc_score(test.label, test_probabilities)),
    "classification_report": classification_report(test.label, test_predictions, target_names=["accurate", "misinformation"], output_dict=True, zero_division=0),
    "confusion_matrix": confusion_matrix(test.label, test_predictions).tolist(),
    "text_fields": "preprocessed text column from bundled split CSVs",
    "classifier": "TF-IDF word unigrams+bigrams + balanced LogisticRegression",
    "production_training": "training + validation; test held out for evaluation",
}
joblib.dump(production, MODEL_DIR / "model.pkl", compress=3)
(MODEL_DIR / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
print(json.dumps({k: v for k, v in metrics.items() if not isinstance(v, (dict, list))}, indent=2))
