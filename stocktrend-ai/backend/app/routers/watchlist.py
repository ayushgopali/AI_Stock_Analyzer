from fastapi import APIRouter, HTTPException
from ..schemas import WatchlistResponse, WatchlistItem
from ..services import watchlist as wl_service

router = APIRouter()

@router.get("/watchlist", response_model=WatchlistResponse)
async def get_watchlist():
    return wl_service.get_all()

@router.post("/watchlist", response_model=WatchlistItem)
async def add_watchlist(ticker: str):
    return wl_service.add(ticker)

@router.delete("/watchlist", response_model=dict)
async def delete_watchlist(ticker: str):
    wl_service.remove(ticker)
    return {"detail": "removed"}
