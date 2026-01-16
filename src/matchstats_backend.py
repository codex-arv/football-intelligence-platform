import pandas as pd
import numpy as np
import joblib
from typing import Dict, List

def load_all_data():
    master_data = joblib.load("master_data.pkl")
    teams_matches = joblib.load("combined_teams_matches.pkl")

    pms_24 = joblib.load("pms_24.pkl")
    pms_25 = joblib.load("pms_25.pkl")

    players_24 = joblib.load("players_24.pkl")
    players_25 = joblib.load("players_25.pkl")

    teams_24 = pd.read_csv("teams24.csv")
    teams_25 = pd.read_csv("teams25.csv")

    return {
        "master": master_data,
        "teams_matches": teams_matches,
        "pms_24": pms_24,
        "pms_25": pms_25,
        "players_24": players_24,
        "players_25": players_25,
        "teams_24": teams_24,
        "teams_25": teams_25
    }


def prepare_master_data(master_data: pd.DataFrame,
                        teams_matches: pd.DataFrame) -> pd.DataFrame:

    final_master = master_data.merge(
        teams_matches[['Date', 'gameweek', 'HomeTeam', 'AwayTeam', 'match_id']],
        on=['Date', 'gameweek', 'HomeTeam', 'AwayTeam'],
        how='left',
        validate='m:1'
    )

    betting_cols = ['GBH', 'GBD', 'GBA', 'GB>2.5', 'GB<2.5', 'B365>2.5', 'B365<2.5', 'B365AHH', 'B365AHA', 'BbMxH', 'BbMxD', 'BbMxA', 
                    'BbMx>2.5', 'BbAv>2.5', 'BbMx<2.5', 'BbAv<2.5', 'BbAHh', 'BbAvAHH', 'BbAvAHA', 'PSH', 'PSD', 'PSA', 'P>2.5', 'P<2.5', 
                    'Max>2.5', 'Max<2.5', 'Avg>2.5', 'Avg<2.5', 'AHh', 'PAHH', 'PAHA', 'MaxAHH', 'MaxAHA', 'AvgAHH', 'AvgAHA', 
                    'MaxCH', 'MaxCD', 'MaxCA', 'B365C>2.5', 'B365C<2.5', 'MaxC>2.5', 'MaxC<2.5', 'B365CAHH', 'B365CAHA', 
                    'MaxCAHH', 'MaxCAHA', 'NormIP_Margin', 'NormIP_BbAvH', 'NormIP_BbAvD', 'NormIP_BbAvA', 'NormIP_AvgCH', 'NormIP_AvgCD', 
                    'NormIP_AvgCA', 'NormIP_PSCH', 'NormIP_PSCD', 'NormIP_PSCA', 'NormIP_MaxH', 'NormIP_MaxD', 'NormIP_MaxA', 'NormIP_AvgH', 
                    'NormIP_AvgD', 'NormIP_AvgA', 'NormIP_B365H', 'NormIP_B365D', 'NormIP_B365A', 'NormIP_B365CH', 'NormIP_B365CD', 
                    'NormIP_B365CA', 'NormIP_AvgC>2.5', 'NormIP_AvgC<2.5', 'NormIP_PC>2.5', 'NormIP_PC<2.5', 'IP_AHO_AvgCAHH', 'IP_AHO_AvgCAHA', 
                    'IP_AHO_PCAHH', 'IP_AHO_PCAHA'] 

    usable_cols = [col for col in master_data.columns if col not in betting_cols]
    final_master = master_data[usable_cols]

    basic_stats = ['Date', 'season', 'gameweek', 'match_id', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'Referee', 'HS', 'AS', 
                   'HST', 'AST', 'HC', 'AC', 'HF', 'AF', 'HY', 'AY', 'HR', 'AR', 'home_possession', 'away_possession',
                   'home_accurate_passes', 'home_accurate_passes_pct', 'away_accurate_passes', 'away_accurate_passes_pct',
                   'home_successful_dribbles', 'home_successful_dribbles_pct', 'away_successful_dribbles', 'away_successful_dribbles_pct', 
                   'home_tackles_won', 'home_tackles_won_pct', 'away_tackles_won', 'away_tackles_won_pct', 'home_expected_goals_xg', 
                   'away_expected_goals_xg', 'home_passes', 'away_passes', 'home_interceptions', 'away_interceptions',
                   'home_keeper_saves', 'away_keeper_saves', 'home_duels_won', 'away_duels_won']     
    
    rolling_features = ['HT_AvgGF_L5', 'AT_AvgGF_L5', 'HT_AvgGA_L5', 'AT_AvgGA_L5', 'HT_AvgShots_L5', 'AT_AvgShots_L5', 'HT_ShotAccuracy_L5', 'AT_ShotAccuracy_L5',
                        'HT_ShotConversion_L5', 'AT_ShotConversion_L5', 'HT_CS_L5', 'AT_CS_L5', 'HT_WinRate_L5', 'AT_WinRate_L5']  

    final_master = final_master[basic_stats + rolling_features]

    final_master.loc[
        (final_master['Date'] == '2025-10-05') &
        (final_master['HomeTeam'] == 'Brentford'),
        'gameweek'] = 7

    final_master.loc[
        (final_master['Date'] == '2025-10-25') &
        (final_master['HomeTeam'] == 'Newcastle'),
        'gameweek'] = 9

    final_master.loc[
        (final_master['Date'] == '2025-10-26') &
        (final_master['HomeTeam'] == 'Arsenal'),
        'gameweek'] = 9

    return final_master

