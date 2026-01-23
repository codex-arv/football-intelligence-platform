import warnings
import numpy as np
import pandas as pd
from typing import Tuple
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

RAW_STATS = ['HTHG', 'HTAG', 'HTR', 'Referee', 'home_score', 'away_score', 'gameweek', 'finished', 'match_url',
       'home_total_shots', 'away_total_shots', 'home_shots_on_target', 'away_shots_on_target',
       'home_fouls_committed', 'away_fouls_committed', 'home_corners', 'away_corners',
       'home_yellow_cards', 'away_yellow_cards', 'home_red_cards', 'away_red_cards',
       'fotmob_id', 'stats_processed', 'player_stats_processed']

ODDS = [
    'GBH', 'GBD', 'GBA', 'BbMxH', 'BbMxD', 'BbMxA',
    'GB>2.5', 'GB<2.5', 'B365>2.5', 'B365<2.5', 'BbMx>2.5', 'BbAv>2.5', 'BbMx<2.5', 'BbAv<2.5', 'P>2.5', 'P<2.5',
    'B365AHH', 'B365AHA', 'BbAHh', 'BbAvAHH', 'BbAvAHA', 'AHh', 'PAHH', 'PAHA',
    'NormIP_BbAvH', 'NormIP_BbAvD', 'NormIP_BbAvA',
    'NormIP_MaxH', 'NormIP_MaxD', 'NormIP_MaxA', 'NormIP_AvgH', 'NormIP_AvgD', 'NormIP_AvgA', 
    'NormIP_B365H', 'NormIP_B365D', 'NormIP_B365A', 
    'IP_AHO_AvgCAHH', 'IP_AHO_AvgCAHA', 'IP_AHO_PCAHH', 'IP_AHO_PCAHA',
]

MATCH_STATS = [
    'home_passes', 'away_passes', 'home_accurate_passes', 'away_accurate_passes', 
    'home_accurate_passes_pct', 'away_accurate_passes_pct', 
    'home_shots_off_target', 'away_shots_off_target', 
    'home_blocked_shots', 'away_blocked_shots', 
    'home_hit_woodwork', 'away_hit_woodwork',
    'home_shots_inside_box', 'away_shots_inside_box', 
    'home_shots_outside_box', 'away_shots_outside_box',
    'home_own_half', 'away_own_half', 'home_opposition_half', 'away_opposition_half',
    'home_accurate_long_balls', 'away_accurate_long_balls', 'home_accurate_long_balls_pct', 
    'away_accurate_long_balls_pct', 'home_accurate_crosses', 'away_accurate_crosses', 
    'home_accurate_crosses_pct', 'away_accurate_crosses_pct', 'home_throws', 'away_throws',
    'home_offsides', 'away_offsides', 
    'home_tackles_won', 'away_tackles_won', 'home_tackles_won_pct', 'away_tackles_won_pct', 
    'home_interceptions', 'away_interceptions', 'home_blocks', 'away_blocks', 
    'home_clearances', 'away_clearances', 'home_keeper_saves', 'away_keeper_saves', 
    'home_duels_won', 'away_duels_won', 'home_ground_duels_won', 'away_ground_duels_won', 
    'home_ground_duels_won_pct', 'away_ground_duels_won_pct', 'home_aerial_duels_won', 
    'away_aerial_duels_won', 'home_aerial_duels_won_pct', 'away_aerial_duels_won_pct', 
    'home_successful_dribbles', 'away_successful_dribbles', 'home_successful_dribbles_pct', 
    'away_successful_dribbles_pct',
]

TEAMS_STATS = [
    'HT_strength', 'HT_strength_overall_home', 'HT_strength_attack_home', 'HT_strength_defence_home',
    'HT_AvgGF_L5', 'HT_AvgGA_L5', 'HG_HT_AvgGF_L5', 'HG_HT_AvgGA_L5', 'HT_AvgShots_L5',
    'HT_ShotAccuracy_L5', 'HT_ShotConversion_L5', 'HT_CS_L5', 'HT_WinRate_L5'
]

ELO_FEATURES = ['ht_match_elo', 'at_match_elo']

