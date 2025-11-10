## extracting data
import os
import pandas as pd
import numpy as np

cofid_pickle_path = "food_dataset/cofid_pickle"
cofid_excel_path = "food_dataset/cofid.xlsx"
sheets = ["1.2 Factors", "1.3 Proximates", "1.4 Inorganics", "1.5 Vitamins"]

# If excel sheet not cached - cache it, else load into cofid_dfs
if not os.path.exists(cofid_pickle_path):
    cofid = pd.read_excel("food_dataset/cofid.xlsx", sheet_name=sheets)
    pd.to_pickle(cofid, cofid_pickle_path)

cofid_dfs = pd.read_pickle(cofid_pickle_path)

factors_df = cofid_dfs[sheets[0]]
proximates_df = cofid_dfs[sheets[1]]
inorganics_df = cofid_dfs[sheets[2]]
vitamins_df = cofid_dfs[sheets[3]]

print(factors_df.head(), "\n")


# for name, df in cofid_dfs.items():
#     print(f"--- {name} ---")
#     print(df.head(), "\n")




