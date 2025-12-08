"""
https://realpython.com/python-data-cleaning-numpy-pandas/
1. Drop unnecessary columns and rows
2. Clean fields (handle tr)
3. Change index if needed
4. Convert columns to right type

Replacing trace values:
- Will employ these rules for handling trace values:
-- Macronutrients: Tr -> 0.1g/0.1kcal
-- Vitamins: Tr -> 0.1mg/0.1µg
-- Minerals: Tr -> 0.01mg

TODO:
- get rid of Energy(Kj) in Proximates

"""

import os
import pandas as pd
import numpy as np


def main():

    COFID_EXCEL_PATH = "data/cofid.xlsx"
    COFID_PICKLE_PATH = "data/cofid_pickle"
    SHEETS = ["1.3 Proximates", "1.4 Inorganics", "1.5 Vitamins"]
    COFID_OUTPUT_PATH = "data/cofid_clean.xlsx"

    MACROS = ["Energy (kcal) (kcal)", "Protein (g)", "Fat (g)", "Carbohydrate (g)", "Water (g)", "Total sugars (g)"]
    VITAMINS = ["Vitamin D (µg)", "Vitamin E (mg)", "Vitamin B6 (mg)", "Vitamin B12 (µg)", "Vitamin C (mg)"]
    MINERALS = ["Sodium (mg)", "Potassium (mg)", "Calcium (mg)", "Magnesium (mg)", "Iron (mg)", "Copper (mg)", "Zinc (mg)", "Manganese (mg)"]

    BASE_COLUMNS = ["Food Code", "Food Name", "Group"]

    def load_data():
        # If excel sheet not cached - cache it, else load into cofid_dfs
        if not os.path.exists(COFID_PICKLE_PATH):
            cofid = pd.read_excel(COFID_EXCEL_PATH, sheet_name=SHEETS)
            pd.to_pickle(cofid, COFID_PICKLE_PATH)

        cofid_dfs = pd.read_pickle(COFID_PICKLE_PATH)
        return cofid_dfs

    def clean_dataframe(df, keep_columns, measure_columns):
        # Drop uneeded columns and rows with 'N' or empty values
        df = df[keep_columns].replace("N", np.nan).dropna()
        # Clean fields in the columns with numeric measurements
        for col in df[measure_columns]:
            if col in MACROS or col in VITAMINS:
                df[col] = df[col].replace("Tr", 0.1)
            elif col in MINERALS:
                df[col] = df[col].replace("Tr", 0.01)
        # Re-index rows
        df = df.reset_index(drop=True)
        # Convert columns with numeric measurements into np/python float types
        df[measure_columns] = df[measure_columns].apply(pd.to_numeric)
        return df


    cofid_dfs = load_data()

    # Loading the relevant sheets into dataframes
    proximates_df = cofid_dfs[SHEETS[0]]
    inorganics_df = cofid_dfs[SHEETS[1]]
    vitamins_df = cofid_dfs[SHEETS[2]]

    proximates_columns = BASE_COLUMNS + ["Water (g)", "Protein (g)", "Fat (g)", "Carbohydrate (g)", "Energy (kcal) (kcal)", "Total sugars (g)"]
    inorganics_columns = BASE_COLUMNS + ["Sodium (mg)", "Potassium (mg)", "Calcium (mg)", "Magnesium (mg)", "Iron (mg)", "Copper (mg)", "Zinc (mg)", "Manganese (mg)"]
    vitamins_columns = BASE_COLUMNS + ["Vitamin D (µg)", "Vitamin E (mg)", "Vitamin B6 (mg)", "Vitamin B12 (µg)", "Vitamin C (mg)"]

    cofid_dfs_dict = {
        "proximates": [proximates_df, proximates_columns],
        "inorganics": [inorganics_df, inorganics_columns],
        "vitamins": [vitamins_df, vitamins_columns]
    }

    clean_cofid_dfs = [proximates_df, inorganics_df, vitamins_df]
    clean_cofid_columns = [proximates_columns, inorganics_columns, vitamins_columns]



    with pd.ExcelWriter(COFID_OUTPUT_PATH) as writer:
        for name, df_items in cofid_dfs_dict.items():
            df = df_items[0]
            columns = df_items[1]
            df = clean_dataframe(df, columns, columns[3:])
            df.to_excel(writer, sheet_name=name, index=False)

if __name__ == "__main__":
    main()

# Converting to dataframes to populate SQLAlchemy tables



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