MATCH_FEATURES = ['home_possession', 'away_possession', 'home_expected_goals_xg', 'away_expected_goals_xg',
                  'home_big_chances', 'away_big_chances', 'home_big_chances_missed', 'away_big_chances_missed',
                  'home_xg_open_play', 'away_xg_open_play', 'home_xg_set_play', 'away_xg_set_play', 
                  'home_non_penalty_xg', 'away_non_penalty_xg',
                  'home_touches_in_opposition_box', 'away_touches_in_opposition_box']

def merged_data_cleaning(merged_data: pd.DataFrame) -> pd.DataFrame:
    print("="*156)
    print("="*156)
    print()
    print(f"{" "*45}STARTING CLEANING, FEATURE ENGINEERING AND FEATURE REDUCTION FOR MERGED DATA!\n")
    print("Cleaning the merged data now:")
    cols_to_impute = [col for col in merged_data.columns if col.startswith(
        ('HT_GK_', 'HT_DEF_', 'HT_MID_', 'HT_FWD_', 'AT_GK_', 'AT_DEF_', 'AT_MID_', 'AT_FWD_'))] 
    merged_data[cols_to_impute] = merged_data[cols_to_impute].fillna(0)
    print(f"1. Imputed {len(cols_to_impute)} columns with 0 to handle the null values.\n")
    return merged_data

import pandas as pd

