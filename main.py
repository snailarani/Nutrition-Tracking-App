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

import os
import pandas as pd
import numpy as np

COFID_EXCEL_PATH = "food_dataset/cofid.xlsx"
COFID_PICKLE_PATH = "food_dataset/cofid_pickle"
SHEETS = ["1.3 Proximates", "1.4 Inorganics", "1.5 Vitamins"]

MACROS = ["Energy (kcal) (kcal)", "Energy (kJ) (kJ)", "Protein (g)", "Fat (g)", "Carbohydrate (g)", "Water (g)", "Total sugars (g)"]
VITAMINS = ["Vitamin D (µg)", "Vitamin E (mg)", "Vitamin B6 (mg)", "Vitamin B12 (µg)", "Vitamin C (mg)"]
MINERALS = ["Sodium (mg)", "Potassium (mg)", "Calcium (mg)", "Magnesium (mg)", "Iron (mg)", "Copper (mg)", "Zinc (mg)", "Manganese (mg)"]


def load_data():
    """
    Load data from cofid dataset into data frame
    """
    # If excel sheet not cached - cache it, else load into cofid_dfs
    if not os.path.exists(COFID_PICKLE_PATH):
        cofid = pd.read_excel(COFID_EXCEL_PATH, sheet_name=SHEETS)
        pd.to_pickle(cofid, COFID_PICKLE_PATH)

    cofid_dfs = pd.read_pickle(COFID_PICKLE_PATH)
    return cofid_dfs

def drop_columns(df, keep_columns):
    return df[keep_columns]

def drop_rows(df):
    df = df.replace("N", np.nan)
    df = df.dropna()
    return df

def clean_fields(df, clean_columns):
    for col in df[clean_columns]:
        if col in MACROS or col in VITAMINS:
            df[col] = df[col].replace("Tr", 0.1)
        elif col in MINERALS:
            df[col] = df[col].replace("Tr", 0.01)
    return df

def index_rows(df):
    return df.reset_index(drop=True)
    
def convert_df_numeric(df, numeric_columns):
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)
    return df

def clean_dataframe(df, keep_columns, measure_columns):
    print(measure_columns)
    df = drop_columns(df, keep_columns)
    df = drop_rows(df)
    df= clean_fields(df, measure_columns)
    df = index_rows(df)
    df = convert_df_numeric(df, measure_columns)
    return df

cofid_dfs = load_data()

# Loading the relevant sheets into dataframes
proximates_df = cofid_dfs[SHEETS[0]]
inorganics_df = cofid_dfs[SHEETS[1]]
vitamins_df = cofid_dfs[SHEETS[2]]

proximates_columns = ["Food Code", "Food Name", "Group", "Water (g)", "Protein (g)", "Fat (g)", "Carbohydrate (g)", "Energy (kcal) (kcal)", "Energy (kJ) (kJ)", "Total sugars (g)"]
inorganics_columns = ["Food Code", "Food Name", "Group", "Sodium (mg)", "Potassium (mg)", "Calcium (mg)", "Magnesium (mg)", "Iron (mg)", "Copper (mg)", "Zinc (mg)", "Manganese (mg)"]
vitamins_columns = ["Food Code", "Food Name", "Group", "Vitamin D (µg)", "Vitamin E (mg)", "Vitamin B6 (mg)", "Vitamin B12 (µg)", "Vitamin C (mg)"]

clean_cofid_dfs = [proximates_df, inorganics_df, vitamins_df]
clean_cofid_columns = [proximates_columns, inorganics_columns, vitamins_columns]

for i in range(len(clean_cofid_dfs)):
    df = clean_cofid_dfs[i]
    columns = clean_cofid_columns[i]
    df = clean_dataframe(df, columns, columns[3:])
    df.to_excel("test"+str(i)+".xlsx")


# ---------------- Just in case I need this again --------------------- #

# # Cleaning proximates_df
# # We only need columns: Food Code, Food Name, Group, Water (g), Protein (g), Fat (g), Carbohydrate (g), Energy (kcal) (kcal), Energy (kJ) (kJ)

# # 1. Drop unecessary columns
# proximates_columns = ["Food Code", "Food Name", "Group", "Water (g)", "Protein (g)", "Fat (g)", "Carbohydrate (g)", "Energy (kcal) (kcal)", "Energy (kJ) (kJ)", "Total sugars (g)"]
# proximates_df = proximates_df[proximates_columns]

# # 2. Dropping NaN rows
# # Replace "N" with NaN and drop rows with NaN
# proximates_df = proximates_df.replace("N", np.nan)
# proximates_df = proximates_df.dropna()


# # 3. Cleaning fields
# # Replace values then convert all columns to integers
# proximate_measures = proximates_columns[3:]
# print(proximate_measures)

# for col in proximates_df[proximate_measures]:
#     if col in MACROS or col in VITAMINS:
#         proximates_df[col] = proximates_df[col].replace("Tr", 0.1)
#     elif col in MINERALS:
#         proximates_df[col] = proximates_df[col].replace("Tr", 0.01)

# # print(proximates_df.iloc[:10, :15])
# # print()

# # 4. Re-index rows
# # Once cleaned fields, dropped rows and stuff - re-index rows
# proximates_df = proximates_df.reset_index(drop=True)
# # print(proximates_df.iloc[:10, :15])

# # 5. Convert columns to np/python floats
# # Convert all columns into numbers or smth like that
# proximates_df[proximate_measures] = proximates_df[proximate_measures].apply(pd.to_numeric)
# # print(proximates_df.dtypes)

# proximates_df.to_excel("test.xlsx")

# proximates_df_2 = proximates_df.copy()
# clean_dataframe(proximates_df_2, proximates_columns, proximates_df_2.columns[3:])

