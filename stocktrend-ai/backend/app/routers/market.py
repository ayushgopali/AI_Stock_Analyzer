from fastapi import APIRouter, HTTPException
from ..schemas import MarketResponse
from ..services import news, sentiment

router = APIRouter()

@router.get("/market", response_model=MarketResponse)
async def market():
    # placeholder – will aggregate market news & sentiment
    return {"overall_sentiment": 0.0, "news": []}
