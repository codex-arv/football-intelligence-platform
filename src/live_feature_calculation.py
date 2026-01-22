import math
import numpy as np
import pandas as pd
import os
import joblib
import time
from typing import List, Tuple, Dict, Union

# -----------------------------
# Configuration & Globals
# -----------------------------
MODEL_ARTIFACTS = 'model_artifacts'
DATA_ARTIFACTS = 'data_artifacts'
MASTER_DATA = 'master_data_transformed.pkl'
FINAL_FEATURES = 'final_features.pkl'

MAIN_DF: pd.DataFrame = pd.DataFrame()
FEATURE_LIST: List[str] = []
MODELS: Dict[str, any] = {}
LABELS = ['Away Win', 'Draw', 'Home Win']

# -----------------------------
# Column Renaming Map
# -----------------------------
RENAME_MAP = {
    'home_possession': 'HT_possession',
    'away_possession': 'AT_possession',
    'home_expected_goals_xg': 'HT_expected_goals',
    'away_expected_goals_xg': 'AT_expected_goals',
    'home_big_chances': 'HT_big_chances',
    'away_big_chances': 'AT_big_chances',
    'home_touches_in_opposition_box': 'HT_touches_in_opposition_box',
    'away_touches_in_opposition_box': 'AT_touches_in_opposition_box',
}

# -----------------------------
# Core Probability Math
# -----------------------------
def poisson_prob(lmbda: float, k: int) -> float:
    if lmbda <= 0: return 1.0 if k == 0 else 0.0
    return math.exp(-lmbda) * (lmbda ** k) / math.factorial(k)

def regression_to_outcome_prob(home_xg: float, away_xg: float, max_goals: int = 10) -> Dict[str, float]:
    home_win, draw, away_win = 0.0, 0.0, 0.0
    h_lambda = max(0, home_xg)
    a_lambda = max(0, away_xg)
    
    for i in range(max_goals + 1):
        p_h = poisson_prob(h_lambda, i)
        for j in range(max_goals + 1):
            p = p_h * poisson_prob(a_lambda, j)
            if i > j: home_win += p
            elif i == j: draw += p
            else: away_win += p
    return {"home_win": home_win, "draw": draw, "away_win": away_win}

def blend_probabilities(class_probs: Dict[str, float], reg_probs: Dict[str, float], weight_class: float, 
                        mode: str = "UNKNOWN") -> Dict[str, float]:
    weight_reg = 1 - weight_class
    blended = {
        "home_win": class_probs["home_win"] * weight_class + reg_probs["home_win"] * weight_reg,
        "draw": class_probs["draw"] * weight_class + reg_probs["draw"] * weight_reg,
        "away_win": class_probs["away_win"] * weight_class + reg_probs["away_win"] * weight_reg,
    }

    # SHARPENING: Use a lower T (more aggressive) for elite teams or mismatches
    # T=0.6 makes the leader MUCH more prominent
    if mode == "ELITE":
        T = 0.8
    elif mode == "MISMATCH":
        T = 0.9
    elif mode == "GRIND":
        T = 0.7
    else: T = 1
    
    keys = list(blended.keys())
    vals = np.array([blended[k] for k in keys]) + 1e-9
    log_p = np.log(vals)
    sharpened = np.exp(log_p / T)
    sharpened /= sharpened.sum()
    print(f"Temperature = {T}")

    return dict(zip(keys, sharpened))

# -----------------------------
# Data & Model Loaders
# -----------------------------
def load_data_once():
    global MAIN_DF, FEATURE_LIST
    if not MAIN_DF.empty and FEATURE_LIST:
        return
    
    data_path = os.path.join(DATA_ARTIFACTS, MASTER_DATA)
    features_path = os.path.join(DATA_ARTIFACTS, FINAL_FEATURES)
    
    if not os.path.exists(data_path) or not os.path.exists(features_path):
        raise FileNotFoundError("Critical data artifacts missing in data_artifacts folder.")

    df = joblib.load(data_path)
    df = df.rename(columns=RENAME_MAP)
    # Clean special characters from column names to match training
    df.columns = [c.replace('>', '_GT_').replace('<', '_LT_').replace('.', '_') for c in df.columns]
    
    # Crucial: Fix date types to prevent infinite loading hangs
    df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
    MAIN_DF = df.sort_values('Date').reset_index(drop=True)
    FEATURE_LIST = joblib.load(features_path)

