# api/club_router.py
import json
from fastapi import APIRouter, HTTPException, Query
from pathlib import Path

router = APIRouter(prefix="/api/v1")

# Path to local JSON files
CLUB_DATA_DIR = Path(__file__).resolve().parent.parent / "lovable_website" / "src" / "data" / "clubs"

def load_local_club_file(club: str):
    """
    Loads a local JSON file matching the club name.
    Example: "Arsenal" → arsenal.json
    """
    filename = club.lower().replace(" ", "").replace("and", "") + ".json"
    filepath = CLUB_DATA_DIR / filename

    if not filepath.exists():
        raise HTTPException(
            status_code=404,
            detail=f"No local data found for club: {club}"
        )

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail=f"Error reading data for club: {club}"
        )


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
