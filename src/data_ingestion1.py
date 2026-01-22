# this file is responsible for reading premier league matches from 2000 to 2025 season, organised in csv files

import os
import glob
import pandas as pd
from typing import List

DIRECTORY = r'C:\PROJECT\data\raw-data\match-data-1' # main directory consisting of csv files

def load_merge_pl_data(data_directory: str = DIRECTORY) -> pd.DataFrame:
    print()
    print("="*156)
    print("="*156)
    print(f"\n{" "*66}LOADING THE MASTER DATA!\n")

    # access the csv files, named as pl0.csv, pl1.csv, pl2.csv and so on 
    files = glob.glob(os.path.join(data_directory, 'pl*.csv'))  

    # chronologically sort the files based on the number in the nomenclature of the file
    try:
        files = sorted(files, key=lambda x: int(os.path.basename(x).replace('pl', '').replace('.csv', ''))) 
    except ValueError:
        print("Warning: Could not sort files chronologically. Ensure filenames are 'pl[number].csv'")

    good_df: List[pd.DataFrame] = []
    bad_files: List[str] = []
    print(f"{len(files)} files found. Checking for errors now!\n")

    for file in files:
        try:
            # if no error is found for a file, append the file to the 'good_df' list
            temp_df = pd.read_csv(file)
            good_df.append(temp_df)
        except Exception as e:
            # print the error along with the file path and name & append the file to the 'bad_df' list
            bad_files.append(file)
            print(f"Error: {e}")
            print(f"File: {os.path.basename(file)}\n")
    
    # resolving errors in the files
    print("Resolving the errors now!")
    pl3_path = os.path.join(data_directory, 'pl3.csv')
    try:
        pl3 = pd.read_csv(pl3_path, sep=",", engine='python', header=0, on_bad_lines="skip")
        insert_index = 3 
        if pl3_path in bad_files:
            bad_files.remove(pl3_path)
        good_df.insert(insert_index, pl3)        
    except Exception as e:
        print(f"Failed to resolve errors in pl3.csv: {e}")
    pl4_path = os.path.join(data_directory, 'pl4.csv')
    try:
        pl4 = pd.read_csv(pl4_path, sep=",", engine='python', header=0, on_bad_lines="skip", encoding="latin1")
        insert_index = 4
        if pl4_path in bad_files:
            bad_files.remove(pl4_path)
        good_df.insert(insert_index, pl4)
    except Exception as e:
        print(f"Failed to resolve errors in pl4.csv: {e}")

    if bad_files:
        print(f"Final Warning: Could not resolve the following files: {[os.path.basename(f) for f in bad_files]}")
    else: print("\nAll errors have been successfully resolved!\n")
    if not good_df:
        raise ValueError("No good dataframes were successfully loaded or resolved!\n")
    
    # finally, concatenate all the data into a single dataframe
    original_df = pd.concat(good_df, ignore_index=True)
    print(f"Original Shape: {original_df.shape}\n")
    
    print(f"{" "*63}MASTER DATA LOADING COMPLETE!\n")
    return original_df