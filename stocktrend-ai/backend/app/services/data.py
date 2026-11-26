import os
import json
from datetime import datetime, timedelta
from typing import List

import pandas as pd
import yfinance as yf
from sqlalchemy.orm import Session

from ..db import SessionLocal, PriceCache, init_db

# Initialise DB tables if not present
init_db()

CACHE_TTL_HOURS = int(os.getenv("YFINANCE_TTL_HOURS", "1"))

def _cache_key(ticker: str) -> str:
    return ticker.upper()

def _is_cache_valid(cached_at: datetime) -> bool:
    return datetime.utcnow() - cached_at < timedelta(hours=CACHE_TTL_HOURS)

def fetch_price_history(ticker: str, years: int = 5) -> pd.DataFrame:
    """Fetch OHLCV price data for the given Indian ticker.
    The ticker is automatically suffixed with '.NS' for NSE listings.
    Results are cached in SQLite for ``CACHE_TTL_HOURS``.
    """
    ticker = ticker.upper().strip()
    full_ticker = f"{ticker}.NS"  # NSE suffix; works for most Indian stocks
    cache_key = _cache_key(full_ticker)

    with SessionLocal() as db:
        cached = db.query(PriceCache).filter(PriceCache.ticker == cache_key).first()
        if cached and _is_cache_valid(cached.fetched_at):
            # Load cached JSON back into DataFrame
            data = json.loads(cached.data)
            df = pd.DataFrame(data)
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
            return df.sort_index()

        # No fresh cache – fetch from yfinance
        end = datetime.utcnow()
        start = end - timedelta(days=years * 365)
        yf_df = yf.download(full_ticker, start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"), progress=False)
        if yf_df.empty:
            raise ValueError(f"No price data returned for ticker {full_ticker}")

        # Store in cache (serialize to JSON for SQLite TEXT column)
        cache_entry = PriceCache(
            ticker=cache_key,
            data=yf_df.reset_index().to_json(date_format="iso"),
            fetched_at=datetime.utcnow(),
        )
        # Upsert
        if cached:
            db.delete(cached)
            db.flush()
        db.add(cache_entry)
        db.commit()

        yf_df.index.name = "Date"
        return yf_df
