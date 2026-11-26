from fastapi import APIRouter, HTTPException
from ..schemas import HistoryResponse
from ..services import history as hist_service

router = APIRouter()

@router.get("/history", response_model=HistoryResponse)
async def get_history(ticker: str):
    return hist_service.get_history(ticker)
