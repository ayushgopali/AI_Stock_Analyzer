from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Session
import datetime
import uuid

from ..db import Base, SessionLocal, init_db

class Watchlist(Base):
    __tablename__ = "watchlist"
    ticker = Column(String, primary_key=True, index=True)
    added_at = Column(DateTime, default=datetime.datetime.utcnow)

# Ensure tables exist
init_db()

def get_all():
    with SessionLocal() as db:
        items = db.query(Watchlist).all()
        return {"items": [{"ticker": w.ticker, "added_at": w.added_at.isoformat()} for w in items]}

def add(ticker: str):
    ticker = ticker.upper().strip()
    with SessionLocal() as db:
        existing = db.query(Watchlist).filter(Watchlist.ticker == ticker).first()
        if existing:
            w = existing
        else:
            w = Watchlist(ticker=ticker)
            db.add(w)
            db.commit()
            db.refresh(w)
        return {"ticker": w.ticker, "added_at": w.added_at.isoformat()}

def remove(ticker: str):
    ticker = ticker.upper().strip()
    with SessionLocal() as db:
        w = db.query(Watchlist).filter(Watchlist.ticker == ticker).first()
        if w:
            db.delete(w)
            db.commit()

