from sqlalchemy.orm import Session
from sqlalchemy import create_engine, delete
import pandas as pd
from engine import engine
from models import Proximates, Inorganics, Vitamins, Food


## TODO: maybe move loading/cleaning data functions here?

cofid_path = "food_dataset/cofid_clean.xlsx"

proximates_df = pd.read_excel(cofid_path, sheet_name="proximates")
inorganics_df = pd.read_excel(cofid_path, sheet_name="inorganics")
vitamins_df = pd.read_excel(cofid_path, sheet_name="vitamins")

# Making column names python compatible (removing spaces, non-alphanumeric characters and making them lowercase)
dfs = [proximates_df, inorganics_df, vitamins_df]
for df in dfs:
    df.columns = df.columns.str.replace(' ', '_', regex=True).str.lower().str.replace(r'\s+', '_', regex=True) 


# Inserting cofid data into sql table
proximates_df.to_sql("proximates", con=engine, if_exists="replace", index=False)
inorganics_df.to_sql("inorganics", con=engine, if_exists="replace", index=False)
vitamins_df.to_sql("vitamins", con=engine, if_exists="replace", index=False)

# Getting all foods from all tables:
food_series = []
food_columns = ["food_code", "food_name", "group"]
all_foods_df = pd.concat([proximates_df[food_columns], 
                          inorganics_df[food_columns], 
                          vitamins_df[food_columns]])

# Remove duplicate foods
all_foods_df = all_foods_df.drop_duplicates(subset="food_code")


# Populating database

# Populate Food first
with Session(engine) as session:

    # Temporary
    session.execute(delete(Food))
    session.commit()

    all_foods = []
    for food in all_foods_df.itertuples():
        # print(food)
        food = Food(
            id = food.food_code,
            name = food.food_name,
            group_id = food.group
        )
        all_foods.append(food)
    session.add_all(all_foods)

    session.commit()

    foods = session.query(Food).all()
    print(f"Number of foods: {len(foods)}")

    for food in foods[:5]:
        print(food.id, food.name, food.group_id)

    