def prepare_players_match_data(
    pms_24: pd.DataFrame,
    pms_25: pd.DataFrame,
    players_24: pd.DataFrame,
    players_25: pd.DataFrame,
    teams_24: pd.DataFrame,
    teams_25: pd.DataFrame
):
    pms_24_ga = pms_24[(pms_24['goals'] > 0) | (pms_24['assists'] > 0)].reset_index(drop=True)
    usable_pms_24_cols = list(pms_24_ga.isnull().sum()[pms_24_ga.isnull().sum() == 0].index)
    pms_24_ga = pms_24_ga[usable_pms_24_cols]
    pms_24_ga = pms_24_ga.rename(columns={'Game Week': 'gameweek'}, errors='ignore')

    players_24 = players_24.rename(columns={'team_code': 'code'}, errors='ignore')
    players_matches_24 = pms_24_ga.merge(
        players_24[['player_id', 'first_name', 'second_name', 'position', 'code']],
        on='player_id',
        how='left',
        validate='m:1'
    )
    players_matches_24['season'] = 2024
    players_matches_24 = players_matches_24.merge(
        teams_24[['code', 'name']],
        on='code',
        how='left'
    )
    valid_24_cols = [
        col for col, val in dict(players_matches_24.eq(0.0).sum()).items()
        if val < players_matches_24.shape[0] * 0.6
    ]
    players_matches_24_final = players_matches_24[valid_24_cols]


    pms_25_ga = pms_25[(pms_25['goals'] > 0) | (pms_25['assists'] > 0)].reset_index(drop=True)
    usable_pms_25_cols = list(pms_25_ga.isnull().sum()[pms_25_ga.isnull().sum() == 0].index)
    pms_25_ga = pms_25_ga[usable_pms_25_cols]
    pms_25_ga = pms_25_ga.rename(columns={'Game Week': 'gameweek'}, errors='ignore')

    players_25 = players_25.rename(
        columns={'team_code': 'code', 'Game Week': 'gameweek'},
        errors='ignore'
    )
    players_matches_25 = pms_25_ga.merge(
        players_25[['player_id', 'gameweek', 'first_name', 'second_name', 'position', 'code']],
        on=['player_id', 'gameweek'],
        how='left',
        validate='m:1'
    )
    players_matches_25['season'] = 2025
    players_matches_25 = players_matches_25.merge(
        teams_25[['code', 'name']],
        on='code',
        how='left'
    )
    valid_25_cols = [
        col for col, val in dict(players_matches_25.eq(0.0).sum()).items()
        if val < players_matches_25.shape[0] * 0.6
    ]
    players_matches_25_final = players_matches_25[valid_25_cols]
    return players_matches_24_final, players_matches_25_final
