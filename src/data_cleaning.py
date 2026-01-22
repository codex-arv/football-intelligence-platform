# this file is responsible for data cleaning: handling null values (eliminating, median & 0 imputation)

import pandas as pd
from typing import Dict

# used in feature_engineering_ewma.py
def data_cleaning(df: pd.DataFrame) -> pd.DataFrame:

    # stage-1: eliminate columns having >90% null values in the dataset
    rows = df.shape[0]
    threshold = 0.90
    null_columns: Dict[str, int] = dict(df.isnull().sum())
    must_delete_columns = {key: value for key, value in null_columns.items() if value > (threshold * rows)}
    print(f"Stage 1 completed: Dropped {len(must_delete_columns)} columns with greater than {int(threshold*100)}% null values.")
    df_stage1 = df.drop(columns=list(must_delete_columns.keys()), axis=1, errors='ignore')
    
    # stage-2: certain specific columns having <90% null values are imputed with the median value of that column
    df_stage2 = df_stage1.copy()
    after_stage1_null_columns = dict(df_stage1.isnull().sum())
    imputable_columns = {key: value for key, value in after_stage1_null_columns.items() if value < (threshold * rows) and value != 0}
    fixed_cols = ['Date', 'HomeTeam', 'AwayTeam', 'Referee', 'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HTR']
    exclude_cols = fixed_cols + [col for col in df_stage2.columns if col.startswith(('HT_', 'AT_', 'HG_', 'AG_'))]
    impute_count = 0
    for col in list(imputable_columns.keys()):
        if col not in exclude_cols: 
            df_stage2[col] = df_stage2[col].fillna(df_stage2[col].median())
            impute_count += 1
    print(f"Stage 2 completed: Imputed {impute_count} columns with their median values")
    
    # stage-3: remaining rolling columns were imputed with a safe 0 value
    after_stage2_null_columns = dict(df_stage2.isnull().sum())
    rolling_columns = {key: value for key, value in after_stage2_null_columns.items() if value > 0}
    df_stage3 = df_stage2.copy()
    for col in rolling_columns:
        df_stage3[col] = df_stage3[col].fillna(0)
    print(f"Stage 3 completed: Imputed {len(rolling_columns)} columns (rolling features) with 0")
    cleaned_df = df_stage3.dropna(how='any')

    return cleaned_df

    





