import pandas as pd
import numpy as np
from typing import Dict, Tuple, List
import joblib
import os

OUTPUT_DIR = "data_artifacts"
MIN_MINUTES_PLAYED = 60 

# accepts the dictionary returned from data_ingestion2.py
# returns set of dataframes: players-matches, players, match, teams
def relational_data(dictionary: Dict[str, pd.DataFrame]) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    try:
        pms_24 = dictionary['pms_24']
        pms_25 = dictionary['pms_25'] 

        players_24 = dictionary['players_24']
        players_25 = dictionary['players_25']
        
        matches_24 = dictionary['matches_24']
        matches_25 = dictionary['matches_25']
        
        teams_24 = dictionary['teams_24']
        teams_25 = dictionary['teams_25']
    except Exception as e:
        raise Exception(f"Error: {e}")
    
    file_path_pms_24 = os.path.join(OUTPUT_DIR,'pms_24.pkl')
    file_path_pms_25 = os.path.join(OUTPUT_DIR,'pms_25.pkl')
    joblib.dump(pms_24, file_path_pms_24)
    joblib.dump(pms_25, file_path_pms_25)
    
    file_path_players_24 = os.path.join(OUTPUT_DIR,'players_24.pkl')
    file_path_players_25 = os.path.join(OUTPUT_DIR,'players_25.pkl')
    joblib.dump(players_24, file_path_players_24)
    joblib.dump(players_25, file_path_players_25)
    
    combined_pms = pd.concat([pms_24, pms_25], ignore_index=True)
    players_24_columns = set(players_24.columns)
    players_25_columns = set(players_25.columns)
    players_different_columns = players_25_columns.difference(players_24_columns)
    combined_players = pd.concat([players_24, players_25], ignore_index=True).drop(
        columns=players_different_columns, 
        errors='ignore'
    )
    combined_players = combined_players.drop_duplicates(subset=['player_id'], keep='first')
    # print(f"Combined Players data shape: {combined_players.shape}")
    matches_24_columns = set(matches_24.columns)
    matches_25_columns = set(matches_25.columns)
    matches_different_columns = matches_25_columns.difference(matches_24_columns)
    matches_24['season'] = 2024
    matches_25['season'] = 2025
    combined_matches = pd.concat([matches_24, matches_25], ignore_index=True).drop(
        columns=matches_different_columns, 
        errors='ignore'
    )
    # print(f"Combined Matches data shape: {combined_matches.shape}")
    teams_25 = teams_25.sort_values(by='id', ascending=True).reset_index(drop=True)
    combined_teams = pd.concat([teams_24, teams_25], ignore_index=True).drop(
        columns=['fotmob_name'], 
        errors='ignore'
    ).drop_duplicates()
    combined_teams.loc[combined_teams.index[:len(teams_24)], 'season'] = 2024
    combined_teams.loc[combined_teams.index[len(teams_24):], 'season'] = 2025
    combined_teams['season'] = combined_teams['season'].astype(int)
    # print(f"Combined Teams data shape: {combined_teams.shape}\n")
    return combined_pms, combined_players, combined_matches, combined_teams

# accepts pms data and players data, returned from relational_data function 
# returns the combined data of pms and players
def merge_pms_players(combined_pms: pd.DataFrame, combined_players: pd.DataFrame) -> pd.DataFrame:
    print("Merging Players Match Data with the Players data...\n")
    pms_players = combined_pms.merge(
        combined_players[['player_id', 'first_name', 'second_name', 'position', 'team_code']],
        on='player_id',
        how='left',
        suffixes=('_pms', '_static')
    )
    return pms_players

