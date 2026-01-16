import pandas as pd
import live_feature_calculation
from live_feature_calculation import load_data_once, get_all_teams
try: 
    live_feature_calculation.load_data_once()
    data = live_feature_calculation.MAIN_DF
    teams = live_feature_calculation.get_all_teams()
    colslist = data.columns.to_list()
    for col in colslist:
        print(col)
except Exception as e:
    print(f"Error: {e}")

