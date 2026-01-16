from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from .stats_router import router as stats_router
from .club_router import router as club_router
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
                   "https://football-intelligence-api-o1dh.onrender.com"],
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
    load_data_once()
    load_model_once()


@app.get("/")
async def root():
    return {"message": "API is running. Visit /docs"}


@app.get("/api/v1/teams", response_model=List[str])
async def teams():
    return get_all_teams()


@app.post("/api/v1/predict")
async def predict(req: MatchRequest):
    return predict_match(req.home_team, req.away_team)