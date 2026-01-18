from fastapi import APIRouter, HTTPException
from typing import List, Dict
import numpy as np
import pandas as pd
from src.stats_data_loader import (
    load_all_data,
    prepare_master_data,
    prepare_players_match_data
)

router = APIRouter(
    prefix="/api/v1/stats",
    tags=["Match Statistics"]
)
STATS_MASTER: pd.DataFrame | None = None
STATS_MASTER_BASIC: pd.DataFrame | None = None
STATS_MASTER_ROLLING: pd.DataFrame | None = None
PLAYERS_MATCHES_24: pd.DataFrame | None = None
PLAYERS_MATCHES_25: pd.DataFrame | None = None
STATS : List | None = None


def ensure_stats_loaded():
    global STATS_MASTER, STATS_MASTER_BASIC, STATS_MASTER_ROLLING, STATS, PLAYERS_MATCHES_24, PLAYERS_MATCHES_25
    if STATS_MASTER is not None:
        return
    try:
        raw = load_all_data()
        STATS_MASTER, STATS_MASTER_BASIC, STATS_MASTER_ROLLING, STATS = prepare_master_data(
            raw["master"],
            raw["teams_matches"]
        )

        PLAYERS_MATCHES_24, PLAYERS_MATCHES_25 = prepare_players_match_data(
            raw["pms_24"],
            raw["pms_25"],
            raw["players_24"],
            raw["players_25"],
            raw["teams_24"],
            raw["teams_25"]
        )


    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load stats data: {str(e)}"
        )



@router.get("/health")
def stats_health():
    ensure_stats_loaded()

    return {
        "status": "OK",
        "master_rows": int(len(STATS_MASTER)),
        "players_2024_rows": int(len(PLAYERS_MATCHES_24)),
        "players_2025_rows": int(len(PLAYERS_MATCHES_25))
    }

@router.get("/matches")
def get_matches(season: int, gameweek: int):
    ensure_stats_loaded()

    df = STATS_MASTER[
        (STATS_MASTER["season"] == season) &
        (STATS_MASTER["gameweek"] == gameweek)
    ]

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="No matches found for given season and gameweek"
        )

    return df[[
        "match_id",
        "HomeTeam",
        "AwayTeam",
        "FTHG",
        "FTAG"
    ]].to_dict(orient="records")


@router.get("/match/basic")
def get_basic_match_stats(
    season: int,
    gameweek: int,
    home: str,
    away: str
):
    ensure_stats_loaded()

    row = STATS_MASTER[
        (STATS_MASTER["season"] == season) &
        (STATS_MASTER["gameweek"] == gameweek) &
        (STATS_MASTER["HomeTeam"] == home) &
        (STATS_MASTER["AwayTeam"] == away)
    ]

    if row.empty:
        raise HTTPException(status_code=404, detail="Match not found")
    
    return row.iloc[0].to_dict()

def resolve_match_id(
    season: int,
    gameweek: int,
    home: str,
    away: str
) -> str:
    row = STATS_MASTER[
        (STATS_MASTER["season"] == season) &
        (STATS_MASTER["gameweek"] == gameweek) &
        (STATS_MASTER["HomeTeam"] == home) &
        (STATS_MASTER["AwayTeam"] == away)
    ]
    if row.empty:
        raise HTTPException(status_code=404, detail="Match not found")
    return str(row.iloc[0]["match_id"])

@router.get("/players")
def get_player_stats(
    season: int,
    gameweek: int,
    home: str,
    away: str
):
    ensure_stats_loaded()
    match_id = resolve_match_id(season, gameweek, home, away)
    if season == 2024:
        df = PLAYERS_MATCHES_24
    elif season == 2025:
        df = PLAYERS_MATCHES_25
    else:
        raise HTTPException(status_code=400, detail="Invalid season")
    players = df[df["match_id"] == match_id]
    if players.empty:
        raise HTTPException(
            status_code=404,
            detail="No player data found for this match"
        )
    return players.to_dict(orient="records")

