import numpy as np
import pandas as pd
from typing import Tuple, List
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.utils.class_weight import compute_class_weight

TEST_SIZE_RATIO = 0.25

# accepts final dataframe, target outputs of classification and regression from data_preparation.py
# returns two dfs of X, 6 series of y (2 of y_classification, 2 each of regression - home & away)
def data_splitting(output_tuples: Tuple[pd.DataFrame, pd.Series, pd.Series, pd.Series]) -> Tuple[
    pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series, pd.Series, pd.Series, pd.Series]:
    df, classification_output_home, regression_output_home, regression_output_away = output_tuples
    X_classification = df.drop(columns='FTR', errors='ignore')
    
    # Preserve FTR in X_train temporarily for weight calculation logic
    if 'FTR' in df.columns:
        X_classification['FTR'] = df['FTR']

    y_classification = pd.get_dummies(classification_output_home, prefix='Result')
    split_point = int(len(X_classification) * (1 - TEST_SIZE_RATIO))
    
    X_train = X_classification.iloc[:split_point].copy()
    X_test = X_classification.iloc[split_point:].copy()
    
    y_train_classification = y_classification.iloc[:split_point].copy()
    y_test_classification = y_classification.iloc[split_point:].copy()
    
    y_train_regression_home = regression_output_home.iloc[:split_point].copy()
    y_test_regression_home = regression_output_home.iloc[split_point:].copy()
    
    y_train_regression_away = regression_output_away.iloc[:split_point].copy()
    y_test_regression_away = regression_output_away.iloc[split_point:].copy()
    
    return X_train, X_test, y_train_classification, y_test_classification, y_train_regression_home, y_test_regression_home, y_train_regression_away, y_test_regression_away 

