# this file is responsible for extensive feature engineering before saving the data as artifact for live predictions
# this file also accounts for the engineered features over which our models train on 

import numpy as np
import pandas as pd
from typing import List
from data_cleaning import data_cleaning

# multi-class odds: must normalize them
PROB_NORM_ODDS: List[List[str]] = [
    ['BbAvH', 'BbAvD', 'BbAvA'], ['AvgCH', 'AvgCD', 'AvgCA'], ['PSCH', 'PSCD', 'PSCA'],              
    ['MaxH', 'MaxD', 'MaxA', 'AvgH', 'AvgD', 'AvgA', 'B365H', 'B365D', 'B365A', 'B365CH', 'B365CD', 'B365CA'],
    ['AvgC>2.5', 'AvgC<2.5'], ['PC>2.5', 'PC<2.5']
]

# binary odds: doesnt need normalization
PROB_ODDS: List[List[str]] = [
    ['AvgCAHH', 'AvgCAHA'], 
    ['PCAHH', 'PCAHA']      
]

REMOVABLE_COLUMNS: List[str] = ['Div', 'AHCh', 'HHW', 'AHW', 'HO', 'AO', 'IWH', 'IWD', 'IWA', 'LBH', 'LBD', 'LBA', 
                                'SBH', 'SBD', 'SBA', 'WHH', 'WHD', 'WHA', 'SYH', 'SYD', 'SYA', 'SOH', 'SOD', 'SOA', 
                                'Unnamed: 48', 'Unnamed: 49', 'Unnamed: 50', 'Unnamed: 51', 'Unnamed: 52', 
                                'GBAHH', 'GBAHA', 'GBAH', 'LBAHH', 'LBAHA', 'LBAH', 'Bb1X2', 'BbOU', 'BbAH', 'BbMxAHH', 'BbMxAHA', 
                                'BWH', 'BWD', 'BWA',  'SJH', 'SJD', 'SJA',  'VCH', 'VCD', 'VCA', 'BSH', 'BSD', 'BSA', 'Time', 'BWCH', 'BWCD', 'BWCA', 
                                'IWCH', 'IWCD', 'IWCA', 'WHCH', 'WHCD', 'WHCA', 'VCCH', 'VCCD', 'VCCA', '1XBH', '1XBD', '1XBA', 
                                '1XBCH', '1XBCD', '1XBCA', 'BFH', 'BFD', 'BFA', 'BFEH', 'BFED', 'BFEA', 'BFE>2.5', 'BFE<2.5', 
                                'BFEAHH', 'BFEAHA', 'BFDH', 'BFDD', 'BFDA', 'BMGMH','BMGMD','BMGMA', 'BVH','BVD','BVA', 
                                'CLH','CLD','CLA', 'BFDCH','BFDCD','BFDCA', 'BMGMCH','BMGMCD','BMGMCA',
                                'BVCH','BVCD','BVCA', 'CLCH','CLCD','CLCA', 'LBCH', 'LBCD','LBCA']

# bookmakers give decimal odds, not probabilities
# first, all the odds are converted to implied probabilities
# domain knowledge: bookmakers add marginal overround (profit) such that the sum of IPs of W,D,L > 1
# to eliminate the bias added by the bookmaker, we removed the margin giving a much truer estimate of market belief
def norm_ip_margin_conversion(df: pd.DataFrame) -> pd.DataFrame:
    temp_df = df.copy()
    temp_df['IP_Home_PS'] = 1 / temp_df['PSCH']
    temp_df['IP_Draw_PS'] = 1 / temp_df['PSCD']
    temp_df['IP_Away_PS'] = 1 / temp_df['PSCA']
    temp_df['NormIP_Margin'] = (temp_df['IP_Home_PS'] + temp_df['IP_Draw_PS'] + temp_df['IP_Away_PS']) - 1
    temp_df = temp_df.drop(columns=['IP_Home_PS', 'IP_Draw_PS', 'IP_Away_PS'], errors='ignore')
    return temp_df

