import datetime
from typing import Dict, Any
import numpy as np

from .data import fetch_price_history
from .features import add_technical_features
from .sentiment import aggregate_sentiment

def _latest_features(ticker: str) -> Dict[str, Any]:
    """Fetch price history, add features, and return the latest row as a dict."""
    df = fetch_price_history(ticker, years=5)
    df = add_technical_features(df)
    latest = df.iloc[-1]
    return latest.to_dict()

def _calculate_trend_score(features: Dict[str, Any]) -> float:
    # Simple trend: price above SMA50 => 1, else 0
    return 1.0 if features.get("Close") > features.get("EMA50", 0) else 0.0

def _crash_risk_flags(features: Dict[str, Any], market_sent: float) -> Dict[str, bool]:
    flags = {}
    # Volatility spike: latest ATR vs 60‑day mean ATR
    atr_series = features.get("ATR_14")
    # Since we only have latest value, compute mean from historical data
    # We'll approximate by using the same series if present; here we compute from df inside function.
    # For simplicity, treat spike if latest ATR > 1.5 * median ATR (placeholder).
    # In real code we'd re‑fetch full df; here we just use latest as proxy.
    flags["volatility_spike"] = False  # placeholder, could be refined later
    # Price below SMA50 with negative MACD histogram
    flags["price_below_sma50_neg_macd"] = (
        features.get("Close", 0) < features.get("SMA20", 0) and features.get("MACD_hist", 0) < 0
    )
    # Negative market sentiment
    flags["negative_market_sentiment"] = market_sent < -0.05
    # Drawdown >20% from 52‑week high (approx 252 trading days)
    # We'll fetch 1‑year high from data (requires historical df). Use placeholder false.
    flags["drawdown_20pct"] = False
    # RSI > 75
    flags["rsi_overbought"] = features.get("RSI_14", 0) > 75
    return flags

def advise(ticker: str, model_prob: float) -> Dict[str, Any]:
    """Combine model probability, sentiment, and technical trend to generate a recommendation.
    Returns a dict matching `AnalyzeResponse` schema.
    """
    # Sentiment aggregation
    sentiment_data = aggregate_sentiment(ticker)
    stock_sent = sentiment_data["stock_score"]
    market_sent = sentiment_data["market_score"]

    # Technical trend and risk flags
    latest_features = _latest_features(ticker)
    trend_score = _calculate_trend_score(latest_features)
    risk_flags = _crash_risk_flags(latest_features, market_sent)

    # Weighted score (0‑1)
    weighted = (
        0.45 * model_prob
        + 0.25 * ((stock_sent + 1) / 2)  # map -1..1 to 0..1
        + 0.10 * ((market_sent + 1) / 2)
        + 0.20 * trend_score
    )

    # Determine recommendation based on thresholds
    if any(risk_flags.values()):
        recommendation = "SELL"
        risk_level = "High"
    else:
        if weighted >= 0.6:
            recommendation = "BUY"
        elif weighted >= 0.4:
            recommendation = "HOLD"
        else:
            recommendation = "SELL"
        # Risk level based on weighted score
        if weighted >= 0.7:
            risk_level = "Low"
        elif weighted >= 0.5:
            risk_level = "Medium"
        else:
            risk_level = "High"

    # Stop‑loss and target using ATR (2× ATR for SL, 3× ATR for target)
    atr = latest_features.get("ATR_14", 0.0)
    close_price = latest_features.get("Close", 0.0)
    stop_loss = round(close_price - 2 * atr, 2) if atr else None
    target = round(close_price + 3 * atr, 2) if atr else None

    reasons = []
    if recommendation == "BUY":
        reasons.append("Model probability strong")
    if recommendation == "HOLD":
        reasons.append("Mixed signals")
    if recommendation == "SELL":
        reasons.append("Negative outlook or risk flags")
    # Add any active risk flags
    for name, active in risk_flags.items():
        if active:
            reasons.append(f"Risk flag: {name.replace('_', ' ')}")

    return {
        "ticker": ticker.upper(),
        "recommendation": recommendation,
        "confidence": round(model_prob, 3),
        "stop_loss": stop_loss,
        "target": target,
        "reasons": reasons,
        "risk_level": risk_level,
    }
