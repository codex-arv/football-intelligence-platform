from pydantic import BaseModel
from typing import Dict

class Input(BaseModel):
    home_team: str
    away_team: str
    
    class Example:
        json_ex = {
            "example": {
                "home_team": "Arsenal",
                "away_team": "Chelsea"
            }
        }

class Output(BaseModel):
    home_team: str
    away_team: str
    scoreline: str
    raw_scoreline: str
    predicted_winner: str
    confidence_level: str
    probabilities: Dict[str, float]

    class Example:
        json_ex = {
            "example": {
                "home_team": "Arsenal",
                "away_team": "Chelsea",
                "scoreline": "2-1",
                "raw_scoreline": "1.850 - 1.200",
                "predicted_winner": "Arsenal",
                "confidence_level": "65.50%",
                "probabilities": {"away_win": 0.15, "draw": 0.195, "home_win": 0.655}
            }
        }

# class PlayerMatchStat(BaseModel):
#     player_id: int
#     player_name: str
#     position: str
#     name: str       
#     goals: int
#     assists: int
