import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import mean_absolute_error, r2_score
import live_feature_calculation as lfc

def audit_regressors():
    lfc.load_data_once()
    lfc.load_model_once()
    
    # 1. Get the actual historical matches
    df = lfc.MAIN_DF.copy()
    
    print(f"Analyzing {len(df)} historical matches...")
    
    # 2. Reconstruct the features for every match in history
    # This ensures columns like 'Elo_Gap_Diff' and 'SoS_Ratio' are created
    processed_rows = []
    actual_h_goals = []
    actual_a_goals = []
    
    # We skip the very beginning of the dataset because they won't have 15-match histories
    for i in range(50, len(df)):
        row = df.iloc[i]
        h_team = row['HomeTeam']
        a_team = row['AwayTeam']
        
        # Capture actual scores (adjust 'FTHG' if your column name is different)
        actual_h_goals.append(row['FTHG'])
        actual_a_goals.append(row['FTAG'])
        
        # Calculate features exactly like we do for a live match
        # We use a subset of MAIN_DF up to this date to avoid data leakage
        temp_main = lfc.MAIN_DF
        lfc.MAIN_DF = df.iloc[:i] # Only look at matches BEFORE this one
        
        X_feature_row = lfc.calculate_features(h_team, a_team)
        processed_rows.append(X_feature_row)
        
        lfc.MAIN_DF = temp_main # Restore
        
        if i % 100 == 0:
            print(f"Processed {i} matches...")

    # 3. Combine processed rows into a single matrix
    X_all = pd.concat(processed_rows, ignore_index=True)
    y_h = np.array(actual_h_goals)
    y_a = np.array(actual_a_goals)

    # 4. Scale and Predict
    scaler = lfc.MODELS.get('scaler')
    X_scaled = pd.DataFrame(scaler.transform(X_all), columns=lfc.FEATURE_LIST) if scaler else X_all
    
    pred_h = lfc.MODELS['regression_home_model'].predict(X_scaled)
    pred_a = lfc.MODELS['regression_away_model'].predict(X_scaled)

    # 5. Output Results
    print(f"\n--- RECONSTRUCTED AUDIT RESULTS ---")
    print(f"Home MAE: {mean_absolute_error(y_h, pred_h):.3f}")
    print(f"Home R2:  {r2_score(y_h, pred_h):.3f}")
    print(f"Away MAE: {mean_absolute_error(y_a, pred_a):.3f}")
    print(f"Away R2:  {r2_score(y_a, pred_a):.3f}")

if __name__ == "__main__":
    audit_regressors()