import os
import json
import joblib
from datetime import datetime, timedelta
from typing import Tuple, Dict

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from .data import fetch_price_history
from .features import add_technical_features

# Directory to store trained models
MODEL_DIR = os.getenv("MODEL_DIR", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

# Mapping of model name to instantiated classifier
_MODEL_CANDIDATES = {
    "logreg": LogisticRegression(max_iter=500),
    "rf": RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
    "gb": GradientBoostingClassifier(random_state=42),
    # XGBoost and LSTM can be added later via optional toggle
}

def _prepare_dataset(ticker: str) -> pd.DataFrame:
    """Fetch price history and add technical features. The target is next‑day up/down.
    Returns a DataFrame with feature columns and a binary "target" column.
    """
    df = fetch_price_history(ticker, years=5)
    df = add_technical_features(df)
    # Create target: 1 if next day's close > today's close, else 0
    df["target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)
    df = df.dropna(subset=["target"])
    return df

def _chronological_split(df: pd.DataFrame, test_ratio: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split without shuffling, preserving chronological order.
    The most recent *test_ratio* portion becomes the test set.
    """
    cut = int(len(df) * (1 - test_ratio))
    train = df.iloc[:cut]
    test = df.iloc[cut:]
    return train, test

def train_models(ticker: str) -> Dict[str, dict]:
    """Train all candidate models on the given ticker's historical data.
    Returns a dict of evaluation metrics per model.
    The best model (by F1) is saved as ``best_model.pkl``.
    """
    df = _prepare_dataset(ticker)
    X = df.drop(columns=["target", "Close"]).values  # keep features only
    y = df["target"].values

    train_df, test_df = _chronological_split(pd.DataFrame(np.hstack([X, y.reshape(-1, 1)])))
    X_train, y_train = train_df.iloc[:, :-1].values, train_df.iloc[:, -1].values
    X_test, y_test = test_df.iloc[:, :-1].values, test_df.iloc[:, -1].values

    results = {}
    best_f1 = -1
    best_name = None
    for name, model in _MODEL_CANDIDATES.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        probs = model.predict_proba(X_test)[:, 1]
        metrics = {
            "accuracy": accuracy_score(y_test, preds),
            "precision": precision_score(y_test, preds, zero_division=0),
            "recall": recall_score(y_test, preds, zero_division=0),
            "f1": f1_score(y_test, preds, zero_division=0),
            "confusion_matrix": confusion_matrix(y_test, preds).tolist(),
            "feature_importance": (
                model.feature_importances_.tolist() if hasattr(model, "feature_importances_") else None
            ),
        }
        results[name] = metrics
        if metrics["f1"] > best_f1:
            best_f1 = metrics["f1"]
            best_name = name
            # Save best model
            joblib.dump(model, os.path.join(MODEL_DIR, "best_model.pkl"))
    # Also store the evaluation summary
    with open(os.path.join(MODEL_DIR, "evaluation.json"), "w") as f:
        json.dump(results, f, indent=2)
    return {"best_model": best_name, "metrics": results}

def load_best_model():
    path = os.path.join(MODEL_DIR, "best_model.pkl")
    if not os.path.isfile(path):
        raise FileNotFoundError("Best model not trained yet. Call train_models() first.")
    return joblib.load(path)

def predict_next_day(ticker: str) -> float:
    """Return the probability of the next‑day price being higher (P(up)).
    Uses the most recent available data (last row after feature engineering).
    """
    df = fetch_price_history(ticker, years=5)
    df = add_technical_features(df)
    latest = df.iloc[-1]
    X_latest = latest.drop(labels=["Close"]).values.reshape(1, -1)
    model = load_best_model()
    prob_up = model.predict_proba(X_latest)[0, 1]
    return float(prob_up)
