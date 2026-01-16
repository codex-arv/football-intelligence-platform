import pandas as pd
import numpy as np
from typing import Tuple
from sklearn.metrics import accuracy_score, classification_report 
from sklearn.ensemble import RandomForestRegressor 
from sklearn.metrics import mean_absolute_error, mean_squared_error 
import xgboost as xgb 

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# Type alias for clarity
rfr_model = RandomForestRegressor

def training_XGB(classification_tuples: Tuple[
    pd.DataFrame, pd.DataFrame, np.ndarray, np.ndarray, np.ndarray
    ]) -> Tuple[xgb.XGBClassifier, np.ndarray, float, str]:
    """
    Trains the XGBoost Classification model using the advanced football-logic weights.
    """
    print("="*156)
    print("="*156)
    print()
    print(f"{' '*62}TRAINING THE CLASSIFICATION MODEL NOW!\n")
    
    X_train_final, X_test_final, y_train_classification, y_test_classification, sample_weight = classification_tuples
    
    print("1. Initializing the XGBoost Ensemble Model.")
    # Parameters optimized for 3-class football outcome (H, D, A)
    xgb_model = xgb.XGBClassifier(
        objective='multi:softmax',
        n_estimators=1000,
        learning_rate=0.03,        # LOWERED (from 0.09) - forces slower, more careful learning
        max_depth=4,               # LOWERED (from default) - prevents the model from finding "complex" fluke patterns
        reg_lambda=10,
        reg_alpha=5,
        min_child_weight=5,        # INCREASED - prevents the model from creating rules based on just 1 or 2 outlier matches
        colsample_bytree=0.6,      # NEW - forces the model to ignore 40% of features (like touches) in each tree
        subsample=0.7,             # NEW - trains on random subsets of data to prevent overfitting
        gamma=1,                   # NEW - makes the model more conservative
        num_class=3, 
        eval_metric='mlogloss',
        random_state=42
    )
    
    print("2. Training the model now with advanced sample weighting.")
    # The sample_weight here now contains both Class Balance AND Football Logic (Elo/xG)
    xgb_model.fit(X_train_final, y_train_classification, sample_weight=sample_weight)
    
    print("3. Predicting on test data.")
    prediction = xgb_model.predict(X_test_final)
    
    print("4. Evaluating the performance of the model.\n")
    accuracy = accuracy_score(y_test_classification, prediction) 
    print(f"ACCURACY: {accuracy * 100:.4f}%")
    
    report = classification_report(y_test_classification, prediction)
    print(f"CLASSIFICATION REPORT (Advanced Logic Training):")
    print(report)
    
    return xgb_model, prediction, accuracy, report

def training_RFR_home(regression_home_tuples: Tuple[
    pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]) -> Tuple[rfr_model, np.ndarray, float, float]:
    """
    Trains the Random Forest Regressor for Home Goals.
    """
    print("="*156)
    print("="*156)
    print()
    print(f"{' '*63}TRAINING THE REGRESSION MODELS NOW!\n")
    
    X_train_final, X_test_final, y_train_regression_home, y_test_regression_home = regression_home_tuples
    
    rfr_home = RandomForestRegressor(
        n_estimators=1000,     
        max_depth=10,         
        random_state=RANDOM_STATE,
        n_jobs=-1             
    )
    
    print("1. Starting training for Home Goals Regressor\n")
    rfr_home.fit(X_train_final, y_train_regression_home)
    
    pred_home_goals_float = rfr_home.predict(X_test_final)
    pred_home_goals = np.round(np.maximum(0, pred_home_goals_float)).astype(int)
    
    mae_home = mean_absolute_error(y_test_regression_home, pred_home_goals)
    mse_home = mean_squared_error(y_test_regression_home, pred_home_goals)
    
    print("HOME REGRESSION MODEL PERFORMANCE:")
    print(f"Mean Absolute Error (MAE): {mae_home:.4f}")
    print(f"Mean Squared Error (MSE):  {mse_home:.4f}\n")
    
    return rfr_home, pred_home_goals, mae_home, mse_home

def training_RFR_away(regression_away_tuples: Tuple[
    pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]) -> Tuple[rfr_model, np.ndarray, float, float]:
    """
    Trains the Random Forest Regressor for Away Goals.
    """
    X_train_final, X_test_final, y_train_regression_away, y_test_regression_away = regression_away_tuples
    
    rfr_away = RandomForestRegressor(
        n_estimators=1000,     
        max_depth=10,         
        random_state=RANDOM_STATE,
        n_jobs=-1             
    )
    
    print("2. Starting training for Away Goals Regressor\n")
    rfr_away.fit(X_train_final, y_train_regression_away)
    
    pred_away_goals_float = rfr_away.predict(X_test_final)
    pred_away_goals = np.round(np.maximum(0, pred_away_goals_float)).astype(int)
    
    mae_away = mean_absolute_error(y_test_regression_away, pred_away_goals)
    mse_away = mean_squared_error(y_test_regression_away, pred_away_goals)
    
    print("AWAY REGRESSION MODEL PERFORMANCE:")
    print(f"Mean Absolute Error (MAE): {mae_away:.4f}")
    print(f"Mean Squared Error (MSE):  {mse_away:.4f}\n")
    
    return rfr_away, pred_away_goals, mae_away, mse_away