def probability(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    temp_df = df.copy()
    ip_columns = [f'IP_AHO_{col}' for col in columns] 
    for odd, new in zip(columns, ip_columns):
        temp_df[new] = 1 / temp_df[odd]
    temp_df = temp_df.drop(columns=columns, errors='ignore')
    return temp_df

# why this matters: 
# failure to normalize probability and remove bias might result in poor generalization, latent bias, lower model performance
def probability_normalization(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    temp_df = df.copy()
    ip_columns = [f'IP_{col}' for col in columns]
    # convert to IP
    for odd, new in zip(columns, ip_columns):
        temp_df[new] = 1 / temp_df[odd]
    # calculate sum for the specific IP columns
    total = temp_df[ip_columns].sum(axis=1)
    norm_columns = [f'NormIP_{col}' for col in columns]
    # calculate the normalized probability for the implied ones
    for ip, norm in zip(ip_columns, norm_columns):
        temp_df[norm] = temp_df[ip] / total
    temp_df = temp_df.drop(columns=columns + ip_columns, errors='ignore')
    return temp_df

def conversion_prob_norm(df: pd.DataFrame) -> pd.DataFrame:
    working_df = df.copy()
    for category in PROB_NORM_ODDS:
        working_df = probability_normalization(working_df, category)
    for category in PROB_ODDS:
        working_df = probability(working_df, category)
    return working_df

def date_to_datetime(df: pd.DataFrame) -> pd.DataFrame:
    df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True)
    df = df.sort_values(by=['Date']).reset_index(drop=True)
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    return df

def rolling_feature_engineering_ewma(df: pd.DataFrame) -> pd.DataFrame:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # Exponentially Weighted Moving Average
    # time-aware smoothening technique where recent observations are of higher priority and as we go back in time, the importance exponentially decays
    def get_ewma(series):
        # span=7 ensures matches from 1-2 months ago are included but recent ones dominate
        # ensuring the use of shift() before ewm to avoid data leakage: ensuring only past matches contribute to features
        # ewma helped to convert raw match data to team-level chronological signals 
        return series.shift().ewm(span=7, adjust=True).mean()

    # 1. Global Goals (REPLACED WITH EWMA)
    home_df = df[['Date', 'HomeTeam', 'FTHG', 'FTAG']].copy()
    home_df.columns = ['Date', 'Team', 'GoalsFor', 'GoalsAgainst']
    away_df = df[['Date', 'AwayTeam', 'FTAG', 'FTHG']].copy()
    away_df.columns = ['Date', 'Team', 'GoalsFor', 'GoalsAgainst']
    combined_df = pd.concat([home_df, away_df], ignore_index=True)
    combined_df = combined_df.sort_values(['Team', 'Date']).reset_index(drop=True)
    
    combined_df['Team_GF_L5'] = combined_df.groupby('Team')['GoalsFor'].transform(get_ewma)
    combined_df['Team_GA_L5'] = combined_df.groupby('Team')['GoalsAgainst'].transform(get_ewma)
    
    df = df.merge(combined_df[['Date', 'Team', 'Team_GF_L5', 'Team_GA_L5']],
                  left_on=['Date', 'HomeTeam'], right_on=['Date', 'Team'], how='left')
    df = df.rename(columns={'Team_GF_L5': 'HT_AvgGF_L5', 'Team_GA_L5': 'HT_AvgGA_L5'}).drop(columns='Team', errors='ignore')
    df = df.merge(combined_df[['Date', 'Team', 'Team_GF_L5', 'Team_GA_L5']],
                  left_on=['Date', 'AwayTeam'], right_on=['Date', 'Team'], how='left')
    df = df.rename(columns={'Team_GF_L5': 'AT_AvgGF_L5', 'Team_GA_L5': 'AT_AvgGA_L5'}).drop(columns='Team', errors='ignore')

    # 2. Home Ground Stats (REPLACED WITH EWMA SPAN 7)
    home_ground = df[['Date', 'HomeTeam', 'FTHG', 'FTAG']].copy()
    home_ground = home_ground.rename(columns={'HomeTeam':'Team', 'FTHG':'GoalsFor', 'FTAG':'GoalsAgainst'})
    home_ground = home_ground.sort_values(['Team', 'Date']).reset_index(drop=True)
    home_ground['HG_HT_AvgGF_L5'] = home_ground.groupby('Team')['GoalsFor'].transform(get_ewma)
    home_ground['HG_HT_AvgGA_L5'] = home_ground.groupby('Team')['GoalsAgainst'].transform(get_ewma)
    home_ground['HG_HT_AvgGD_L5'] = home_ground['HG_HT_AvgGF_L5'] - home_ground['HG_HT_AvgGA_L5']
    df = df.merge(home_ground[['Date', 'Team', 'HG_HT_AvgGF_L5', 'HG_HT_AvgGA_L5', 'HG_HT_AvgGD_L5']],
                left_on=['Date', 'HomeTeam'], right_on=['Date', 'Team'], how='left').drop(columns='Team', errors='ignore')
    
    # 3. Away Ground Stats (REPLACED WITH EWMA SPAN 7)
    away_ground = df[['Date', 'AwayTeam', 'FTHG', 'FTAG']].copy()
    away_ground = away_ground.rename(columns={'AwayTeam':'Team', 'FTHG':'GoalsAgainst', 'FTAG':'GoalsFor'}) 
    away_ground = away_ground.sort_values(['Team', 'Date']).reset_index(drop=True)
    away_ground['AG_AT_AvgGF_L5'] = away_ground.groupby('Team')['GoalsFor'].transform(get_ewma)
    away_ground['AG_AT_AvgGA_L5'] = away_ground.groupby('Team')['GoalsAgainst'].transform(get_ewma)
    away_ground['AG_AT_AvgGD_L5'] = away_ground['AG_AT_AvgGF_L5'] - away_ground['AG_AT_AvgGA_L5']
    df = df.merge(away_ground[['Date', 'Team', 'AG_AT_AvgGF_L5', 'AG_AT_AvgGA_L5', 'AG_AT_AvgGD_L5']],
                  left_on=['Date', 'AwayTeam'], right_on=['Date', 'Team'], how='left').drop(columns='Team', errors='ignore')
    
    df = df[~df.duplicated()].reset_index(drop=True)

    # 4. Avg Shots (REPLACED WITH EWMA SPAN 7)
    shots_home = df[['Date','HomeTeam','HS']].copy().rename(columns={'HomeTeam':'Team', 'HS':'Shots'})
    shots_away = df[['Date','AwayTeam','AS']].copy().rename(columns={'AwayTeam':'Team', 'AS':'Shots'})
    shots_df = pd.concat([shots_home, shots_away], ignore_index=True).sort_values(['Team','Date'])
    shots_df['Shots_L5'] = shots_df.groupby('Team')['Shots'].transform(get_ewma)
    mapping = dict(zip(zip(shots_df['Date'], shots_df['Team']), shots_df['Shots_L5']))
    df['HT_AvgShots_L5'] = df.apply(lambda x: mapping.get((x['Date'], x['HomeTeam'])), axis=1)
    df['AT_AvgShots_L5'] = df.apply(lambda x: mapping.get((x['Date'], x['AwayTeam'])), axis=1)

    # 5. Shot Accuracy (REPLACED WITH EWMA SPAN 7)
    home_shots = df[['Date', 'HomeTeam', 'HS', 'HST']].copy().rename(columns={'HomeTeam':'Team'})
    away_shots = df[['Date', 'AwayTeam', 'AS', 'AST']].copy().rename(columns={'AwayTeam':'Team'})
    home_shots['Shot_Accuracy'] = home_shots['HST'] / home_shots['HS'].replace(0, np.nan)
    away_shots['Shot_Accuracy'] = away_shots['AST'] / away_shots['AS'].replace(0, np.nan)
    shots_acc_df = pd.concat([home_shots[['Date', 'Team', 'Shot_Accuracy']], away_shots[['Date', 'Team', 'Shot_Accuracy']]], ignore_index=True).sort_values(['Team', 'Date'])
    shots_acc_df['ShotAccuracy_L5'] = shots_acc_df.groupby('Team')['Shot_Accuracy'].transform(get_ewma)
    mapping = dict(zip(zip(shots_acc_df['Date'], shots_acc_df['Team']), shots_acc_df['ShotAccuracy_L5']))
    df['HT_ShotAccuracy_L5'] = df.apply(lambda x: mapping.get((x['Date'], x['HomeTeam'])), axis=1)
    df['AT_ShotAccuracy_L5'] = df.apply(lambda x: mapping.get((x['Date'], x['AwayTeam'])), axis=1)

    # 6. Shot Conversion (REPLACED WITH EWMA SPAN 7)
    ht_shots = df[['Date', 'HomeTeam', 'FTHG', 'HS']].copy().rename(columns={'HomeTeam':'Team'})
    ht_shots['Shot_Conversion'] = np.where(ht_shots['HS'] > 0, ht_shots['FTHG'] / ht_shots['HS'], 0)
    at_shots = df[['Date', 'AwayTeam', 'FTAG', 'AS']].copy().rename(columns={'AwayTeam':'Team'})
    at_shots['Shot_Conversion'] = np.where(at_shots['AS'] > 0, at_shots['FTAG'] / at_shots['AS'], 0)
    shots_conv_df = pd.concat([ht_shots[['Date', 'Team', 'Shot_Conversion']], at_shots[['Date', 'Team', 'Shot_Conversion']]], ignore_index=True).sort_values(['Team', 'Date'])
    shots_conv_df['ShotConversion_L5'] = shots_conv_df.groupby('Team')['Shot_Conversion'].transform(get_ewma)
    mapping = dict(zip(zip(shots_conv_df['Date'], shots_conv_df['Team']), shots_conv_df['ShotConversion_L5']))
    df['HT_ShotConversion_L5'] = df.apply(lambda x: mapping.get((x['Date'], x['HomeTeam'])), axis=1)
    df['AT_ShotConversion_L5'] = df.apply(lambda x: mapping.get((x['Date'], x['AwayTeam'])), axis=1)

    # 7. Clean Sheets (REPLACED WITH EWMA SPAN 7)
    home_record = df[['Date', 'HomeTeam', 'FTAG']].copy().rename(columns={'HomeTeam':'Team', 'FTAG':'GoalsAgainst'})
    home_record['Clean_Sheet'] = np.where(home_record['GoalsAgainst'] > 0, 0, 1)
    away_record = df[['Date', 'AwayTeam', 'FTHG']].copy().rename(columns={'AwayTeam':'Team', 'FTHG':'GoalsAgainst'})
    away_record['Clean_Sheet'] = np.where(away_record['GoalsAgainst'] > 0, 0, 1)
    cs_record = pd.concat([home_record[['Date', 'Team', 'Clean_Sheet']], away_record[['Date', 'Team', 'Clean_Sheet']]], ignore_index=True).sort_values(['Team', 'Date'])
    cs_record['CleanSheet_L5'] = cs_record.groupby('Team')['Clean_Sheet'].transform(get_ewma)
    cs_mapping = dict(zip(zip(cs_record['Date'], cs_record['Team']), cs_record['CleanSheet_L5']))
    df['HT_CS_L5'] = df.apply(lambda x: cs_mapping.get((x['Date'], x['HomeTeam'])), axis=1)
    df['AT_CS_L5'] = df.apply(lambda x: cs_mapping.get((x['Date'], x['AwayTeam'])), axis=1)

    # 8. Win Rate (REPLACED WITH EWMA SPAN 7)
    home_wins = df[['Date', 'HomeTeam', 'FTR']].copy().rename(columns={'HomeTeam':'Team'})
    home_wins['Win'] = np.where(home_wins['FTR'] == 'H', 1, 0)
    away_wins = df[['Date', 'AwayTeam', 'FTR']].copy().rename(columns={'AwayTeam':'Team'})
    away_wins['Win'] = np.where(away_wins['FTR'] == 'A', 1, 0)
    wins_record = pd.concat([home_wins[['Date', 'Team', 'Win']], away_wins[['Date', 'Team', 'Win']]], ignore_index=True).sort_values(['Team', 'Date'])
    wins_record['Wins_L5'] = wins_record.groupby('Team')['Win'].transform(get_ewma)
    win_mapping = dict(zip(zip(wins_record['Date'], wins_record['Team']), wins_record['Wins_L5']))
    df['HT_WinRate_L5'] = df.apply(lambda x: win_mapping.get((x['Date'], x['HomeTeam'])), axis=1)
    df['AT_WinRate_L5'] = df.apply(lambda x: win_mapping.get((x['Date'], x['AwayTeam'])), axis=1)

    # 9. Referee Stats (UNREPLACED - Uses Expanding Mean)
    df['TotalCards'] = (df['HY'] + df['AY'] + df['HR'] + df['AR'])
    df['Ref_Avg_Cards'] = df.groupby('Referee')['TotalCards'].transform(
        lambda x: x.expanding().mean().shift(1))
    df['Ref_Avg_Cards'] = df['Ref_Avg_Cards'].fillna(df['TotalCards'].median())
    df = df.drop(columns='TotalCards', errors='ignore')

    # 10. Last Win Indicator (UNREPLACED)
    df['HT_Win_Indicator'] = (df['FTR'] == 'H').astype(int)
    df['AT_Win_Indicator'] = (df['FTR'] == 'A').astype(int)
    ht_wins = df[['Date', 'HomeTeam', 'HT_Win_Indicator']].rename(columns={'HomeTeam':'Team', 'HT_Win_Indicator':'Win'})
    at_wins = df[['Date', 'AwayTeam', 'AT_Win_Indicator']].rename(columns={'AwayTeam':'Team', 'AT_Win_Indicator':'Win'})
    combined = pd.concat([ht_wins, at_wins], ignore_index=True).sort_values(by=['Team', 'Date']).reset_index(drop=True)
    combined['Last_Win'] = combined.groupby('Team')['Win'].shift(1)
    df = pd.merge(df, combined[['Team', 'Date', 'Last_Win']], left_on=['HomeTeam', 'Date'], right_on=['Team', 'Date'], how='left').rename(columns={'Last_Win': 'HT_Last_Win'}).drop(columns=['Team'])
    df = pd.merge(df, combined[['Team', 'Date', 'Last_Win']], left_on=['AwayTeam', 'Date'], right_on=['Team', 'Date'], how='left').rename(columns={'Last_Win': 'AT_Last_Win'}).drop(columns=['Team'])
    df['HT_Last_Win'] = df['HT_Last_Win'].fillna(0)
    df['AT_Last_Win'] = df['AT_Last_Win'].fillna(0)
    df = df.drop(columns=['HT_Win_Indicator', 'AT_Win_Indicator'], errors='ignore').drop_duplicates() 

    # 11-14. Differentials (UNREPLACED - Now automatically use EWMA inputs)
    df['GD_Diff_L5'] = df['HG_HT_AvgGD_L5'] - df['AG_AT_AvgGD_L5']
    df['Attack_Defense_L5'] = df['HG_HT_AvgGF_L5'] - df['AG_AT_AvgGA_L5']
    df['Overall_Win_Rate_L5'] = df['HT_WinRate_L5'] - df['AT_WinRate_L5']
    df['ShotConversion_Diff_L5'] = df['HT_ShotConversion_L5'] - df['AT_ShotConversion_L5']

    # 15. H2H Points (UNREPLACED - Keep Rolling for long-term matchup history)
    df['HT_Points'] = np.where(df['FTR'] == 'H', 3, np.where(df['FTR'] == 'D', 1, 0))
    df['AT_Points'] = np.where(df['FTR'] == 'A', 3, np.where(df['FTR'] == 'D', 1, 0))
    teams_array = df[['HomeTeam', 'AwayTeam']].astype(str).values
    teams_array.sort(axis=1) 
    df['MatchUp'] = teams_array[:, 0] + "_" + teams_array[:, 1]
    df['H2H_HT_Points_L5'] = df.groupby('MatchUp')['HT_Points'].transform(lambda x: x.shift(1).rolling(5, min_periods=1).sum())
    df['H2H_AT_Points_L5'] = df.groupby('MatchUp')['AT_Points'].transform(lambda x: x.shift(1).rolling(5, min_periods=1).sum())
    df['H2H_HT_Points_L5'] = df['H2H_HT_Points_L5'].fillna(0)
    df['H2H_AT_Points_L5'] = df['H2H_AT_Points_L5'].fillna(0)
    df['H2H_Points_Diff'] = df['H2H_HT_Points_L5'] - df['H2H_AT_Points_L5']
    df = df.drop(columns=['HT_Points', 'AT_Points', 'MatchUp'], errors='ignore')

    return df

def drop_columns(df: pd.DataFrame) -> pd.DataFrame:
    revised_df = df.drop(columns=REMOVABLE_COLUMNS, errors='ignore')
    return revised_df

def data_formatting(df: pd.DataFrame) -> pd.DataFrame:
    df = df[:-1].copy()
    df = df.tail(590).reset_index(drop=True).copy()
    df.loc[:379, 'season'] = 2024
    df.loc[380:, 'season'] = 2025
    df['season'] = df['season'].astype(int)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    return df


# main function
def run_full_feature_engineering_ewma(df: pd.DataFrame) -> pd.DataFrame:
    print("="*156)
    print("="*156)
    print(f"\n{" "*64}STARTING FEATURE ENGINEERING FOR MASTER DATA!\n")
    print("1. Calculating Normalized IP Market Margin...\n")
    df = norm_ip_margin_conversion(df)
    print("2. Converting into IPs & Normalized IPs...\n")
    df = conversion_prob_norm(df)
    print("3. Preparing the data for rolling feature engineering...\n")
    df = date_to_datetime(df)
    print("4. Starting EWMA feature engineering for last 7 matches...")
    df = rolling_feature_engineering_ewma(df)
    print("5. Structuring the data by removing noisy betting odds columns...\n")
    df = drop_columns(df) 
    print("6. Cleaning the data now...\n")
    df = data_cleaning(df)
    print("\n7. Formatting the data now...\n")
    df = data_formatting(df)
    print(f"Shape after feature engineering: {df.shape}\n")
    print(f"{" "*62}FEATURE ENGINEERING COMPLETE!\n")
    return df

