import pandas as pd
import joblib
from typing import Dict, Tuple, List
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data_artifacts"   

def load_all_data():
    master_data = joblib.load(DATA_DIR / "master_data.pkl")
    teams_matches = joblib.load(DATA_DIR / "combined_tm.pkl")

    pms_24 = joblib.load(DATA_DIR / "pms_24.pkl")
    pms_25 = joblib.load(DATA_DIR / "pms_25.pkl")

    players_24 = joblib.load(DATA_DIR / "players_24.pkl")
    players_25 = joblib.load(DATA_DIR / "players_25.pkl")

    teams_24 = pd.read_csv(DATA_DIR / "teams24.csv")
    teams_25 = pd.read_csv(DATA_DIR / "teams25.csv")

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


def prepare_master_data(
    final_master: pd.DataFrame,
    teams_matches: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, List]:

    betting_cols = [
        'GBH','GBD','GBA','GB>2.5','GB<2.5','B365>2.5','B365<2.5','B365AHH','B365AHA',
        'BbMxH','BbMxD','BbMxA','BbMx>2.5','BbAv>2.5','BbMx<2.5','BbAv<2.5',
        'BbAHh','BbAvAHH','BbAvAHA','PSH','PSD','PSA','P>2.5','P<2.5',
        'Max>2.5','Max<2.5','Avg>2.5','Avg<2.5','AHh','PAHH','PAHA',
        'MaxAHH','MaxAHA','AvgAHH','AvgAHA','MaxCH','MaxCD','MaxCA',
        'B365C>2.5','B365C<2.5','MaxC>2.5','MaxC<2.5','B365CAHH','B365CAHA',
        'MaxCAHH','MaxCAHA','NormIP_Margin','NormIP_BbAvH','NormIP_BbAvD',
        'NormIP_BbAvA','NormIP_AvgCH','NormIP_AvgCD','NormIP_AvgCA',
        'NormIP_PSCH','NormIP_PSCD','NormIP_PSCA','NormIP_MaxH','NormIP_MaxD',
        'NormIP_MaxA','NormIP_AvgH','NormIP_AvgD','NormIP_AvgA',
        'NormIP_B365H','NormIP_B365D','NormIP_B365A','NormIP_B365CH',
        'NormIP_B365CD','NormIP_B365CA','NormIP_AvgC>2.5',
        'NormIP_AvgC<2.5','NormIP_PC>2.5','NormIP_PC<2.5',
        'IP_AHO_AvgCAHH','IP_AHO_AvgCAHA','IP_AHO_PCAHH','IP_AHO_PCAHA'
    ]

    usable_cols = [col for col in final_master.columns if col not in betting_cols]
    final_master = final_master[usable_cols]

    basic_stats = [
        'Date','season','gameweek','match_id','HomeTeam','AwayTeam',
        'FTHG','FTAG','FTR','Referee','HS','AS','HST','AST',
        'HC','AC','HF','AF','HY','AY','HR','AR',
        'home_possession','away_possession',
        'home_accurate_passes','home_accurate_passes_pct',
        'away_accurate_passes','away_accurate_passes_pct',
        'home_successful_dribbles','home_successful_dribbles_pct',
        'away_successful_dribbles','away_successful_dribbles_pct',
        'home_tackles_won','home_tackles_won_pct',
        'away_tackles_won','away_tackles_won_pct',
        'home_expected_goals_xg','away_expected_goals_xg',
        'home_passes','away_passes',
        'home_interceptions','away_interceptions',
        'home_keeper_saves','away_keeper_saves',
        'home_duels_won','away_duels_won'
    ]

    rolling_features = [
        'HT_AvgGF_L5','AT_AvgGF_L5','HT_AvgGA_L5','AT_AvgGA_L5',
        'HT_AvgShots_L5','AT_AvgShots_L5',
        'HT_ShotAccuracy_L5','AT_ShotAccuracy_L5',
        'HT_ShotConversion_L5','AT_ShotConversion_L5',
        'HT_CS_L5','AT_CS_L5',
        'HT_WinRate_L5','AT_WinRate_L5'
    ]

    print("Code working after merge and before subsetting the columns!\n")

    required_cols = basic_stats + rolling_features
    missing = [c for c in required_cols if c not in final_master.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
#     teams_matches.loc[
#     (teams_matches['gameweek'] == 7) & (teams_matches['HomeTeam'] == 'Brentford'), 'Date'] = '2025-10-05'

#     teams_matches.loc[
#     (teams_matches['gameweek'] == 9) & (teams_matches['HomeTeam'] == 'Newcastle'), 'Date'] = '2025-10-25'

#     teams_matches.loc[
#     (teams_matches['gameweek'] == 9) & (teams_matches['HomeTeam'] == 'Arsenal'), 'Date'] = '2025-10-26'

#     teams_matches['Date'] = pd.to_datetime(
#         teams_matches['Date'],
#         errors='coerce'
# )

    # final_master.loc[
    #     (final_master['Date'] == '2025-10-05') &
    #     (final_master['HomeTeam'] == 'Brentford'),
    #     ['gameweek','match_id']
    # ] = [7, '25-26-prem-brentford-vs-manchester-city']

    # final_master.loc[
    #     (final_master['Date'] == '2025-10-25') &
    #     (final_master['HomeTeam'] == 'Newcastle'),
    #     ['gameweek','match_id']
    # ] = [9, '25-26-prem-newcastle-vs-fulham']

    # final_master.loc[
    #     (final_master['Date'] == '2025-10-26') &
    #     (final_master['HomeTeam'] == 'Arsenal'),
    #     ['gameweek','match_id']
    # ] = [9, '25-26-prem-arsenal-vs-crystal-palace']

    final_master = final_master[required_cols]

    return final_master, final_master[basic_stats], final_master[rolling_features], required_cols


def prepare_players_match_data(
    pms_24: pd.DataFrame,
    pms_25: pd.DataFrame,
    players_24: pd.DataFrame,
    players_25: pd.DataFrame,
    teams_24: pd.DataFrame,
    teams_25: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:

    pms_24_ga = pms_24[(pms_24['goals'] > 0) | (pms_24['assists'] > 0)].reset_index(drop=True)
    usable_cols_24 = pms_24_ga.isnull().sum()[pms_24_ga.isnull().sum() == 0].index
    pms_24_ga = pms_24_ga[list(usable_cols_24)]
    pms_24_ga = pms_24_ga.rename(columns={'Game Week': 'gameweek'}, errors='ignore')

    pms_25_ga = pms_25[(pms_25['goals'] > 0) | (pms_25['assists'] > 0)].reset_index(drop=True)
    usable_cols_25 = pms_25_ga.isnull().sum()[pms_25_ga.isnull().sum() == 0].index
    pms_25_ga = pms_25_ga[list(usable_cols_25)]
    pms_25_ga = pms_25_ga.rename(columns={'Game Week': 'gameweek'}, errors='ignore')

    players_24 = players_24.rename(columns={'team_code': 'code'}, errors='ignore')
    pm_final_24 = pms_24_ga.merge(
        players_24[['player_id','first_name','second_name','position','code']],
        on='player_id',
        how='left',
        validate='m:1'
    )
    pm_final_24 = pm_final_24.merge(teams_24[['code','name']], on='code', how='left')

    players_25 = players_25.rename(
        columns={'team_code':'code','Game Week':'gameweek'},
        errors='ignore'
    )
    pm_final_25 = pms_25_ga.merge(
        players_25[['player_id','gameweek','first_name','second_name','position','code']],
        on=['player_id','gameweek'],
        how='left',
        validate='m:1'
    )
    pm_final_25 = pm_final_25.merge(teams_25[['code','name']], on='code', how='left')

    valid_24_cols = [
        c for c, v in pm_final_24.eq(0.0).sum().items()
        if v < pm_final_24.shape[0] * 0.6
    ]
    pm_24_final = pm_final_24[valid_24_cols]

    valid_25_cols = [
        c for c, v in pm_final_25.eq(0.0).sum().items()
        if v < pm_final_25.shape[0] * 0.6
    ]
    pm_25_final = pm_final_25[valid_25_cols]

    pm_24_final["player_name"] = (pm_24_final["first_name"] + " " + pm_24_final["second_name"])
    pm_25_final["player_name"] = (pm_25_final["first_name"] + " " + pm_25_final["second_name"])

    # --- Brentford vs Man City (GW7)
    pm_25_final.loc[
        (pm_25_final['gameweek'] == 7) & (pm_25_final['name'] == 'Brentford'),
        'match_id'
    ] = '25-26-prem-brentford-vs-manchester-city'

    pm_25_final.loc[
        (pm_25_final['gameweek'] == 7) & (pm_25_final['name'] == 'Manchester City'),
        'match_id'
    ] = '25-26-prem-brentford-vs-manchester-city'


    # --- Newcastle vs Fulham (GW9)
    pm_25_final.loc[
        (pm_25_final['gameweek'] == 9) & (pm_25_final['name'] == 'Newcastle'),
        'match_id'
    ] = '25-26-prem-newcastle-vs-fulham'

    pm_25_final.loc[
        (pm_25_final['gameweek'] == 9) & (pm_25_final['name'] == 'Fulham'),
        'match_id'
    ] = '25-26-prem-newcastle-vs-fulham'


    # --- Arsenal vs Crystal Palace (GW9)
    pm_25_final.loc[
        (pm_25_final['gameweek'] == 9) & (pm_25_final['name'] == 'Arsenal'),
        'match_id'
    ] = '25-26-prem-arsenal-vs-crystal-palace'

    pm_25_final.loc[
        (pm_25_final['gameweek'] == 9) & (pm_25_final['name'] == 'Crystal Palace'),
        'match_id'
    ] = '25-26-prem-arsenal-vs-crystal-palace'

    pm_24_cols = list(pm_24_final.columns)
    pm_25_cols = list(pm_25_final.columns)

    return pm_24_final, pm_25_final
