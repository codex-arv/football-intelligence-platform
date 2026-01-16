import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import os

# Paths (adjust if different)
MODEL_PATH = 'model_artifacts/xgb_model1.joblib'
DATA_PATH = 'data_artifacts/master_data.pkl'

def run_model_audit():
    print("--- 1. LOAD DATA & MODEL ---")
    if not os.path.exists(MODEL_PATH):
        print("Model file not found!")
        return
        
    model = joblib.load(MODEL_PATH)
    # Your live script variables should be initialized before running this
    # Assuming load_assets() or similar has been called.
    
    print(f"Model Class: {type(model)}")
    
    print("\n--- 2. CHECK FEATURE IMPORTANCE (The 'Gold' Check) ---")
    # This tells us if your new features (Stalemate, Elo Symmetry) are actually being used
    if hasattr(model, 'feature_importances_'):
        importances = pd.Series(model.feature_importances_, index=joblib.load('data_artifacts/final_features.pkl'))
        print("Top 10 Most Influential Features:")
        print(importances.sort_values(ascending=False).head(10))
    
    print("\n--- 3. LIVE PIPELINE SMOKE TEST ---")
    # Let's test a specific high-profile match to see if the logic holds
    # Replace these with teams actually in your MASTER_DATA
    test_teams = [("Brentford", "Man City"), ("Aston Villa", "Chelsea")]
    
    for home, away in test_teams:
        try:
            from live_feature_calculation import predict_match, load_data_once, load_model_once
            load_data_once()
            load_model_once()
            
            res = predict_match(home, away)
            print(f"\nLive Simulation [{home} vs {away}]:")
            print(f"  -> Scoreline: {res['scoreline']}")
            print(f"  -> Original Winner: {res['predicted_winner_original']} ({res['confidence_level_original']})")
            print(f"  -> Blended Winner: {res['predicted_winner_blended']}")
        except Exception as e:
            print(f"  -> Simulation failed for {home} vs {away}: {e}")

    print("\n--- 4. DATA CONSISTENCY CHECK ---")
    df = joblib.load(DATA_PATH)
    latest_date = pd.to_datetime(df['Date']).max()
    print(f"Latest match in dataset: {latest_date}")
    print(f"Total records available: {len(df)}")

if __name__ == "__main__":
    run_model_audit()