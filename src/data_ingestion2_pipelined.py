# this file is responsible for fetching data (players+match, players, match, team) from a public GitHub repo and further archive the data
# data archiving is done to freeze the data the model was trained on and also to make our system fault-tolerant
# next, all these data are read and stored in individual dataframes, collectively stored in one dictionary

import os
import requests
import pandas as pd
from typing import List, Dict, Optional
import shutil
from dotenv import load_dotenv

# configuration
DIRECTORY = r'C:\PROJECT\data\raw-data'
ARCHIVE_DIR = r'C:\PROJECT\data\archive-data'

owner = "olbauday"
repo = "FPL-Elo-Insights"
branch = "main"

load_dotenv(dotenv_path="C:/PROJECT/.env")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise RuntimeError("GitHub PAT not found in .env")

path_25 = "data/2025-2026/By Tournament/Premier League"

file_dir_map = {
    "playermatchstats.csv": os.path.join(DIRECTORY, "player-match-data-25"),
    "players.csv": os.path.join(DIRECTORY, "player-data-25"),
    "matches.csv": os.path.join(DIRECTORY, "match-data-github-25")
}

# github data ingestion via api
def download_github_gw_data(base_path: str, current_gw: int):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{base_path}?ref={branch}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"GitHub API error: {response.status_code}")
        return

    contents = response.json()

    for item in contents:
        name = item['name']

        # recursively, call this function till we reach at the leaf level of a directory by extracting the GW number
        # by ignoring all directories with GW number > current GW number, we only extract the files upto the current GW number
        if item['type'] == 'dir' and name.startswith('GW'):
            try:
                gw_number = int(name[2:])
            except ValueError:
                continue
            if gw_number > current_gw: 
                continue
            new_path = f"{base_path}/{name}"
            download_github_gw_data(new_path, current_gw)

        # if a file is encountered which corresponds to our 'file_dir_map', we download the file and save it to our local path
        elif item['type'] == 'file' and name in file_dir_map:
            download_url = item.get('download_url')
            if not download_url:
                continue

            gw_folder = base_path.split('/')[-1]  
            target_root = file_dir_map[name]
            local_dir = os.path.join(target_root, gw_folder)
            os.makedirs(local_dir, exist_ok=True)

            local_path = os.path.join(local_dir, name)

            if not os.path.exists(local_path):
                print(f"Downloading {name} -> {local_path}")
                file_bytes = requests.get(download_url).content
                with open(local_path, 'wb') as f:
                    f.write(file_bytes)
                    
            archive_file(local_path, gw_folder, name)

# archive the files for reproducibility
def archive_file(local_path: str, gw_folder: str, filename: str):
    season = "2025-2026"  
    archive_path = os.path.join(ARCHIVE_DIR, season, gw_folder, filename)

    if not os.path.exists(archive_path):
        os.makedirs(os.path.dirname(archive_path), exist_ok=True)
        shutil.copy2(local_path, archive_path)
        print(f"Archived -> {archive_path}")

# load the data from system in a dataframe
def load_gw_data(folder: str, csv_file: str, gw_num: int,
                 gw_column_name: str = 'Game Week') -> Optional[pd.DataFrame]:

    root = os.path.join(DIRECTORY, folder)
    all_gw_data: List[pd.DataFrame] = []

    for idx in range(1, gw_num + 1):
        gw_folder = f"GW{idx}"
        csv_path = os.path.join(root, gw_folder, csv_file)

        if os.path.exists(csv_path):
            temp_df = pd.read_csv(csv_path)
            temp_df[gw_column_name] = idx
            all_gw_data.append(temp_df)

    if all_gw_data:
        return pd.concat(all_gw_data, ignore_index=True)
    return None


def load_csv(folder: str, csv_file: str) -> Optional[pd.DataFrame]:
    csv_path = os.path.join(DIRECTORY, folder, csv_file)
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return None

# initial data normalization to ensure consistent & normalized data throughout
def preprocess_matches_df(df: pd.DataFrame) -> pd.DataFrame:
    df['kickoff_time'] = pd.to_datetime(df['kickoff_time'], format="mixed", errors='coerce')
    df['gameweek'] = df['gameweek'].astype(int, errors='ignore')
    return df.sort_values(by=['gameweek', 'kickoff_time']).reset_index(drop=True)

# main function
def load_all_data(current_gw: int = 22) -> Dict[str, pd.DataFrame]:

    print("\nUPDATING 2025 DATA FROM GITHUB!\n")
    download_github_gw_data(path_25, current_gw)

    print("\nLOADING RELATIONAL DATA!\n")
    dataframes: Dict[str, pd.DataFrame] = {}

    # 2024 (static)
    dataframes['pms_24'] = load_gw_data("player-match-data-24", "playermatchstats.csv", 38)
    dataframes['players_24'] = load_csv("player-data-24", "players.csv")
    matches_24 = load_csv("match-data-github-24", "matches.csv")
    dataframes['matches_24'] = preprocess_matches_df(matches_24)
    dataframes['teams_24'] = load_csv("team-data-24", "teams24.csv")

    # 2025 (dynamic)
    dataframes['pms_25'] = load_gw_data("player-match-data-25", "playermatchstats.csv", current_gw)
    dataframes['players_25'] = load_gw_data("player-data-25", "players.csv", current_gw)
    matches_25 = load_gw_data("match-data-github-25", "matches.csv", current_gw)
    dataframes['matches_25'] = preprocess_matches_df(matches_25)
    dataframes['teams_25'] = load_csv("team-data-25", "teams25.csv")

    print("\nDATA LOADING COMPLETE\n")
    return dataframes