def load_model_once():
    global MODELS
    if MODELS: return
    model_dict = {
        'classification_model': os.path.join(MODEL_ARTIFACTS, 'xgb_model1.joblib'),
        'regression_home_model': os.path.join(MODEL_ARTIFACTS, 'rfr_home1.joblib'),
        'regression_away_model': os.path.join(MODEL_ARTIFACTS, 'rfr_away1.joblib'),
        'scaler': os.path.join(MODEL_ARTIFACTS, 'scaler1.joblib'),
    }
    for name, path in model_dict.items():
        if os.path.exists(path):
            MODELS[name] = joblib.load(path)
        else:
            print(f"Warning: Model file {path} not found.")

# -----------------------------
# API Helper Functions
# -----------------------------
def get_all_teams() -> List[str]:
    load_data_once()
    if MAIN_DF.empty: return []
    teams = pd.concat([MAIN_DF['HomeTeam'], MAIN_DF['AwayTeam']]).unique()
    return sorted(teams.tolist())

def get_base_features() -> Tuple[List[str], List[str]]:
    diff_features = [col for col in FEATURE_LIST if col.endswith('_Diff')]
    base_names = [col.replace('_Diff', '') for col in diff_features]
    static_features = [col for col in FEATURE_LIST if not col.endswith('_Diff')]
    return sorted(list(set(base_names))), static_features

# -----------------------------
# Internal Feature Extractors
# -----------------------------
def _get_historical_series(team: str, col_name: str, window: int) -> float:
    mask = (MAIN_DF['HomeTeam'] == team) | (MAIN_DF['AwayTeam'] == team)
    team_data = MAIN_DF[mask].tail(window)
    if team_data.empty: return 0.0
    vals = np.where(team_data['HomeTeam'] == team, team_data[f'HT_{col_name}'], team_data[f'AT_{col_name}'])
    return float(np.nanmean(vals))

def _get_rolling_team_stats(team: str, base_features: List[str], window: int = 8) -> Dict[str, float]:
    mask = (MAIN_DF['HomeTeam'] == team) | (MAIN_DF['AwayTeam'] == team)
    team_history = MAIN_DF[mask].tail(window)
    if team_history.empty: return {base: 0.0 for base in base_features}
    
    is_home = (team_history['HomeTeam'] == team).values
    stats = {}
    for base in base_features:
        h_col, a_col = f'HT_{base}', f'AT_{base}'
        if h_col in team_history.columns and a_col in team_history.columns:
            vals = np.where(is_home, team_history[h_col].values, team_history[a_col].values)
            stats[base] = float(np.nanmean(vals))
        else:
            stats[base] = 0.0
    return stats

def _get_ewma_team_stats(team: str, base_features: List[str], span: int = 15) -> Dict[str, float]:
    # We pull 7 games to ensure the EWMA calculation has enough historical 'momentum'
    mask = (MAIN_DF['HomeTeam'] == team) | (MAIN_DF['AwayTeam'] == team)
    team_history = MAIN_DF[mask].tail(10)
    
    if team_history.empty:
        return {base: 0.0 for base in base_features}
    
    is_home = (team_history['HomeTeam'] == team).values
    stats = {}
    
    for base in base_features:
        h_col, a_col = f'HT_{base}', f'AT_{base}'
        if h_col in team_history.columns and a_col in team_history.columns:
            # Create a single chronological series of the team's performance
            vals = pd.Series(np.where(is_home, team_history[h_col].values, team_history[a_col].values))
            # Calculate Exponential Weighted Moving Average
            # Using adjust=True ensures that we account for the relative weight of the start of the series
            stats[base] = float(vals.ewm(span=span, adjust=True).mean().iloc[-1])
        else:
            stats[base] = 0.0
            
    return stats

def _get_latest_metadata(team: str) -> Tuple[pd.Series, str]:
    mask = (MAIN_DF['HomeTeam'] == team) | (MAIN_DF['AwayTeam'] == team)
    team_history = MAIN_DF[mask]
    if team_history.empty: raise ValueError(f"No metadata for team: {team}")
    latest_row = team_history.iloc[-1]
    prefix = 'HT_' if latest_row['HomeTeam'] == team else 'AT_'
    return latest_row, prefix

