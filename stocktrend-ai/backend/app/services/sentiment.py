from .data import fetch_price_history
import pandas as pd

def aggregate_sentiment(ticker: str = None):
    """Return overall sentiment score (average of sentiment_score) and list of items.
    If *ticker* is provided, also returns stock‑specific sentiment (average of filtered items).
    """
    from .news import get_recent_news
    # Market‑wide news (no ticker filter)
    market_items = get_recent_news()
    market_score = sum(item["sentiment_score"] for item in market_items) / len(market_items) if market_items else 0.0
    # Stock‑specific news
    stock_items = get_recent_news(ticker) if ticker else []
    stock_score = sum(item["sentiment_score"] for item in stock_items) / len(stock_items) if stock_items else 0.0
    return {
        "market_score": market_score,
        "market_items": market_items,
        "stock_score": stock_score,
        "stock_items": stock_items,
    }