# accepts the combined data of pms and players returned from merge_pms_players
# returns the set of dataframes respective of the position of players 
def positional_classification(pms_players: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    print("Dividing the merged data into position specific stats...\n")
    position_map = {
    'Goalkeeper':'GK',
    'Defender':'DEF',
    'Midfielder':'MID',
    'Forward':'FWD',
    'Unknown':'NA'
    }
    pms_players['position_group'] = pms_players['position'].map(position_map)
    df1 = pms_players[pms_players['position_group']=='GK'].copy()
    df2 = pms_players[pms_players['position_group']=='DEF'].copy()
    df3 = pms_players[pms_players['position_group']=='MID'].copy()
    df4 = pms_players[pms_players['position_group']=='FWD'].copy()
    df1 = df1[['player_id', 'team_code', 'match_id', 'Game Week', 'minutes_played', 
                           'gk_accurate_passes', 'gk_accurate_long_balls', 
                           'saves', 'saves_inside_box', 
                           'goals_conceded', 'team_goals_conceded',
                           'xgot_faced', 'goals_prevented',
                           'sweeper_actions', 'high_claim']].copy()

    df2 = df2[['player_id', 'match_id', 'team_code', 'Game Week', 'minutes_played', 'xg', 'xa',
                                'accurate_passes', 'accurate_long_balls', 'final_third_passes',
                                'tackles_won', 'interceptions', 'recoveries', 'blocks', 'clearances', 
                                'headed_clearances', 'dribbled_past', 'duels_won',
                                'ground_duels_won', 'aerial_duels_won', 'was_fouled', 'fouls_committed',
                                'tackles', 'distance_covered', 'defensive_contributions']].copy()
    df2['tackles_won_percentage'] = df2['tackles_won'] / df2['tackles']
    df2 = df2.drop(columns='tackles', errors='ignore')
    df3 = df3[['player_id', 'match_id', 'team_code', 'Game Week', 'minutes_played',
                                'goals', 'assists', 'xg', 'xa',
                                'accurate_passes', 'accurate_crosses', 'accurate_long_balls', 'final_third_passes',
                                'total_shots', 'shots_on_target',
                                'chances_created', 'touches',
                                'successful_dribbles', 'corners',
                                'penalties_scored', 'penalties_missed',
                                'tackles_won', 'interceptions', 'recoveries', 'blocks', 'clearances',
                                'dribbled_past', 'duels_won', 'ground_duels_won', 'aerial_duels_won',
                                'was_fouled', 'fouls_committed',
                                'distance_covered', 'defensive_contributions']].copy()
    df4 = df4[['player_id', 'match_id', 'team_code', 'Game Week', 'minutes_played',
                                'goals', 'assists', 'xg', 'xa', 'xgot',
                                'accurate_passes', 'final_third_passes',
                                'total_shots', 'shots_on_target',
                                'chances_created', 'big_chances_missed', 'touches', 'touches_opposition_box',
                                'successful_dribbles', 'corners', 'offsides',
                                'penalties_scored', 'penalties_missed',
                                'duels_won', 'ground_duels_won', 'aerial_duels_won',
                                'was_fouled', 'fouls_committed', 'dispossessed']].copy()
    # print(f"Shape of GK stats: {df1.shape}")
    # print(f"Shape of DEF stats: {df2.shape}")
    # print(f"Shape of MID stats: {df3.shape}")
    # print(f"Shape of FWD stats: {df4.shape}\n")
    return df1, df2, df3, df4

# accepts the position-wise data of players returned from positional_classification
# returns the cleaned position-wise data
def positional_data_cleaning(multiple_df: Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]
                             ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    print("Cleaning the positional data now:\n")
    df1, df2, df3, df4 = multiple_df
    def_mid_drop_columns = ['defensive_contributions', 'distance_covered']
    fwd_drop_columns = ['dispossessed']
    df2 = df2.drop(columns=def_mid_drop_columns, errors='ignore')
    df3 = df3.drop(columns=def_mid_drop_columns, errors='ignore')
    print(f"{len(def_mid_drop_columns)} dropped from DEF & MID data")
    df4 = df4.drop(columns=fwd_drop_columns, errors='ignore')
    print(f"{len(fwd_drop_columns)} dropped from FWD data")
    df1['saves_inside_box'] = df1['saves_inside_box'].fillna(0)
    df2['tackles_won_percentage'] = df2['tackles_won_percentage'].fillna(0)
    df3['corners'] = df3['corners'].fillna(0)
    df4['corners'] = df4['corners'].fillna(0)
    print("Null columns were imputed with 0\n")
    return df1, df2, df3, df4

def rolling_features(df: pd.DataFrame, rolling: List[str], groupedby: str = 'player_id', prefix: str = 'L5_Avg_') -> pd.DataFrame:
    rolling_df = df.groupby(groupedby)[rolling].rolling(window=5, min_periods=1).mean().shift(1).reset_index()
    new_cols = ['player_id', 'chron_idx'] + [prefix + col for col in rolling]
    rolling_df.columns = new_cols
    first_row_idx = df.groupby(groupedby)['chron_idx'].min().values
    rolling_df['is_first_match'] = rolling_df['chron_idx'].isin(first_row_idx)
    for col in rolling_df.columns:
        if col.startswith(prefix):
            rolling_df.loc[rolling_df['is_first_match'], col] = np.nan
    merged_df = df.merge(
        rolling_df.drop(columns='is_first_match', errors='ignore'),
        on=['player_id', 'chron_idx'], 
        how='left'
    ).drop(columns='chron_idx')
    return merged_df

# accepts the position-wise data of players returned from positional_classification
# returns the feature-engineered position-wise data 
def relational_data_feature_engineering(multiple_df: Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]
                             ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    print("Starting feature engineering:")
    print("1. Extracting players who have played atleast 60 minutes of a game")
    df1, df2, df3, df4 = multiple_df
    # gk
    df1 = df1[df1['minutes_played'] >= MIN_MINUTES_PLAYED].copy()
    df1 = df1.sort_values(by=['player_id', 'Game Week'])
    df1 = df1.reset_index(drop=True)
    df1['chron_idx'] = df1.index
    # def    
    df2 = df2[df2['minutes_played'] >= MIN_MINUTES_PLAYED].copy()
    df2 = df2.sort_values(by=['player_id', 'Game Week'])
    df2 = df2.reset_index(drop=True)
    df2['chron_idx'] = df2.index
    # mid
    df3 = df3[df3['minutes_played'] >= MIN_MINUTES_PLAYED].copy()
    df3 = df3.sort_values(by=['player_id', 'Game Week'])
    df3 = df3.reset_index(drop=True)
    df3['chron_idx'] = df3.index
    # fwd
    df4 = df4[df4['minutes_played'] >= MIN_MINUTES_PLAYED].copy()
    df4 = df4.sort_values(by=['player_id', 'Game Week'])
    df4 = df4.reset_index(drop=True)
    print("2. Sorting the players by their ID and Game Week")
    df4['chron_idx'] = df4.index
    gk_rolling = ['gk_accurate_passes', 'gk_accurate_long_balls', 
              'saves', 'saves_inside_box', 
              'goals_conceded', 'team_goals_conceded', 
              'xgot_faced', 'goals_prevented' ,
              'sweeper_actions', 'high_claim']
    def_rolling = ['xg', 'xa', 'accurate_passes', 'accurate_long_balls', 'final_third_passes',
                'tackles_won', 'interceptions', 'recoveries', 'blocks', 'clearances',
                'headed_clearances', 'dribbled_past', 'duels_won', 'ground_duels_won',
                'aerial_duels_won', 'was_fouled', 'fouls_committed',
                'tackles_won_percentage']
    mid_rolling = ['goals', 'assists', 'xg', 'xa', 
                'accurate_passes', 'accurate_crosses', 'accurate_long_balls','final_third_passes', 
                'total_shots', 'shots_on_target',
                'chances_created', 'touches', 'successful_dribbles', 'corners',
                'penalties_scored', 'penalties_missed', 'tackles_won', 'interceptions',
                'recoveries', 'blocks', 'clearances', 'dribbled_past', 'duels_won',
                'ground_duels_won', 'aerial_duels_won', 'was_fouled', 'fouls_committed']
    fwd_rolling = ['goals', 'assists', 'xg', 'xa', 'xgot', 
                'accurate_passes', 'final_third_passes', 
                'total_shots', 'shots_on_target', 'chances_created', 'big_chances_missed', 
                'touches', 'touches_opposition_box', 'successful_dribbles', 'corners', 'offsides',
                'penalties_scored', 'penalties_missed', 'duels_won', 'ground_duels_won',
                'aerial_duels_won', 'was_fouled', 'fouls_committed']
    print("3. Creating engineered features for each positions for last 5 matches\n")
    fe_df1 = rolling_features(df1, gk_rolling)
    fe_df2 = rolling_features(df2, def_rolling)
    fe_df3 = rolling_features(df3, mid_rolling)
    fe_df4 = rolling_features(df4, fwd_rolling)
    return fe_df1, fe_df2, fe_df3, fe_df4

# accepts matches and teams returned from relational-data
# returns the combined matches and teams data
def merge_teams_matches(combined_matches: pd.DataFrame, combined_teams: pd.DataFrame) -> pd.DataFrame:
    print("Merging Matches and Teams...\n")
    home_strength_columns = ['name', 'code', 'season', 'strength', 
                             'strength_overall_home', 'strength_attack_home', 'strength_defence_home', 'elo']
    away_strength_columns = ['name', 'code', 'season', 'strength', 
                             'strength_overall_away', 'strength_attack_away', 'strength_defence_away', 'elo']
    df = combined_matches.merge(
        combined_teams[home_strength_columns].rename(
            columns={col: f'HT_{col}' for col in home_strength_columns if col not in ['code', 'season']}
        ),
        left_on=['home_team', 'season'],
        right_on=['code', 'season'],
        how='left'
    ).drop(columns='code', errors='ignore').copy()
    df = df.merge(
        combined_teams[away_strength_columns].rename(
            columns={col: f'AT_{col}' for col in away_strength_columns if col not in ['code', 'season']}
        ),
        left_on=['away_team', 'season'],
        right_on=['code', 'season'],
        how='left'
    ).drop(columns='code', errors='ignore').copy()
    # print(f"Shape of Merged Matches & Teams: {df.shape}\n")
    return df

# accepts the combined matches and teams data from merge_teams_matches
# returns the cleaned combined matches and teams 
def teams_matches_data_cleaning(teams_matches: pd.DataFrame) -> pd.DataFrame:
    print("Cleaning the data of merged Teams & Matches:")
    teams_matches['kickoff_time'] = pd.to_datetime(teams_matches['kickoff_time'], format="mixed")
    teams_matches = teams_matches.drop(columns='fotmob_id', errors='ignore')
    print("1. Sorting the data according to Game Week and Kickoff Time")
    teams_matches['gameweek'] = teams_matches['gameweek'].astype(int)
    teams_matches = teams_matches.sort_values(by=['gameweek', 'kickoff_time'], ascending=True).reset_index(drop=True)
    median_cols = ['home_team_elo', 'away_team_elo',
                   'home_possession', 'away_possession',
                   'home_tackles_won_pct', 'away_tackles_won_pct']
    print(f"2. Imputing {len(median_cols)} null columns with their respective median\n")
    for col in median_cols:
        median = teams_matches[col].median() 
        teams_matches[col] = teams_matches[col].fillna(median)
    teams_matches['elo_diff'] = teams_matches['home_team_elo'] - teams_matches['away_team_elo']    
    teams_matches = teams_matches.rename(columns={'home_team_elo':'ht_match_elo', 'away_team_elo':'at_match_elo'})
    teams_matches['kickoff_time'] = teams_matches['kickoff_time'].dt.normalize()
    teams_matches = teams_matches.rename(columns={'kickoff_time':'Date'}, errors='ignore')
    teams_matches['HT_name'] = teams_matches['HT_name'].replace({'Man Utd':'Man United', 'Spurs':'Tottenham'})
    teams_matches['AT_name'] = teams_matches['AT_name'].replace({'Man Utd':'Man United', 'Spurs':'Tottenham'})
    teams_matches = teams_matches.rename(columns={'HT_name':'HomeTeam', 'AT_name':'AwayTeam'}, errors='ignore')
    home1 = 'Brentford'
    away1 = 'Aston Villa'
    m1_date = '2025-08-23'
    m1_faulty = '2025-09-16'
    home2 = 'Wolves'
    away2 = 'Everton'
    m2_date = '2025-08-30'
    m2_faulty = '2025-09-23'
    teams_matches.loc[(teams_matches['Date'] == m1_faulty) & (teams_matches['HomeTeam'] == home1), 'Date'] = m1_date
    teams_matches.loc[(teams_matches['Date'] == m2_faulty) & (teams_matches['HomeTeam'] == home2), 'Date'] = m2_date
    return teams_matches

# main function!
def work_with_relational_data(dictionary: Dict[str, pd.DataFrame]) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    print("="*156)
    print("="*156)
    print()
    print(f"{" "*62}WORKING WITH THE RELATIONAL DATA!")
    print(f"{" "*40}(INVOLVES DATA CONSOLIDATING, MERGING, DIVIDING, CLEANING AND FEATURE ENGINEERING)\n")
    combined_pms, combined_players, combined_matches, combined_teams = relational_data(dictionary)
    pms_players = merge_pms_players(combined_pms, combined_players)
    gk_stats, def_stats, mid_stats, fwd_stats = positional_classification(pms_players)
    gk_stats, def_stats, mid_stats, fwd_stats = positional_data_cleaning((gk_stats, def_stats, mid_stats, fwd_stats))
    fe_gk_stats, fe_def_stats, fe_mid_stats, fe_fwd_stats = relational_data_feature_engineering((gk_stats, def_stats, mid_stats, fwd_stats))
    teams_matches = merge_teams_matches(combined_matches, combined_teams)
    joblib.dump(teams_matches, "e1.pkl")
    final_teams_matches = teams_matches_data_cleaning(teams_matches)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file_path_pms_players = os.path.join(OUTPUT_DIR, 'pms_players.pkl')
    joblib.dump(pms_players, file_path_pms_players)
    print("Final Shape of all data frames:")
    print(f"GK data: {fe_gk_stats.shape}")
    print(f"DEF data: {fe_def_stats.shape}")
    print(f"MID data: {fe_mid_stats.shape}")
    print(f"FWD data: {fe_fwd_stats.shape}")
    print(f"Matches & Teams data: {final_teams_matches.shape}\n")
    print(f"{" "*50}ALL RELATIONAL DATA ARE READY FOR MERGING WITH THE MASTER DATASET!\n")
    return fe_gk_stats, fe_def_stats, fe_mid_stats, fe_fwd_stats, final_teams_matches