def get_venue_performance_mod(home_team, away_team):
    h_row, h_pre = _get_latest_metadata(home_team)
    a_row, a_pre = _get_latest_metadata(away_team)
    
    h_elo = float(h_row.get(f'{h_pre}elo', 1500))
    a_elo = float(a_row.get(f'{a_pre}elo', 1500))
    elo_diff = h_elo - a_elo

    # 1. JUGGERNAUT PRIORITY (Elo >= 2000)
    # Use if/if here so BOTH can be boosted if both are elite
    h_mod, a_mod = 1.0, 1.0
    is_juggernaut = False

    if h_elo >= 2000:
        h_mod = 1.15
        is_juggernaut = True
    if a_elo >= 2000:
        a_mod = 1.05
        is_juggernaut = True

    # If a juggernaut is involved, we RETURN NOW so lower logic doesn't overwrite
    if is_juggernaut:
        return h_mod, a_mod

    # 2. HEAVY MISMATCH (Only if no juggernaut)
    if abs(elo_diff) > 175:
        if elo_diff > 175:
            h_mod, a_mod = 1.0, 0.95
        else:
            h_mod, a_mod = 1.0, 1.05
            
    # 3. ELITE PROTECTION (Elo > 1875)
    elif h_elo > 1875 or a_elo > 1875:
        if h_elo > 1875: h_mod = 1.05
        if a_elo > 1875: a_mod = 1.0

    # 4. FINAL SAFETY (Only for mid/low tier games)
    elif h_elo < 1775 and a_elo > 1775:
        a_mod = 1.05
    elif a_elo < 1775 and h_elo > 1775:
        a_mod = 0.90

    return h_mod, a_mod

# -----------------------------
# Main Calculation Logic
# -----------------------------

def compute_dynamic_weight(home_elo: float, away_elo: float) -> Tuple[float, str]:
    """
    Computes blending weight dynamically based on Elo and match context.
    Prioritizes mismatch > elite duel > balanced game.
    """
    elo_diff = abs(home_elo - away_elo)
    elite_threshold = 1875
    mismatch_threshold = 150

    # 1. Heavy mismatch first
    if elo_diff > mismatch_threshold:
        mode = "MISMATCH"
        weight_class = 0.45
    # 2. Elite duel (both teams elite)
    elif home_elo > elite_threshold and away_elo > elite_threshold:
        mode = "ELITE"
        weight_class = 0.35
    # 3. Otherwise balanced / grind
    else:
        mode = "GRIND"
        weight_class = 0.55

    return weight_class, mode


