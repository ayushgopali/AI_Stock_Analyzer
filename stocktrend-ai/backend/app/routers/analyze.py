from fastapi import APIRouter, HTTPException
from ..schemas import AnalyzeResponse
from ..services import models, advice

router = APIRouter()

@router.get("/analyze", response_model=AnalyzeResponse)
async def analyze(ticker: str):
    if not ticker:
        raise HTTPException(status_code=400, detail="Ticker required")
    # Train model for ticker if not already trained
    try:
        prob = models.predict_next_day(ticker)
    except FileNotFoundError:
        models.train_models(ticker)
        prob = models.predict_next_day(ticker)
    # Generate recommendation using advice engine
    result = advice.advise(ticker, prob)
    return result
