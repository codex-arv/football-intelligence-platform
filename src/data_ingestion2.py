import os
import pandas as pd
from typing import List, Dict, Optional

DIRECTORY = r'C:\PROJECT\data\raw-data'

def load_gw_data(folder: str, sub_folder: str, csv_file: str, gw_num: int, 
                  gw_column_name: str = 'Game Week') -> Optional[pd.DataFrame]:
    root = os.path.join(DIRECTORY, folder)
    all_gw_data: List[pd.DataFrame] = []
    for idx in range(1, gw_num + 1):
        gw_folder = f"GW{idx}"
        csv_path = os.path.join(root, gw_folder, csv_file)
        
        if os.path.exists(csv_path):
            try:
                temp_df = pd.read_csv(csv_path)
                temp_df[gw_column_name] = idx
                all_gw_data.append(temp_df)
            except Exception as e:
                 print(f"Error reading {csv_path}: {e}")
        else: print(f"{gw_folder} not found!\n")

    if all_gw_data:
        combined_df = pd.concat(all_gw_data, ignore_index=True)
        print(f"Successfully combined {len(all_gw_data)} GW files from {folder}\nShape: {combined_df.shape}\n")
        return combined_df
    else:
        print(f"No files were found for folder: {folder}")
        return None

def load_csv(folder: str, csv_file: str) -> Optional[pd.DataFrame]:
    root = os.path.join(DIRECTORY, folder)
    csv_single = os.path.join(root, csv_file)
    if os.path.exists(csv_single):
        try:
            df = pd.read_csv(csv_single)
            print(f"{csv_file} loaded from {folder}\nShape: {df.shape}\n")
            return df
        except Exception as e:
            print(f"Error reading {csv_single}: {e}")
            return None
    else:
        print(f"Error: {csv_file} not found!")
        return None

def preprocess_matches_df(df: pd.DataFrame) -> pd.DataFrame:
    if 'kickoff_time' in df.columns:
        df['kickoff_time'] = pd.to_datetime(df['kickoff_time'], format="mixed", errors='coerce')
    if 'gameweek' in df.columns:
        df['gameweek'] = df['gameweek'].astype(int, errors='ignore')
    df = df.sort_values(by=['gameweek', 'kickoff_time'], ascending=True).reset_index(drop=True)
    return df

# main function!
def load_all_data() -> Dict[str, pd.DataFrame]:
    print("="*156)
    print("="*156)
    print(f"\n{" "*64}LOADING THE RELATIONAL DATA!\n")
    dataframes: Dict[str, pd.DataFrame] = {}

    print("1. Loading 2024 Season Data:\n")
    pms_24 = load_gw_data("player-match-data-24", "GW", "playermatchstats.csv", 38)
    if pms_24 is not None: dataframes['pms_24'] = pms_24
    players_24 = load_csv("player-data-24", "players.csv")
    if players_24 is not None: dataframes['players_24'] = players_24
    matches_24 = load_csv("match-data-github-24", "matches.csv")
    if matches_24 is not None: 
        dataframes['matches_24'] = preprocess_matches_df(matches_24)
    teams_24 = load_csv("team-data-24", "teams24.csv")
    if teams_24 is not None: dataframes['teams_24'] = teams_24

    print("2. Loading 2025 Season Data:\n")
    pms_25 = load_gw_data("player-match-data-25", "GW", "playermatchstats.csv", 21)
    if pms_25 is not None: dataframes['pms_25'] = pms_25    
    players_25 = load_gw_data("player-data-25", "GW", "players.csv", 21)
    if players_25 is not None: dataframes['players_25'] = players_25
    matches_25 = load_gw_data("match-data-github-25", "GW", "matches.csv", 21)
    if matches_25 is not None: 
        dataframes['matches_25'] = preprocess_matches_df(matches_25)
    teams_25 = load_csv("team-data-25", "teams25.csv")
    if teams_25 is not None: dataframes['teams_25'] = teams_25
    print(f"{" "*63}RELATIONAL DATA LOADING COMPLETE!\n")
    return dataframes

