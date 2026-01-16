import joblib
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from typing import Any, List

OUTPUT_ARTIFACTS_DIR = 'model_artifacts'
OUTPUT_DATA_DIR = 'data_artifacts'

FEATURES = ['Date', 'HomeTeam', 'AwayTeam', 'FTR', 
            'PSH', 'PSD', 'PSA', 'Max>2.5', 'Max<2.5', 'Avg>2.5', 'Avg<2.5', 
            'MaxAHH', 'MaxAHA', 'AvgAHH', 'AvgAHA', 'MaxCH', 'MaxCD', 'MaxCA', 'B365C>2.5', 'B365C<2.5', 'MaxC>2.5', 'MaxC<2.5', 
            'B365CAHH', 'B365CAHA', 'MaxCAHH', 'MaxCAHA', 'NormIP_Margin', 'NormIP_AvgCH', 'NormIP_AvgCD', 'NormIP_AvgCA', 
            'NormIP_PSCH', 'NormIP_PSCD', 'NormIP_PSCA', 'NormIP_B365CH', 'NormIP_B365CD', 'NormIP_B365CA', 
            'NormIP_AvgC>2.5', 'NormIP_AvgC<2.5', 'NormIP_PC>2.5', 'NormIP_PC<2.5', 'Ref_Avg_Cards', 'GD_Diff_L5', 
            'Attack_Defense_L5', 'Overall_Win_Rate_L5', 'ShotConversion_Diff_L5', 'H2H_Points_Diff', 'elo_diff', 'strength_Diff', 
            'AvgGF_L5_Diff', 'AvgGA_L5_Diff', 'AvgShots_L5_Diff', 'ShotAccuracy_L5_Diff', 'ShotConversion_L5_Diff', 'CS_L5_Diff', ''
            'WinRate_L5_Diff', 'DEF_L5_Avg_accurate_long_balls_Diff', 'DEF_L5_Avg_accurate_passes_Diff', 
            'DEF_L5_Avg_aerial_duels_won_Diff', 'DEF_L5_Avg_blocks_Diff', 'DEF_L5_Avg_clearances_Diff', 
            'DEF_L5_Avg_dribbled_past_Diff', 'DEF_L5_Avg_duels_won_Diff', 'DEF_L5_Avg_final_third_passes_Diff', 
            'DEF_L5_Avg_fouls_committed_Diff', 'DEF_L5_Avg_ground_duels_won_Diff', 'DEF_L5_Avg_headed_clearances_Diff', 
            'DEF_L5_Avg_interceptions_Diff', 'DEF_L5_Avg_recoveries_Diff', 'DEF_L5_Avg_tackles_won_Diff', 
            'DEF_L5_Avg_tackles_won_percentage_Diff', 'DEF_L5_Avg_was_fouled_Diff', 'DEF_L5_Avg_xa_Diff', 'DEF_L5_Avg_xg_Diff', 
            'FWD_L5_Avg_accurate_passes_Diff', 'FWD_L5_Avg_aerial_duels_won_Diff', 'FWD_L5_Avg_assists_Diff', 
            'FWD_L5_Avg_big_chances_missed_Diff', 'FWD_L5_Avg_chances_created_Diff', 'FWD_L5_Avg_corners_Diff', 
            'FWD_L5_Avg_duels_won_Diff', 'FWD_L5_Avg_final_third_passes_Diff', 'FWD_L5_Avg_fouls_committed_Diff', 
            'FWD_L5_Avg_goals_Diff', 'FWD_L5_Avg_ground_duels_won_Diff', 'FWD_L5_Avg_offsides_Diff', 'FWD_L5_Avg_penalties_missed_Diff', 
            'FWD_L5_Avg_penalties_scored_Diff', 'FWD_L5_Avg_shots_on_target_Diff', 'FWD_L5_Avg_successful_dribbles_Diff', 
            'FWD_L5_Avg_total_shots_Diff', 'FWD_L5_Avg_touches_Diff', 'FWD_L5_Avg_touches_opposition_box_Diff', 
            'FWD_L5_Avg_was_fouled_Diff', 'FWD_L5_Avg_xa_Diff', 'FWD_L5_Avg_xg_Diff', 'FWD_L5_Avg_xgot_Diff', 
            'GK_L5_Avg_gk_accurate_long_balls_Diff', 'GK_L5_Avg_gk_accurate_passes_Diff', 'GK_L5_Avg_goals_conceded_Diff', 
            'GK_L5_Avg_goals_prevented_Diff', 'GK_L5_Avg_high_claim_Diff', 'GK_L5_Avg_saves_Diff', 'GK_L5_Avg_saves_inside_box_Diff', 
            'GK_L5_Avg_sweeper_actions_Diff', 'GK_L5_Avg_xgot_faced_Diff', 'MID_L5_Avg_accurate_crosses_Diff', 
            'MID_L5_Avg_accurate_long_balls_Diff', 'MID_L5_Avg_accurate_passes_Diff', 'MID_L5_Avg_aerial_duels_won_Diff', 
            'MID_L5_Avg_assists_Diff', 'MID_L5_Avg_blocks_Diff', 'MID_L5_Avg_chances_created_Diff', 'MID_L5_Avg_clearances_Diff', 
            'MID_L5_Avg_corners_Diff', 'MID_L5_Avg_dribbled_past_Diff', 'MID_L5_Avg_duels_won_Diff', 'MID_L5_Avg_final_third_passes_Diff', 
            'MID_L5_Avg_fouls_committed_Diff', 'MID_L5_Avg_goals_Diff', 'MID_L5_Avg_ground_duels_won_Diff', 'MID_L5_Avg_interceptions_Diff', 
            'MID_L5_Avg_penalties_missed_Diff', 'MID_L5_Avg_penalties_scored_Diff', 'MID_L5_Avg_recoveries_Diff', 'MID_L5_Avg_shots_on_target_Diff', 
            'MID_L5_Avg_successful_dribbles_Diff', 'MID_L5_Avg_tackles_won_Diff', 'MID_L5_Avg_total_shots_Diff', 'MID_L5_Avg_touches_Diff', 
            'MID_L5_Avg_was_fouled_Diff', 'MID_L5_Avg_xa_Diff', 'MID_L5_Avg_xg_Diff', 'possession_Diff', 'expected_goals_Diff', 
            'big_chances_Diff', 'big_chances_missed_Diff', 'xg_open_play_Diff', 'xg_set_play_Diff', 'non_penalty_Diff', 
            'xg_on_targetot_Diff', 'touches_in_opposition_box_Diff']

