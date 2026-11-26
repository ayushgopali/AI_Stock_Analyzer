from pydantic import BaseModel, Field
from typing import List, Optional

# -------------------
# API response models
# -------------------
class AnalyzeResponse(BaseModel):
    ticker: str = Field(..., description="Requested ticker symbol")
    recommendation: str = Field(..., description="BUY / HOLD / SELL")
    confidence: float = Field(..., ge=0, le=1, description="Probability of UP direction")
    stop_loss: Optional[float] = None
    target: Optional[float] = None
    reasons: List[str] = []
    risk_level: str = Field(..., description="Low / Medium / High")

class MarketNewsItem(BaseModel):
    title: str
    source: str
    link: str
    date: str
    sentiment_score: float
    sentiment_label: str

class MarketResponse(BaseModel):
    overall_sentiment: float
    news: List[MarketNewsItem]

class WatchlistItem(BaseModel):
    ticker: str
    added_at: str

class WatchlistResponse(BaseModel):
    items: List[WatchlistItem]

class HistoryRecord(BaseModel):
    date: str
    predicted: str
    actual: str
    confidence: float

class HistoryResponse(BaseModel):
    ticker: str
    records: List[HistoryRecord]

class HealthResponse(BaseModel):
    status: str = Field(..., description="Service health status, e.g. 'ok'")
