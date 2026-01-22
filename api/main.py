from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from .stats_router import router as stats_router
from .stats_router import ensure_stats_loaded
from .club_router import router as club_router
from .club_router import preload_club_data

from src.live_feature_calculation import (
    load_data_once,
    load_model_once,
    get_all_teams,
    predict_match
)

app = FastAPI(
    title="Football Prediction API",
    description="Live predictions + historical match stats"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080",
                   "http://10.58.74.41:8080",
                   "https://football-intelligence-api-o1dh.onrender.com",
                   "https://the90thminute.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(club_router)
app.include_router(stats_router)


class MatchRequest(BaseModel):
    home_team: str
    away_team: str


@app.on_event("startup")
async def startup_event():
    print("Initializing backend...")

@app.get("/health")
async def health_check():
    return {"status": "alive", "mode": "warm-up"}


@app.get("/")
async def root():
    return {"message": "API is running. Visit /docs"}


@app.get("/api/v1/teams", response_model=List[str])
async def teams():
    print("Loading Data...")
    load_data_once()
    return get_all_teams()


@app.post("/api/v1/predict")
async def predict(req: MatchRequest):
    print("Loading Data...")
    load_data_once()
    print("Loading Models...")
    load_model_once()
    return predict_match(req.home_team, req.away_team)