def calculate_features(home_team: str, away_team: str) -> pd.DataFrame:
    load_data_once()
    base_columns, static_features = get_base_features()
    feature_dict = {col: 0.0 for col in FEATURE_LIST}

    # 1. Load Data for both teams using EWMA (Span 10)
    h_stats = _get_ewma_team_stats(home_team, base_columns, span=15)
    a_stats = _get_ewma_team_stats(away_team, base_columns, span=15)
    h_row, h_pre = _get_latest_metadata(home_team)
    a_row, a_pre = _get_latest_metadata(away_team)

    # 2. Extract Elo and Strength of Schedule (SoS)
    h_elo = float(h_row.get(f'{h_pre}elo', 1500))
    a_elo = float(a_row.get(f'{a_pre}elo', 1500))
    h_opp_elo = h_row.get(f'{h_pre}Avg_Opponent_Elo_L5', 1500)
    a_opp_elo = a_row.get(f'{a_pre}Avg_Opponent_Elo_L5', 1500)
    
    sos_ratio = float(h_opp_elo) / float(a_opp_elo) if a_opp_elo > 0 else 1.0
    h_boost = 1.0 + (max(0, h_elo - 1500) / 1000)
    a_boost = 1.0 + (max(0, a_elo - 1500) / 1000)

    # 3. Apply EWMA Stats Differences with Quality Adjustments
    # Unified Adjustment Loop (Venue -> Difference -> Quality)
    adjust_targets = ['touches_in_opposition_box', 'expected_goals', 'big_chances', 'possession']
    h_mod, a_mod = get_venue_performance_mod(home_team, away_team)

    for base in base_columns:
        diff_key = f"{base}_Diff"
        if diff_key in feature_dict:
            h_val = h_stats.get(base, 0.0)
            a_val = a_stats.get(base, 0.0)

            if base.lower() in adjust_targets:
                # Apply our stable venue modifiers
                h_val *= h_mod
                a_val *= a_mod
            
            raw_diff = h_val - a_val

            # SOS and QUALITY are the 'Long Term' anchors. Keep these!
            if base.lower() in adjust_targets:
                raw_diff *= sos_ratio
                # This ensures quality (Elo) is the multiplier, not the venue.
                raw_diff *= (h_boost / a_boost)
                
            feature_dict[diff_key] = raw_diff

    # 4. CRITICAL: Pass the "Context" features to the model
    feature_dict['HT_Home_Comfort'] = h_mod
    feature_dict['AT_Away_Resilience'] = a_mod

    # 4. Correct Static Feature Handling (The primary fix for the Draw Trap)
    for col in static_features:
        if feature_dict.get(col, 0.0) == 0.0:
            # If the feature is team-specific (like elo, rating, or season points)
            # we must provide the DIFFERENCE. If it's neutral (like league ID), use Home val.
            h_val = h_row.get(f'{h_pre}{col}', h_row.get(col, 0.0))
            a_val = a_row.get(f'{a_pre}{col}', a_row.get(col, 0.0))
            
            if isinstance(h_val, (int, float, np.number)):
                feature_dict[col] = float(h_val) - float(a_val)
            else:
                feature_dict[col] = h_val

    # 5. Derived "Gold" Features
    feature_dict['SoS_Ratio'] = sos_ratio
    feature_dict['Elo_Gap_Diff'] = h_elo - a_elo
    feature_dict['Elo_Gap_Absolute'] = abs(h_elo - a_elo)
    feature_dict['Elo_Symmetry'] = np.exp(-abs(h_elo - a_elo) / 50)
    
    h_xg_season = _get_historical_series(home_team, 'expected_goals', 12)
    a_xg_season = _get_historical_series(away_team, 'expected_goals', 12)
    feature_dict['HT_xG_Season_Base'] = h_xg_season
    feature_dict['AT_xG_Season_Base'] = a_xg_season
    feature_dict['Season_Class_Diff'] = h_xg_season - a_xg_season
    
    # 6. Date Logic
    today = pd.Timestamp.now().tz_localize(None)
    h_last_date = h_row['Date']
    a_last_date = a_row['Date']
    feature_dict['Rest_Days_Diff'] = min(14, (today - h_last_date).days) - min(14, (today - a_last_date).days)
    
    feature_dict['Quality_Index_Diff'] = feature_dict.get('expected_goals_Diff', 0.0)
    
    # 7. Scaling Clamps
    # Clamping prevents extreme outliers but allows elite teams to stand out
    # clip_val = 4 if (h_elo > 1875 or a_elo > 1875) else 1.5
    # for col in ['xg_on_targetot_Diff']:
    #     if col in feature_dict:
    #         feature_dict[col] = np.clip(feature_dict[col], -clip_val, clip_val)

    # 8. Final DataFrame Assembly
    final_df = pd.DataFrame([feature_dict])
    
    # Ensure all columns exist and are in the correct order for the model
    for col in FEATURE_LIST:
        if col not in final_df.columns:
            final_df[col] = 0.0
            
    return final_df[FEATURE_LIST].fillna(0.0)

# -----------------------------
# Public API Entry Point
# -----------------------------

