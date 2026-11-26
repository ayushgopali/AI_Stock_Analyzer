import os
import json
from datetime import datetime, timedelta
from typing import List, Dict

import feedparser
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# Optional FinBERT import – only if toggle is true
if os.getenv("FINBERT_TOGGLE", "false").lower() == "true":
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch
    _finbert_tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
    _finbert_model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")
    _finbert_model.eval()
    def _finbert_score(text: str) -> float:
        inputs = _finbert_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            logits = _finbert_model(**inputs).logits
        probs = torch.softmax(logits, dim=1).cpu().numpy()[0]
        # label order: 0=negative,1=neutral,2=positive
        return float(probs[2] - probs[0])
else:
    _finbert_score = None

# Simple VADER wrapper
_analyzer = SentimentIntensityAnalyzer()

def _vader_score(text: str) -> float:
    return _analyzer.polarity_scores(text)["compound"]

CACHE_TTL_MIN = int(os.getenv("NEWS_TTL_MINUTES", "10"))
CACHE_FILE = os.path.join(os.getenv("MODEL_DIR", "models"), "news_cache.json")

_FEEDS = [
    "https://economictimes.indiatimes.com/rssfeedsdefault.cms?feedtype=ml&cntno=50",
    "https://www.livemint.com/rss/companies",
    "https://www.moneycontrol.com/rss/markets.xml",
]

def _load_cache() -> Dict:
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            data = json.load(f)
            ts = datetime.fromisoformat(data.get("fetched_at", "1970-01-01T00:00:00"))
            if datetime.utcnow() - ts < timedelta(minutes=CACHE_TTL_MIN):
                return data.get("items", [])
    return []

def _save_cache(items: List[Dict]):
    with open(CACHE_FILE, "w") as f:
        json.dump({"fetched_at": datetime.utcnow().isoformat(), "items": items}, f)

def _fetch_feed(url: str) -> List[Dict]:
    feed = feedparser.parse(url)
    entries = []
    for entry in feed.entries:
        entries.append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "date": entry.get("published", datetime.utcnow().isoformat()),
            "source": entry.get("source", {}).get("title", ""),
        })
    return entries

def _score_item(item: Dict) -> Dict:
    text = f"{item['title']} {item.get('summary', '')}"
    if _finbert_score:
        score = _finbert_score(text)
    else:
        score = _vader_score(text)
    label = "positive" if score > 0.05 else "negative" if score < -0.05 else "neutral"
    item.update({"sentiment_score": score, "sentiment_label": label})
    return item

def get_recent_news(ticker: str = None) -> List[Dict]:
    """Return cached news items; if cache is stale, refresh from RSS feeds.
    If *ticker* is provided, filter items that contain the ticker (case‑insensitive).
    """
    items = _load_cache()
    if not items:
        # Refresh all feeds
        all_items = []
        for url in _FEEDS:
            all_items.extend(_fetch_feed(url))
        # Add Google News search for the ticker/market if needed
        if ticker:
            query = f"{ticker} India stock market"
            # Simple Google News RSS (no API key) – limited but works for demo
            google_rss = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}"
            all_items.extend(_fetch_feed(google_rss))
        # Score each item
        items = [_score_item(it) for it in all_items]
        _save_cache(items)
    # Filter by ticker if supplied
    if ticker:
        tick = ticker.upper()
        items = [it for it in items if tick in it["title"].upper() or tick in it.get("summary", "").upper()]
    # Return most recent first (limit 20)
    items.sort(key=lambda x: x["date"], reverse=True)
    return items[:20]
