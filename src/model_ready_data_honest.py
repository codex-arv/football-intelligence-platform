import numpy as np
import pandas as pd
from typing import Tuple, List
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.utils.class_weight import compute_sample_weight

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

# main function!
def define_model_ready_data_honest(output_tuples: 
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
    
    print("5. Computing balanced class weights.\n")
    sample_weight = compute_sample_weight(
        class_weight='balanced',
        y=y_train_classification_encoded
    )
    
    # FINAL CLEANUP: Remove FTR from the datasets before returning to model
    X_train_scaled = X_train_scaled.drop(columns='FTR', errors='ignore')
    X_test_scaled = X_test_scaled.drop(columns='FTR', errors='ignore')
    X_train = X_train.drop(columns='FTR', errors='ignore')
    X_test = X_test.drop(columns='FTR', errors='ignore')

    print(f"{' '*59}THE MODEL IS READY TO MAKE PREDICTIONS NOW!\n")
    return X_train_scaled, X_test_scaled, X_train, X_test, y_train_classification_encoded, y_test_classification_encoded, y_train_regression_home, y_test_regression_home, y_train_regression_away, y_test_regression_away, sample_weight, scaler, all_features