def predict_match(home: str, away: str) -> Dict[str, Union[str, float, Dict[str, float]]]:
    load_model_once()
    load_data_once()

    # 1. Detect Elite/Mismatch
    h_row, h_pre = _get_latest_metadata(home)
    a_row, a_pre = _get_latest_metadata(away)
    h_elo_raw = h_row.get(f'{h_pre}elo', 1500)
    a_elo_raw = a_row.get(f'{a_pre}elo', 1500)

    h_elo = float(h_elo_raw)
    a_elo = float(a_elo_raw)

    # --- SMART WEIGHTING SYSTEM ---
    avg_elo = (h_elo + a_elo) / 2
    elo_diff = abs(h_elo - a_elo) 
    
    X_live = calculate_features(home, away)

    # ------------------ CRITICAL FEATURE ALIGNMENT ------------------

    # 1. Add any missing columns
    for col in FEATURE_LIST:
        if col not in X_live.columns:
            X_live[col] = 0.0

    # 2. Remove extra columns
    X_live = X_live[FEATURE_LIST]

    # 3. Enforce float type (very important for scaler consistency)
    X_live = X_live.astype(float)

    # ------------------ SCALING ------------------
    scaler = MODELS.get('scaler')
    X_live_scaled = pd.DataFrame(
        scaler.transform(X_live),
        columns=FEATURE_LIST
    ) if scaler else X_live


    # 3. Classification Path
    c_model = MODELS['classification_model']
    c_probs = c_model.predict_proba(X_live_scaled)[0]
    class_probs_dict = {"away_win": float(c_probs[0]), "draw": float(c_probs[1]), "home_win": float(c_probs[2])}

    # 4. Regression Path
    h_goals = MODELS['regression_home_model'].predict(X_live_scaled)[0]
    a_goals = MODELS['regression_away_model'].predict(X_live_scaled)[0]
    reg_probs = regression_to_outcome_prob(h_goals, a_goals)

    # 5. Logic Evaluation
    elo_diff = abs(h_elo - a_elo)
    is_mismatch = abs(elo_diff) > 150
    is_elite = (h_elo > 1875) or (a_elo > 1875)

    # DEBUG PRINT: This will show you why the weight is failing
    print(f"{home} : ({h_elo}) vs {away} : ({a_elo}) ||| ELO DIFF = {elo_diff}")
    print(f"Elite: {is_elite}, Mismatch: {is_mismatch}")
    weight_class, mode = compute_dynamic_weight(h_elo, a_elo)

    blended_probs = blend_probabilities(
        class_probs_dict, reg_probs,
        weight_class=weight_class,
        mode=mode
    )
    print(f"Mode: {mode} | Weight: {weight_class}")

    # 4. Final Decision
    final_label = max(blended_probs, key=blended_probs.get)
    winner_blended = away if final_label == "away_win" else home if final_label == "home_win" else "Draw"

    return {
        "home_team": home,
        "away_team": away,
        "scoreline": f"{round(max(0, h_goals))} - {round(max(0, a_goals))}",
        "raw_scoreline": f"{h_goals:.2f} - {a_goals:.2f}",
        "predicted_winner_original": LABELS[np.argmax(c_probs)],
        "confidence_level_original": f"{np.max(c_probs):.3%}",
        "probabilities_original": class_probs_dict,
        "regression_probabilities": reg_probs,
        "blended_probabilities": blended_probs,
        "predicted_winner_blended": winner_blended,
        "blending_weights": {"classification": weight_class, "regression": 1 - weight_class},
    }


def debug_team_modifiers(team_a: str, team_b: str):
    """
    Prints the actual venue modifiers and calculates the final 
    Intensity Gap created by the tiered Elo logic.
    """
    load_data_once()
    
    # 1. Get the modifiers from your updated logic
    h_mod, a_mod = get_venue_performance_mod(team_a, team_b)
    
    # 2. Extract metadata for display
    h_row, h_pre = _get_latest_metadata(team_a)
    a_row, a_pre = _get_latest_metadata(team_b)
    
    h_elo = h_row.get(f'{h_pre}elo', 1500)
    a_elo = a_row.get(f'{a_pre}elo', 1500)
    
    # 3. Calculate "Match Intensity Score"
    # This represents the total statistical shift before players even touch the ball.
    intensity_gap = (h_mod / a_mod) if a_mod != 0 else h_mod

    print(f"\n" + "="*45)
    print(f" MATCHUP: {team_a} vs {team_b}")
    print(f"="*45)
    print(f"{'Team':<15} | {'Elo':<8} | {'Modifier':<10}")
    print(f"-"*45)
    print(f"{team_a + ' (H)':<15} | {h_elo:<8.1f} | {h_mod:<10.3f}")
    print(f"{team_b + ' (A)':<15} | {a_elo:<8.1f} | {a_mod:<10.3f}")
    print(f"-"*45)
    print(f"Venue Intensity Gap: {intensity_gap:.3f}x")
    
    if intensity_gap > 1.10:
        print("Status: Significant Home Advantage")
    elif intensity_gap < 0.95:
        print("Status: Significant Away Advantage")
    else:
        print("Status: Statistically Balanced Match")
    print(f"="*45)


if __name__ == "__main__":
    debug_team_modifiers("Tottenham", "Arsenal")