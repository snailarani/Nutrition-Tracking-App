## extracting data
import os
import pandas as pd
import numpy as np

cofid_pickle_path = "food_dataset/cofid_pickle"
cofid_excel_path = "food_dataset/cofid.xlsx"
sheets = ["1.3 Proximates", "1.4 Inorganics", "1.5 Vitamins"]

# If excel sheet not cached - cache it, else load into cofid_dfs
if not os.path.exists(cofid_pickle_path):
    cofid = pd.read_excel("food_dataset/cofid.xlsx", sheet_name=sheets)
    pd.to_pickle(cofid, cofid_pickle_path)

cofid_dfs = pd.read_pickle(cofid_pickle_path)

# Loading the relevant sheets into dataframes
proximates_df = cofid_dfs[sheets[0]]
inorganics_df = cofid_dfs[sheets[1]]
vitamins_df = cofid_dfs[sheets[2]]


# Cleaning time
# trace value represented with Tr
# N - nutrient is present in significant quantities but no reliable information on the amount
"""
https://realpython.com/python-data-cleaning-numpy-pandas/
1. Drop unnecessary columns
2. Change index if needed
3. Tidy fields
4. Clean Columns
5. 

Replacing trace values:
- Will employ these rules for handling trace values:
-- Macronutrients: Tr -> 0.1g/0.1kcal
-- Vitamins: Tr -> 0.1mg
-- Minerals: Tr -> 0.01mg

"""

macros = ["Energy (kcal) (kcal)", "Energy (kJ) (kJ)", "Protein (g)", "Fat (g)", "Carbohydrate (g)", "Water (g)", "Total sugars (g)"]
vitamins = []
minerals = []

# Cleaning proximates_df
# We only need columns: Food Code, Food Name, Group, Water (g), Protein (g), Fat (g), Carbohydrate (g), Energy (kcal) (kcal), Energy (kJ) (kJ)

proximates_columns = ["Food Code", "Food Name", "Group", "Water (g)", "Protein (g)", "Fat (g)", "Carbohydrate (g)", "Energy (kcal) (kcal)", "Energy (kJ) (kJ)", "Total sugars (g)"]
proximate_measures = proximates_columns[3:]
print(proximate_measures)
proximates_df = proximates_df[proximates_columns]

# Replace "N" with NaN and drop rows with NaN
proximates_df = proximates_df.replace("N", np.nan)
proximates_df = proximates_df.dropna()

# Cleaning fields
# Replace values then convert all columns to integers
for col in proximates_df[proximate_measures]:
    if col in macros or col in vitamins:
        proximates_df[col] = proximates_df[col].replace("Tr", 0.1)
    elif col in minerals:
        proximates_df[col] = proximates_df[col].replace("Tr", 0.01)

print(proximates_df.iloc[:10, :15])
print()

# Once cleaned fields, dropped rows and stuff - re-index rows
proximates_df = proximates_df.reset_index(drop= True)
print(proximates_df.iloc[:10, :15])

# Convert all columns into numbers or smth like that
proximates_df[proximate_measures] = proximates_df[proximate_measures].apply(pd.to_numeric)
print(proximates_df.dtypes)