import pandas as pd
from typing import Tuple
import joblib

DROPPED_COLUMNS = [
    'FTHG', 'FTAG',
    'HS', 'AS', 'HST', 'AST', 'HC', 'AC', 'HF', 'AF', 'HY', 'AY', 'HR', 'AR', 
    'season', 'match_id', 'MatchUp', 'HT_Last_Win', 'AT_Last_Win',
    'HT_code', 'AT_code', 'HT_Points', 'AT_Points'
    # 'H2H_HT_Points_L5', 'H2H_AT_Points_L5',
    # 'HT_strength_overall_home', 'AT_strength_overall_away',
    # 'HT_strength_attack_home', 'AT_strength_attack_away',
    # 'HT_strength_defence_home', 'AT_strength_defence_away',
    # 'HG_HT_AvgGF_L5', 'HG_HT_AvgGA_L5', 'HG_HT_AvgGD_L5', 'AG_AT_AvgGF_L5', 'AG_AT_AvgGA_L5', 'AG_AT_AvgGD_L5',
    # 'HT_Encoded_Strength', 'AT_Encoded_Strength', 
    # 'GK_L5_Avg_team_goals_conceded_Diff' 
]

def data_preparation(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, pd.Series, pd.Series]:
    print("="*156)
    print("="*156)
    print()
    print(f"{" "*56}PREPARING THE DATA FOR MODEL FEEDING AND TRAINING!\n")
    classification_output = df['FTR']
    regression_output_home = df['FTHG']
    regression_output_away = df['FTAG']
    df = df.drop(columns=DROPPED_COLUMNS, errors='ignore')
    joblib.dump(df, "final_data.pkl")
    return df, classification_output, regression_output_home, regression_output_away