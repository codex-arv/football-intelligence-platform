import pandas as pd
from data_ingestion1 import load_merge_pl_data, DIRECTORY
from data_ingestion2_pipelined import load_all_data
from feature_engineering import run_full_feature_engineering
from feature_engineering_ewma import run_full_feature_engineering_ewma
from relational_data import work_with_relational_data
from data_merging import load_merge_data
from merged_data_feature_engineering import merged_data_cleaning, merged_data_feature_manipulation
from data_preparation import data_preparation
from model_ready_data import define_model_ready_data
from model_training import training_XGB, training_RFR_home, training_RFR_away
from save_artifacts import save_model_artifacts, save_data_artifact, save_transformed_data_artifact, OUTPUT_ARTIFACTS_DIR, OUTPUT_DATA_DIR

# 1. Load PL data from 2000 to 2025 (master data)
original_df = load_merge_pl_data(DIRECTORY)
transform_df = original_df.copy()

# 2. Load Relational Data (Players-Matches, Players, Matches, Teams) of 2024 and 2025 season
dictionary = load_all_data()

# 3. Clean the PL data (original_df) and perform Feature Engineering (rolling L5 features)
clean_df = run_full_feature_engineering(original_df)
transformed_df = run_full_feature_engineering_ewma(transform_df)

# 4. Work with the Relational Data (Combine dataframes, clean them and perform feature engineering - rolling last 5 matches)
fe_gk_stats, fe_def_stats, fe_mid_stats, fe_fwd_stats, final_teams_matches = work_with_relational_data(dictionary=dictionary)

# 5. Merge all these data into one master dataset for feeding to the model
merged_tuples = (clean_df, fe_gk_stats, fe_def_stats, fe_mid_stats, fe_fwd_stats, final_teams_matches)
merged_tuples_transformed = (transformed_df, fe_gk_stats, fe_def_stats, fe_mid_stats, fe_fwd_stats, final_teams_matches)
merged_df = load_merge_data(all_data=merged_tuples)
merged_transformed_df = load_merge_data(all_data=merged_tuples_transformed)

# 6. Clean the merged data, perform Feature Engineering and Feature Reduction
cleaned_merged_data = merged_data_cleaning(merged_data=merged_df)
transformed_merged_data = merged_data_cleaning(merged_data=merged_transformed_df)
full_data, final_merged_data = merged_data_feature_manipulation(clean_merged_data=transformed_merged_data)

# 7. Preparing the data for model training: Final dataset before splitting, returning target features 
final_df, y_classification, y_regression_home, y_regression_away = data_preparation(final_merged_data)
final_passed_df = final_df.drop(columns=['Date', 'HomeTeam', 'AwayTeam'], errors='ignore')

# 8. Preparing the Model-ready data (involves data splitting, feature scaling, column renaming, label encoding the classification output features and computing the class weight for classification)
output_tuples = (final_passed_df, y_classification, y_regression_home, y_regression_away)
X_train, X_test, X_train_ref, X_test_ref, y_train_classification_final, y_test_classification_final, y_train_regression_home, y_test_regression_home, y_train_regression_away, y_test_regression_away, sample_weight, scaler, all_features = define_model_ready_data(output_tuples=output_tuples)

# 9. Training the classification model (XGBoost Classifier)
classification_tuples = (X_train, X_test, y_train_classification_final, y_test_classification_final, sample_weight)
xgb_model, xgb_prediction, xgb_accuracy, xgb_report = training_XGB(classification_tuples=classification_tuples)

# Check the raw probabilities instead of the final labels
probs = xgb_model.predict_proba(X_test)
prob_df = pd.DataFrame(probs, columns=['Away_Prob', 'Draw_Prob', 'Home_Prob'])

# Look for games where the model is 'overconfident' (> 80%)
high_conf = prob_df[prob_df['Home_Prob'] > 0.80]
print(f"Number of high-confidence Home predictions: {len(high_conf)}")

 # Get feature importance
importance = xgb_model.get_booster().get_score(importance_type='weight')
importance = dict(sorted(importance.items(), key=lambda item: item[1], reverse=True))

# Print the top 20
print("TOP 20 FEATURES:")
for i, (k, v) in enumerate(list(importance.items())[:20]):
    print(f"{i+1}. {k}: {v}")

# 10. Training the regression models (RandomForest Regressor)
regression_home_tuples = (X_train, X_test, y_train_regression_home, y_test_regression_home)
regression_away_tuples = (X_train, X_test, y_train_regression_away, y_test_regression_away)
rfr_home, home_prediction, mae_home, mse_home = training_RFR_home(regression_home_tuples=regression_home_tuples)
rfr_away, away_prediction, mae_away, mse_away = training_RFR_away(regression_away_tuples=regression_away_tuples)

# 11. Save the artifacts for future integration
save_data_artifact(df=cleaned_merged_data, features=all_features, output_dir=OUTPUT_DATA_DIR)
save_transformed_data_artifact(df=transformed_merged_data, features=all_features, output_dir=OUTPUT_DATA_DIR)
save_model_artifacts(xgb_model=xgb_model, rfr_home=rfr_home, rfr_away=rfr_away, scaler=scaler,output_dir=OUTPUT_ARTIFACTS_DIR)
