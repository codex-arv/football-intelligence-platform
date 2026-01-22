# this file is majorly responsible for maintaining one consistent dataframe by merging historical match data with the teams-matches data
# also aggregating the player based rolling features

import pandas as pd
from typing import Tuple
import joblib
import os

OUTPUT_DIR = "data_artifacts"

def load_merge_data(all_data: Tuple[pd.DataFrame, pd.DataFrame,
                                    pd.DataFrame, pd.DataFrame,
                                    pd.DataFrame, pd.DataFrame]) -> pd.DataFrame:
    master_df, fe_gk, fe_def, fe_mid, fe_fwd, teams_matches = all_data
    print("="*156)
    print("="*156)
    print()
    print(f"{" "*66}STARTING DATA MERGING!\n")

    # fixing faulty dates for specific fixtures
    teams_matches.loc[
        (teams_matches['season'] == 2025) &
        (teams_matches['HomeTeam'] == 'Brentford') &
        (teams_matches['AwayTeam'] == 'Man City'),
        'Date'
    ] = '2025-10-05'

    teams_matches.loc[
        (teams_matches['season'] == 2025) &
        (teams_matches['HomeTeam'] == 'Newcastle') &
        (teams_matches['AwayTeam'] == 'Fulham'),
        'Date'
    ] = '2025-10-25'

    teams_matches.loc[
        (teams_matches['season'] == 2025) &
        (teams_matches['HomeTeam'] == 'Arsenal') &
        (teams_matches['AwayTeam'] == 'Crystal Palace'),
        'Date'
    ] = '2025-10-26'

    # enforce datetime on both sides
    teams_matches['Date'] = pd.to_datetime(teams_matches['Date'])
    master_df['Date'] = pd.to_datetime(master_df['Date'])
    file_path_combined_teams_matches = os.path.join(OUTPUT_DIR, 'combined_tm.pkl')
    joblib.dump(teams_matches, file_path_combined_teams_matches)

    # multi-key merge 1 (master df and teams+matches)
    merged_1 = master_df.merge(
        teams_matches,
        on=['Date', 'season', 'HomeTeam', 'AwayTeam'],
        how='left',
        suffixes=('', '_tm')
    )
    merged_1 = merged_1.drop(columns=[col for col in merged_1.columns if col.endswith('_tm')], errors='ignore').rename(
        columns={'home_team':'HT_code', 'away_team':'AT_code'}
    )
    player_stats_df = {
        'GK':fe_gk,
        'DEF':fe_def,
        'MID':fe_mid,
        'FWD':fe_fwd
    }

    # converting player-level rolling form into team-level positional strength
    aggregated_data = []
    for position, stats in player_stats_df.items():
        print(f"Aggregating {position} stats...")
        rolling_cols = [col for col in stats.columns if col.startswith('L5_Avg')]
        agg_df = stats.groupby(['match_id', 'team_code'])[rolling_cols].mean().reset_index()
        print(f"{position} stats aggregated successfully! Shape: {agg_df.shape}\n")
        agg_df.columns = ['match_id', 'team_code'] + [f'{position}_{col}' for col in rolling_cols]
        aggregated_data.append(agg_df)
        
    final_players_stats = aggregated_data[0]
    for data in aggregated_data[1:]:
        final_players_stats = final_players_stats.merge(
            data,
            on=['match_id', 'team_code'],
            how='outer'
        )
    final_players_stats = final_players_stats.fillna(0)
    print(f"Final Aggregated Players stats ready! Shape: {final_players_stats.shape}\n")
    home_final_players_stats = final_players_stats.copy()
    player_features = [col for col in home_final_players_stats.columns if col not in ['match_id', 'team_code']]
    home_rename_map = {col: f'HT_TEMP_{col}' for col in player_features}
    home_final_players_stats = home_final_players_stats.rename(columns=home_rename_map)
    merged_2a = merged_1.merge(
        home_final_players_stats,
        left_on=['match_id', 'HT_code'],
        right_on=['match_id', 'team_code'],
        how='left'
    )
    home_players = [col for col in merged_2a.columns if col.startswith('HT_TEMP_')]
    home_rename_map_final = {col: col.replace('HT_TEMP_', 'HT_') for col in home_players}
    merged_2a = merged_2a.rename(columns=home_rename_map_final)
    merged_2a = merged_2a.drop(columns=['team_code'], errors='ignore')
    print("Home Team Player stats merged successfully!")
    away_final_players_stats = final_players_stats.copy()
    player_features = [col for col in away_final_players_stats.columns if col not in ['match_id', 'team_code']]
    away_rename_map = {col: f'AT_TEMP_{col}' for col in player_features}
    away_final_players_stats = away_final_players_stats.rename(columns=away_rename_map)
    merged_2b = merged_2a.merge(
        away_final_players_stats,
        left_on=['match_id', 'AT_code'],
        right_on=['match_id', 'team_code'],
        how='left'
    )
    away_players = [col for col in merged_2b.columns if col.startswith('AT_TEMP_')]
    away_rename_map_final = {col: col.replace('AT_TEMP_', 'AT_') for col in away_players}
    merged_2b = merged_2b.rename(columns=away_rename_map_final)
    merged_2b = merged_2b.drop(columns=['team_code'], errors='ignore')
    print("Away Team Player stats merged successfully!\n")
    merged_data = merged_2b.copy()
    print(f"Shape of the merged data: {merged_data.shape}\n")
    print(f"{" "*50}RELATIONAL DATA HAS BEEN SUCCESSFULLY MERGED WITH THE MASTER DATA!\n")
    return merged_data