def save_model_artifacts(xgb_model: Any, rfr_home: Any, rfr_away: Any, scaler: StandardScaler, output_dir: str = OUTPUT_ARTIFACTS_DIR):
    print("="*156)
    print("="*156)
    print(f"\n{" "*60}SAVING ALL THE MODEL ARTIFACTS NOW!\n")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    try:
        joblib.dump(xgb_model, os.path.join(output_dir, 'xgb_model1.joblib'))
        print("XGBoost model saved successfully!\n")
        joblib.dump(rfr_home, os.path.join(output_dir, 'rfr_home1.joblib'))
        print("RFR Home model saved successfully!\n")
        joblib.dump(rfr_away, os.path.join(output_dir, 'rfr_away1.joblib'))
        print("RFR Away model saved successfully!\n")
        joblib.dump(scaler, os.path.join(output_dir, 'scaler1.joblib'))
        print("Scaler saved successfully!\n")
    except Exception as e:
        print(f"Error: {e}\n")
    print(f"{" "*53}ALL THE MODEL ARTIFACTS HAVE BEEN SAVED SUCCESSFULLY!\n")

def save_data_artifact(df: pd.DataFrame, features: List[str] , output_dir: str = OUTPUT_DATA_DIR):
    print("="*156)
    print("="*156)  
    print(f"{" "*65}SAVING THE MASTER DATA NOW!\n")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    try:
        joblib.dump(df, os.path.join(output_dir, 'master_data.pkl'))
        joblib.dump(features, os.path.join(output_dir, 'final_features.pkl'))
    except Exception as e:
        print(f"Error: {e}\n")
    print(f"{" "*51}MASTER DATA AND FINAL FEATURE LIST HAS BEEN SUCCESSFULLY SAVED!\n")

def save_transformed_data_artifact(df: pd.DataFrame, features: List[str] , output_dir: str = OUTPUT_DATA_DIR):
    print("="*156)
    print("="*156)  
    print(f"{" "*65}SAVING THE MASTER DATA NOW!\n")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    try:
        joblib.dump(df, os.path.join(output_dir, 'master_data_transformed.pkl'))
        joblib.dump(features, os.path.join(output_dir, 'final_features.pkl'))
    except Exception as e:
        print(f"Error: {e}\n")
    print(f"{" "*51}MASTER TRANSFORMED DATA AND FINAL FEATURE LIST HAS BEEN SUCCESSFULLY SAVED!\n")