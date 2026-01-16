# import numpy as np
# import pandas as pd
# import os
# import joblib
# from typing import List, Tuple, Dict, Union

# # ---------------- CONFIG ---------------- #

# RENAME_MAP = {
#     'home_possession': 'HT_possession',
#     'away_possession': 'AT_possession',
#     'home_expected_goals_xg': 'HT_expected_goals',
#     'away_expected_goals_xg': 'AT_expected_goals',
#     'home_big_chances': 'HT_big_chances',
#     'away_big_chances': 'AT_big_chances',
#     'home_big_chances_missed': 'HT_big_chances_missed',
#     'away_big_chances_missed': 'AT_big_chances_missed',
#     'home_xg_open_play': 'HT_xg_open_play',
#     'away_xg_open_play': 'AT_xg_open_play',
#     'home_xg_set_play': 'HT_xg_set_play',
#     'away_xg_set_play': 'AT_xg_set_play',
#     'home_non_penalty_xg': 'HT_non_penalty',
#     'away_non_penalty_xg': 'AT_non_penalty',
#     'home_xg_on_target_xgot': 'HT_xg_on_targetot',
#     'away_xg_on_target_xgot': 'AT_xg_on_targetot',
#     'home_touches_in_opposition_box': 'HT_touches_in_opposition_box',
#     'away_touches_in_opposition_box': 'AT_touches_in_opposition_box',
#     'H2H_HT_Points_L5': 'HT_H2H_Points',
#     'H2H_AT_Points_L5': 'AT_H2H_Points',
#     'BbMxH': 'MaxH',
#     'BbMxD': 'MaxD',
#     'BbMxA': 'MaxA',
#     'BbMx_GT_2.5': 'Max_GT_2_5',
#     'BbMx_LT_2.5': 'Max_LT_2_5',
#     'BbAv_GT_2.5': 'Avg_GT_2_5',
#     'BbAv_LT_2.5': 'Avg_LT_2_5',
# }

# FORM_WINDOW_SIZE = 5

# MODEL_ARTIFACTS = 'model_artifacts'
# DATA_ARTIFACTS = 'data_artifacts'
# MASTER_DATA = 'master_data.pkl'
# FINAL_FEATURES = 'final_features.pkl'

# LABELS = ['Away Win', 'Draw', 'Home Win']

# MAIN_DF = pd.DataFrame()
# FEATURE_LIST: List[str] = []
# MODELS: Dict[str, any] = {}

# # ---------------- LOADERS ---------------- #

# def load_data_once():
#     global MAIN_DF, FEATURE_LIST

#     data_path = os.path.join(DATA_ARTIFACTS, MASTER_DATA)
#     features_path = os.path.join(DATA_ARTIFACTS, FINAL_FEATURES)

#     MAIN_DF = joblib.load(data_path)
#     MAIN_DF = MAIN_DF.rename(columns=RENAME_MAP)
#     MAIN_DF["Date"] = pd.to_datetime(MAIN_DF["Date"])
#     MAIN_DF = MAIN_DF.sort_values("Date", ascending=False).reset_index(drop=True)

#     # Clean column names
#     MAIN_DF.columns = [
#         col.replace('>', '_GT_').replace('<', '_LT_').replace('2.5', '2_5')
#         for col in MAIN_DF.columns
#     ]

#     FEATURE_LIST[:] = joblib.load(features_path)


# def load_model_once():
#     global MODELS

#     paths = {
#         "classification_model": "xgb_model1.joblib",
#         "regression_home_model": "rfr_home1.joblib",
#         "regression_away_model": "rfr_away1.joblib",
#         "scaler": "scaler1.joblib"
#     }

#     for name, file in paths.items():
#         full = os.path.join(MODEL_ARTIFACTS, file)
#         MODES = MODELS[name] = joblib.load(full)


# # ---------------- UTILS ---------------- #

