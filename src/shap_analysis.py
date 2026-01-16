import pandas as pd
import numpy as np
import joblib
import shap 
import os
import matplotlib.pyplot as plt

# Import your live logic (Ensure the filename matches your actual live script file)
from live_feature_calculation import calculate_features, MODELS, load_model_once, load_data_once

def debug_match_features(home_team: str, away_team: str):
    # 1. Initialize
    print("="*80)
    print(f"SHAP DEBUGGER: {home_team} vs {away_team}")
    print("="*80)
    print("--- Loading Data and Models ---")
    load_data_once()
    load_model_once()
    
    # Import the actual FEATURE_LIST from the live module
    import live_feature_calculation
    local_feature_list = live_feature_calculation.FEATURE_LIST
    
    if len(local_feature_list) == 0:
        local_feature_list = joblib.load('data_artifacts/final_features.pkl')

    # 2. Generate the live feature row (This now includes SoS and Season Anchors)
    X_live = calculate_features(home_team, away_team)
    
    # Ensure columns match the FEATURE_LIST exactly for the model
    X_live = X_live[local_feature_list]
    
    model = MODELS['classification_model']
    scaler = MODELS.get('scaler')
    
    # We must scale the features because the model was trained on scaled data
    X_live_scaled = pd.DataFrame(scaler.transform(X_live), columns=X_live.columns) if scaler else X_live
    
    print(f"\n--- Contextual Feature Values ---")
    relevant_cols = ['SoS_Ratio', 'Quality_Index_Diff', 'Season_Class_Diff', 'Elo_Gap_Diff']
    for col in relevant_cols:
        if col in X_live.columns:
            print(f"{col}: {X_live.iloc[0][col]:.4f}")

    # 3. SHAP Analysis
    print("\n--- Calculating SHAP Impact (The 'Why') ---")
    # Use the TreeExplainer for XGBoost
    explainer = shap.TreeExplainer(model)
    
    # Get SHAP values for the scaled input
    shap_results = explainer.shap_values(X_live_scaled)
    
    # Logic to handle XGBoost multi-class output versions
    # Class 0: Away, Class 1: Draw, Class 2: Home
    if isinstance(shap_results, list):
        # Older XGBoost versions return a list of arrays
        impact_data = shap_results[2][0] 
    elif len(shap_results.shape) == 3:
        # Newer versions return (samples, features, classes)
        impact_data = shap_results[0, :, 2] 
    else:
        # Single output/binary fallback
        impact_data = shap_results[0]

    impact_series = pd.Series(impact_data, index=local_feature_list)
    
    print(f"\n--- Top 10 Features DRIVING the prediction toward {home_team} ---")
    print(impact_series.sort_values(ascending=False).head(10))
    
    print(f"\n--- Top 10 Features PREVENTING {home_team} from winning ---")
    print(impact_series.sort_values(ascending=True).head(10))

# -----------------------------
# 🚀 THE FIX: Reality Calibration
# -----------------------------
def apply_tier_calibration(probs: dict, home_team: str, away_team: str) -> dict:
    """
    Manually dampens unrealistic confidence when a Tier 2 team plays a Tier 1 team.
    This acts as a safety net if the SoS normalization isn't aggressive enough.
    """
    big_six = ['Man City', 'Arsenal', 'Liverpool', 'Chelsea', 'Man United', 'Tottenham']
    
    # Calibration: If a non-Big Six team shows massive confidence against a Giant
    if away_team in big_six and home_team not in big_six:
        if probs['home_win'] > 0.65:
            print(f"⚠️ Calibrating unrealistic confidence: {home_team} vs {away_team}")
            excess = probs['home_win'] - 0.65
            probs['home_win'] = 0.65
            # Distribute the excess probability to Draw and Away Win
            probs['draw'] += excess * 0.4
            probs['away_win'] += excess * 0.6
            
    return probs

if __name__ == "__main__":
    # Test on the specific Brentford/City outlier
    debug_match_features("Brentford", "Man City")