def merged_data_feature_manipulation(clean_merged_data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    print("Performing feature engineering and reduction:")
    
    # 1. REST DAYS (FATIGUE)
    clean_merged_data['Date'] = pd.to_datetime(clean_merged_data['Date'])
    clean_merged_data = clean_merged_data.sort_values(['Date'])
    
    def get_rest_days(df):
        # Create a helper to track last match date for every team
        mask = pd.concat([
            df[['Date', 'HomeTeam']].rename(columns={'HomeTeam': 'Team'}),
            df[['Date', 'AwayTeam']].rename(columns={'AwayTeam': 'Team'})
        ]).sort_values(['Team', 'Date'])
        
        mask['Last_Match'] = mask.groupby('Team')['Date'].shift(1)
        mask['Rest_Days'] = (mask['Date'] - mask['Last_Match']).dt.days.fillna(14)
        # Only clip the numeric column, not the whole dataframe
        # clipped at 14 as if rest days >= 14, it accounts for international break etc so the effect of fatigueness saturates
        mask['Rest_Days'] = mask['Rest_Days'].clip(upper=14)
        return mask

    rest_df = get_rest_days(clean_merged_data)

    # Merge carefully to avoid Date_x / Date_y issues
    clean_merged_data = clean_merged_data.merge(
        rest_df[['Date', 'Team', 'Rest_Days']], 
        left_on=['Date', 'HomeTeam'], right_on=['Date', 'Team'], how='left'
    ).rename(columns={'Rest_Days': 'HT_Rest'}).drop(columns='Team')
    
    clean_merged_data = clean_merged_data.merge(
        rest_df[['Date', 'Team', 'Rest_Days']], 
        left_on=['Date', 'AwayTeam'], right_on=['Date', 'Team'], how='left'
    ).rename(columns={'Rest_Days': 'AT_Rest'}).drop(columns='Team')
    
    clean_merged_data['Rest_Days_Diff'] = clean_merged_data['HT_Rest'] - clean_merged_data['AT_Rest']

    # 2. STRENGTH OF SCHEDULE (SoS) / AVG OPPONENT ELO
    home_side = clean_merged_data[['Date', 'HomeTeam', 'AwayTeam', 'AT_elo']].rename(
        columns={'HomeTeam': 'Team', 'AwayTeam': 'Opponent', 'AT_elo': 'Opp_Elo'}
    )
    away_side = clean_merged_data[['Date', 'AwayTeam', 'HomeTeam', 'HT_elo']].rename(
        columns={'AwayTeam': 'Team', 'HomeTeam': 'Opponent', 'HT_elo': 'Opp_Elo'}
    )
    
    all_games = pd.concat([home_side, away_side]).sort_values(['Team', 'Date'])
    all_games['Avg_Opponent_Elo_L5'] = all_games.groupby('Team')['Opp_Elo'].transform(
        lambda x: x.shift(1).rolling(window=5, min_periods=1).mean()
    )

    clean_merged_data = clean_merged_data.merge(
        all_games[['Date', 'Team', 'Avg_Opponent_Elo_L5']], 
        left_on=['Date', 'HomeTeam'], right_on=['Date', 'Team'], how='left'
    ).rename(columns={'Avg_Opponent_Elo_L5': 'HT_Avg_Opponent_Elo_L5'}).drop(columns=['Team'])

    clean_merged_data = clean_merged_data.merge(
        all_games[['Date', 'Team', 'Avg_Opponent_Elo_L5']], 
        left_on=['Date', 'AwayTeam'], right_on=['Date', 'Team'], how='left'
    ).rename(columns={'Avg_Opponent_Elo_L5': 'AT_Avg_Opponent_Elo_L5'}).drop(columns=['Team'])

    clean_merged_data['HT_Avg_Opponent_Elo_L5'] = clean_merged_data['HT_Avg_Opponent_Elo_L5'].fillna(1500)
    clean_merged_data['AT_Avg_Opponent_Elo_L5'] = clean_merged_data['AT_Avg_Opponent_Elo_L5'].fillna(1500)

    # 3. STRENGTH OF SCHEDULE NORMALIZATION
    # useful in analyzing if the home team has faced tougher or weaker opponents in the last 5 matches, compared to the away team
    clean_merged_data['SoS_Ratio'] = clean_merged_data['HT_Avg_Opponent_Elo_L5'] / clean_merged_data['AT_Avg_Opponent_Elo_L5']

    # 4. ELO QUALITY GAP
    if 'ht_match_elo' in clean_merged_data.columns and 'at_match_elo' in clean_merged_data.columns:
        clean_merged_data['Elo_Gap_Diff'] = clean_merged_data['ht_match_elo'] - clean_merged_data['at_match_elo']
        clean_merged_data['Elo_Gap_Absolute'] = clean_merged_data['Elo_Gap_Diff'].abs()

    # 5. HOME ADVANTAGE / VENUE STRENGTH
    if 'HG_HT_AvgGF_L5' in clean_merged_data.columns and 'AG_AT_AvgGF_L5' in clean_merged_data.columns:
        clean_merged_data['Venue_GF_Diff'] = clean_merged_data['HG_HT_AvgGF_L5'] - clean_merged_data['AG_AT_AvgGF_L5']
        clean_merged_data['Venue_GA_Diff'] = clean_merged_data['HG_HT_AvgGA_L5'] - clean_merged_data['AG_AT_AvgGA_L5']

    # 6. GOALKEEPER EFFICIENCY
    if 'HT_GK_L5_Avg_xgot_faced' in clean_merged_data.columns:
        ht_eff = clean_merged_data['HT_GK_L5_Avg_xgot_faced'] - clean_merged_data['HT_GK_L5_Avg_goals_conceded']
        at_eff = clean_merged_data['AT_GK_L5_Avg_xgot_faced'] - clean_merged_data['AT_GK_L5_Avg_goals_conceded']
        clean_merged_data['GK_Efficiency_Diff'] = ht_eff - at_eff

    # 7. FIELD TILT
    # accounts for territorial dominance and not just mere possession 
    ht_tilt = clean_merged_data['home_touches_in_opposition_box'].fillna(0) / (clean_merged_data['home_possession'].fillna(50) + 1)
    at_tilt = clean_merged_data['away_touches_in_opposition_box'].fillna(0) / (clean_merged_data['away_possession'].fillna(50) + 1)
    clean_merged_data['Field_Tilt_Diff'] = ht_tilt - at_tilt

    # 8. DRAW PROPENSITY FEATURES
    if 'Elo_Gap_Absolute' in clean_merged_data.columns:
        clean_merged_data['Elo_Symmetry'] = np.exp(-clean_merged_data['Elo_Gap_Absolute'] / 50)

    if all(c in clean_merged_data.columns for c in ['HT_AvgGF_L5', 'AT_AvgGF_L5', 'HT_CS_L5', 'AT_CS_L5']):
        clean_merged_data['Stalemate_Score'] = (
            (clean_merged_data['HT_CS_L5'] + clean_merged_data['AT_CS_L5']) -
            (clean_merged_data['HT_AvgGF_L5'] + clean_merged_data['AT_AvgGF_L5'])
        )

    if all(c in clean_merged_data.columns for c in ['NormIP_BbAvH', 'NormIP_BbAvD', 'NormIP_BbAvA']):
        clean_merged_data['Market_Uncertainty'] = (
            clean_merged_data['NormIP_BbAvH'] *
            clean_merged_data['NormIP_BbAvD'] *
            clean_merged_data['NormIP_BbAvA']
        )

    # 9. DIFFERENTIAL FEATURES 
    player_base_features = [
        col.replace('HT_', '') for col in clean_merged_data.columns
        if col.startswith(('HT_GK', 'HT_DEF', 'HT_MID', 'HT_FWD'))
    ]
    player_base_features = sorted(list(set(player_base_features)))

    original_cols_to_drop = []

    # Team stats diff
    for home_col in TEAMS_STATS:
        base_col = home_col.replace('HT_', '')
        away_col = f'AT_{base_col}'
        if away_col in clean_merged_data.columns:
            clean_merged_data[f'{base_col}_Diff'] = (
                clean_merged_data[home_col] - clean_merged_data[away_col]
            )
            original_cols_to_drop.extend([home_col, away_col])

    # Player stats diff
    for features in player_base_features:
        home = f'HT_{features}'
        away = f'AT_{features}'
        if home in clean_merged_data.columns and away in clean_merged_data.columns:
            clean_merged_data[f'{features}_Diff'] = (
                clean_merged_data[home] - clean_merged_data[away]
            )
            original_cols_to_drop.extend([home, away])

    # Match stats diff (FIXED NAMING)
    for idx in range(0, len(MATCH_FEATURES), 2):
        home_col = MATCH_FEATURES[idx]
        away_col = MATCH_FEATURES[idx + 1]
        base = home_col.replace('home_', '')
        new_col = f"{base}_Diff"
        clean_merged_data[new_col] = (
            clean_merged_data[home_col] - clean_merged_data[away_col]
        )
        original_cols_to_drop.extend([home_col, away_col])

    original_cols_to_drop.extend(ELO_FEATURES)
    original_cols_to_drop.extend(['HT_Rest', 'AT_Rest', 'home_xg_on_target_xgot', 'away_xg_on_target_xgot', 'xg_on_target_xgot_Diff'])

    # 10. LONG-TERM ANCHOR (Anti-Fluke)
    # Calculate average xG over 15 matches to capture the true team class over short-run form

    # Prepare home-side xG
    home_side_long = clean_merged_data[['Date', 'HomeTeam', 'home_expected_goals_xg']].rename(
        columns={
            'HomeTeam': 'Team',
            'home_expected_goals_xg': 'xG'
        }
    )

    # Prepare away-side xG
    away_side_long = clean_merged_data[['Date', 'AwayTeam', 'away_expected_goals_xg']].rename(
        columns={
            'AwayTeam': 'Team',
            'away_expected_goals_xg': 'xG'
        }
    )

    # Combine all matches into one timeline per team
    all_games_long = pd.concat([home_side_long, away_side_long]) \
        .sort_values(['Team', 'Date'])
    
    # Rolling long-term xG baseline (shifted to avoid leakage)
    all_games_long['xG_Season_Base'] = (
        all_games_long
            .groupby('Team')['xG']
            .transform(
                lambda x: x.shift(1).rolling(window=15, min_periods=1).mean()
            )
    )

    all_games_long['xG_Season_Base'] = all_games_long['xG_Season_Base'].fillna(1.2)


    # Merge back for Home Team
    clean_merged_data = clean_merged_data.merge(
        all_games_long[['Date', 'Team', 'xG_Season_Base']],
        left_on=['Date', 'HomeTeam'],
        right_on=['Date', 'Team'],
        how='left'
    ).rename(
        columns={'xG_Season_Base': 'HT_xG_Season_Base'}
    ).drop(columns=['Team'])

    # Merge back for Away Team
    clean_merged_data = clean_merged_data.merge(
        all_games_long[['Date', 'Team', 'xG_Season_Base']],
        left_on=['Date', 'AwayTeam'],
        right_on=['Date', 'Team'],
        how='left'
    ).rename(
        columns={'xG_Season_Base': 'AT_xG_Season_Base'}
    ).drop(columns=['Team'])

    # Difference in long-term season class between teams
    clean_merged_data['Season_Class_Diff'] = (
        clean_merged_data['HT_xG_Season_Base'] -
        clean_merged_data['AT_xG_Season_Base']
    )


    # ================= STABLE OFFLINE ADJUSTMENT =================

    clean_merged_data['HT_Quality_Boost'] = 1.0
    clean_merged_data['AT_Quality_Boost'] = 1.0

    if 'ht_match_elo' in clean_merged_data.columns:
        clean_merged_data['HT_Quality_Boost'] = 1.0 + (
            np.maximum(0, clean_merged_data['ht_match_elo'] - 1500) / 1000
        )
        clean_merged_data['AT_Quality_Boost'] = 1.0 + (
            np.maximum(0, clean_merged_data['at_match_elo'] - 1500) / 1000
        )

    clean_merged_data['HT_Home_Comfort'] = 1.05
    clean_merged_data['AT_Away_Resilience'] = 0.95

    if 'ht_match_elo' in clean_merged_data.columns:
        clean_merged_data.loc[
            clean_merged_data['ht_match_elo'] < 1700, 'HT_Home_Comfort'
        ] = 1.0
        clean_merged_data.loc[
            clean_merged_data['at_match_elo'] > 1900, 'AT_Away_Resilience'
        ] = 1.0

    # Ensure SoS is stable
    if 'SoS_Ratio' in clean_merged_data.columns:
        clean_merged_data['SoS_Ratio'] = clean_merged_data['SoS_Ratio'].clip(0.7, 1.3)
    else:
        clean_merged_data['SoS_Ratio'] = 1.0

    adjust_targets = [
        'expected_goals_xg',
        'big_chances',
        'touches_in_opposition_box',
        'possession'
    ]

    for base in adjust_targets:
        diff_col = f'{base}_Diff'
        h_col = f'home_{base}'
        a_col = f'away_{base}'

        if h_col in clean_merged_data.columns and a_col in clean_merged_data.columns:
            h_val = clean_merged_data[h_col] * clean_merged_data['HT_Home_Comfort']
            a_val = clean_merged_data[a_col] * clean_merged_data['AT_Away_Resilience']
            raw_diff = h_val - a_val
            boost_factor = (
                clean_merged_data['HT_Quality_Boost'] /
                clean_merged_data['AT_Quality_Boost']
            )
            clean_merged_data[diff_col] = (
                raw_diff * boost_factor * clean_merged_data['SoS_Ratio']
            )

    clean_merged_data['Quality_Index_Diff'] = clean_merged_data['expected_goals_xg_Diff']

    # # Proper clipping 
    # if 'xg_on_target_xgot_Diff' in clean_merged_data.columns:
    #     is_apex = (
    #         (clean_merged_data['ht_match_elo'] > 1875) |
    #         (clean_merged_data['at_match_elo'] > 1875)
    #     )
    #     clean_merged_data['xg_on_target_xgot_Diff'] = np.where(
    #         is_apex,
    #         clean_merged_data['xg_on_target_xgot_Diff'].clip(-4.0, 4.0),
    #         clean_merged_data['xg_on_target_xgot_Diff'].clip(-1.5, 1.5)
    #     )

    # ================= FINAL DROP =================

    original_cols_to_drop = list(set(original_cols_to_drop))
    future_cols_to_drop = RAW_STATS + ODDS + MATCH_STATS
    union_cols_to_drop = list(
        set(future_cols_to_drop).union(set(original_cols_to_drop))
    )

    data_analysis = clean_merged_data.copy()
    final_merged = clean_merged_data.drop(columns=union_cols_to_drop, errors='ignore')

    gold_check = [
        'Rest_Days_Diff', 'GK_Efficiency_Diff', 'Field_Tilt_Diff',
        'Elo_Gap_Diff', 'Elo_Symmetry', 'Stalemate_Score',
        'HT_Avg_Opponent_Elo_L5', 'AT_Avg_Opponent_Elo_L5',
        'SoS_Ratio', 'Quality_Index_Diff',
        'HT_Home_Comfort', 'AT_Away_Resilience'
    ]

    found_gold = [f for f in gold_check if f in final_merged.columns]
    print(f"GOLD FEATURES VERIFIED: {found_gold}")

    return data_analysis, final_merged