# api/club_router.py
import json
from fastapi import APIRouter, HTTPException, Query
from pathlib import Path

CLUB_CACHE: dict[str, dict] = {}

# Path to local JSON files
CLUB_DATA_DIR = Path(__file__).resolve().parent.parent / "lovable_website" / "src" / "data" / "clubs"

router = APIRouter(prefix="/api/v1")

def preload_club_data():
    global CLUB_CACHE
    CLUB_CACHE = {}

    if not CLUB_DATA_DIR.exists():
        raise RuntimeError(f"Club data directory not found: {CLUB_DATA_DIR}")

    for file in CLUB_DATA_DIR.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                CLUB_CACHE[file.stem] = json.load(f)
        except Exception as e:
            print(f"⚠️ Failed to load {file.name}: {e}")

def load_local_club_file(club: str):
    key = club.lower().replace(" ", "").replace("&", "")
    if key not in CLUB_CACHE:
        raise HTTPException(
            status_code=404,
            detail=f"No local data found for club: {club}"
        )
    return CLUB_CACHE[key]



@router.get("/club")
def get_club(club: str = Query(..., description="Club name")):
    """
    Returns the EXACT full JSON file content for the club.
    No extra fields, just the keys and values from the JSON file.
    """
    if not club or not club.strip():
        raise HTTPException(status_code=400, detail="Missing club parameter")

    club_clean = club.strip()

    # Load the JSON file
    data = load_local_club_file(club_clean)

    # Return exactly the JSON contents
    return data