# accepts the dfs of X after splitting
# returns the renamed dfs of X
def column_renaming(X_dfs: Tuple[pd.DataFrame, pd.DataFrame]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    X_train, X_test = X_dfs
    X_train.columns = X_train.columns.str.replace('>', '_GT_', regex=False).str.replace('<', '_LT_', regex=False).str.replace('.', '_', regex=False)
    X_test.columns = X_test.columns.str.replace('>', '_GT_', regex=False).str.replace('<', '_LT_', regex=False).str.replace('.', '_', regex=False)    
    return X_train, X_test 

# accepts the two renamed dfs of X, returns scaled dfs of X
def values_scaling(X_renamed: Tuple[pd.DataFrame, pd.DataFrame]) -> Tuple[pd.DataFrame, pd.DataFrame, StandardScaler]:
    X_train, X_test = X_renamed
    scaler = StandardScaler()
    
    # We exclude 'FTR' from scaling if it's still there
    cols_to_scale = [c for c in X_train.columns if c != 'FTR']
    
    X_train[cols_to_scale] = scaler.fit_transform(X_train[cols_to_scale])
    X_test[cols_to_scale] = scaler.transform(X_test[cols_to_scale])
    
    return X_train, X_test, scaler

# accepts the output series of classification
# returns the label encoded output series of classification
def label_encoding(y_classification_series: Tuple[pd.Series, pd.Series]) -> Tuple[pd.Series, pd.Series]:
    y_train_classification, y_test_classification = y_classification_series
    y_train_labels = y_train_classification.idxmax(axis=1)
    y_test_labels = y_test_classification.idxmax(axis=1)
    le = LabelEncoder()
    le.fit(pd.concat([y_train_labels, y_test_labels]).unique()) 
    y_train_encoded = le.transform(y_train_labels)
    y_test_encoded = le.transform(y_test_labels) 
    return y_train_encoded, y_test_encoded

# --- UPDATED: Advanced Football Logic Weighting ---
def class_weight_computation(y_encoded_series: Tuple[np.array, np.array], X_train_raw: pd.DataFrame) -> np.array:
    y_train_classification_encoded, _ = y_encoded_series
    
    # 1. Base Class Balancing (Standard)
    classes = np.unique(y_train_classification_encoded)
    class_weights = compute_class_weight(
        class_weight='balanced', 
        classes=classes, 
        y=y_train_classification_encoded 
    )
    sample_weight = np.array([class_weights[i] for i in y_train_classification_encoded])
    
    # Ensure necessary columns exist for the logic
    required_cols = ['expected_goals_Diff', 'Elo_Gap_Diff', 'HT_elo', 'AT_elo', 'FTR']
    if not all(col in X_train_raw.columns for col in required_cols):
        return sample_weight

    # 2. Extract Logic Variables (Matching Online predicit_match)
    avg_elo = (X_train_raw['HT_elo'] + X_train_raw['AT_elo']) / 2
    elo_diff_abs = X_train_raw['Elo_Gap_Diff'].abs()
    
    # 3. Apply Weights Based on Online "Modes"
    
    # A. ELITE MATCHES (High quality data - Boost importance)
    # Trust these games more because they are tactically consistent
    elite_mask = ((X_train_raw['HT_elo'] > 1875) | (X_train_raw['AT_elo'] > 1875)) & (elo_diff_abs < 150)
    sample_weight[elite_mask.values] *= 1.25

    # B. HEAVY MISMATCHES (One team dominant)
    # If the favorite wins, boost it (learning the 'norm'). 
    # If it's a draw, deflate it (the 'Draw Trap' fix from online).
    mismatch_mask = elo_diff_abs > 150
    mismatch_draw = mismatch_mask & (X_train_raw['FTR'] == 'D')
    sample_weight[mismatch_draw.values] *= 0.15 # Strong penalty for outlier draws
    
    # C. LOW-QUALITY / GRIND ZONE (Relegation scraps)
    # Deflate importance slightly because these are high-variance/random
    grind_mask = (X_train_raw['HT_elo'] < 1775) | (X_train_raw['AT_elo'] < 1775)
    sample_weight[grind_mask.values] *= 0.8

    # 4. Performance-Based Refinement (The "Lucky" Win Tax)
    # Deflate wins where the winner had significantly worse xG (Noise reduction)
    lucky_home = (X_train_raw['FTR'] == 'H') & (X_train_raw['expected_goals_Diff'] < -1.0)
    lucky_away = (X_train_raw['FTR'] == 'A') & (X_train_raw['expected_goals_Diff'] > 1.0)
    sample_weight[lucky_home.values | lucky_away.values] *= 0.5 

    return sample_weight

# main function!
def define_model_ready_data(output_tuples: 
                            Tuple[pd.DataFrame, pd.Series, pd.Series, pd.Series]) -> Tuple[
    pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series, pd.Series, pd.Series, pd.Series, np.array, StandardScaler, List[str]]:
    
    print("1. Splitting the data into Training (75%) and Testing splits (25%)\n")
    X_train, X_test, y_train_classification, y_test_classification, y_train_regression_home, y_test_regression_home, y_train_regression_away, y_test_regression_away = data_splitting(output_tuples)
    
    print("2. Renaming the columns for better model understanding.\n")
    X_train_renamed, X_test_renamed = column_renaming(X_dfs=(X_train, X_test))
    
    # Capture all features before scaling/dropping FTR
    all_features = [c for c in X_train_renamed.columns if c != 'FTR']
    
    print("3. Scaling and transforming the values of Input training data and testing data.\n")
    X_train_scaled, X_test_scaled, scaler = values_scaling(X_renamed=(X_train_renamed, X_test_renamed))
    
    print("4. Performing Label Encoding on classification output series.\n")
    y_train_classification_encoded, y_test_classification_encoded = label_encoding(y_classification_series=(y_train_classification, y_test_classification))
    
    print("5. Computing the advanced football-logic class weights.\n")
    # Pass renamed X_train so we can access Elo/xG columns for logic
    sample_weight = class_weight_computation(
        y_encoded_series=(y_train_classification_encoded, y_test_classification_encoded),
        X_train_raw=X_train_renamed
    )
    
    # FINAL CLEANUP: Remove FTR from the datasets before returning to model
    X_train_scaled = X_train_scaled.drop(columns='FTR', errors='ignore')
    X_test_scaled = X_test_scaled.drop(columns='FTR', errors='ignore')
    X_train = X_train.drop(columns='FTR', errors='ignore')
    X_test = X_test.drop(columns='FTR', errors='ignore')

    print(f"{' '*59}THE MODEL IS READY TO MAKE PREDICTIONS NOW!\n")
    return X_train_scaled, X_test_scaled, X_train, X_test, y_train_classification_encoded, y_test_classification_encoded, y_train_regression_home, y_test_regression_home, y_train_regression_away, y_test_regression_away, sample_weight, scaler, all_features