# def get_all_teams():
#     return sorted(set(MAIN_DF["HomeTeam"]).union(set(MAIN_DF["AwayTeam"])))


# def get_base_features():
#     diff = [c for c in FEATURE_LIST if c.endswith("_Diff")]
#     bases = sorted(list(set([c.replace("_Diff", "") for c in diff])))
#     static = [c for c in FEATURE_LIST if not c.endswith("_Diff")]
#     return bases, static


# def _get_team_form_stats(team: str, base_features: List[str], loc: str):
#     if loc == "Home":
#         df = MAIN_DF[MAIN_DF["HomeTeam"] == team]
#         prefix = "HT_"
#     else:
#         df = MAIN_DF[MAIN_DF["AwayTeam"] == team]
#         prefix = "AT_"

#     df = df.head(FORM_WINDOW_SIZE)
#     stats = {}

#     for base in base_features:
#         col = prefix + base
#         if col in df.columns:
#             stats[base] = df[col].mean()
#         else:
#             stats[base] = 0.0

#     return stats


# def calculate_features(home: str, away: str):
#     base, static = get_base_features()

#     home_stats = _get_team_form_stats(home, base, "Home")
#     away_stats = _get_team_form_stats(away, base, "Away")

#     features = {}

#     # differential features
#     for b in base:
#         features[f"{b}_Diff"] = home_stats[b] - away_stats[b]

#     # static features (use dataset mean)
#     for s in static:
#         features[s] = MAIN_DF[s].mean() if s in MAIN_DF else 0.0

#     df = pd.DataFrame([features])
#     df = df[FEATURE_LIST]

#     return df


# # ---------------- PREDICTION ---------------- #

# def predict_match(home: str, away: str):
#     X = calculate_features(home, away)

#     # scale
#     scaler = MODELS["scaler"]
#     X_scaled = pd.DataFrame(scaler.transform(X), columns=X.columns)

#     # classification
#     clf = MODELS["classification_model"]
#     probs = clf.predict_proba(X_scaled)[0]

#     idx = np.argmax(probs)
#     winner_label = LABELS[idx]

#     if winner_label == "Home Win":
#         winner = home
#     elif winner_label == "Away Win":
#         winner = away
#     else:
#         winner = "Draw"

#     # regression
#     home_goals = MODELS["regression_home_model"].predict(X_scaled)[0]
#     away_goals = MODELS["regression_away_model"].predict(X_scaled)[0]

#     return {
#         "winner": winner,
#         "scoreline": f"{round(home_goals)} - {round(away_goals)}",
#         "raw_scoreline": f"{home_goals:.3f} - {away_goals:.3f}",
#         "probabilities": {
#             "away_win": float(probs[0]),
#             "draw": float(probs[1]),
#             "home_win": float(probs[2])
#         }
#     }


# # # ---------------- CLI ENTRY ---------------- #

# # if __name__ == "__main__":
# #     print("📌 Loading Data & Models...")
# #     load_data_once()
# #     load_model_once()

# #     teams = get_all_teams()

# #     print("\n⚽ Available Teams:")
# #     print(", ".join(teams))

# #     print("\n-----------------------------------------")
# #     home = input("🏟️ Enter Home Team: ").strip()
# #     away = input("🚗 Enter Away Team: ").strip()
# #     print("-----------------------------------------\n")

# #     if home not in teams or away not in teams:
# #         print("❌ Invalid team name. Please run again.")
# #         exit()

# #     result = predict_match(home, away)

# #     print("✅ Prediction Complete!\n")
# #     print(f"📌 Predicted Winner: {result['winner']}")
# #     print(f"📊 Scoreline: {result['scoreline']}")
# #     print(f"🧪 Raw Scoreline: {result['raw_scoreline']}")
# #     print("\n🔮 Probabilities:")
# #     for k, v in result["probabilities"].items():
# #         print(f"  {k}: {v:.3%}")
