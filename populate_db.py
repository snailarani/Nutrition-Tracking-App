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

# Making column names python compatible 
dfs = [proximates_df, inorganics_df, vitamins_df]
for df in dfs:
    df.columns = (
        df.columns.str.replace(r"\s+", "_", regex=True)  #  Replace spaces with _
        .str.lower()                                     # Convert to lowercase
        .str.replace(r"\(.*", "", regex=True)            # Remove evrything after first ( - we dont need units here
        .str.strip("_")                                 # Remove trailing underscores
    )

print(vitamins_df['food_code'].duplicated().any())

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
    session.execute(delete(Inorganics))
    session.execute(delete(Vitamins))
    session.execute(delete(Proximates))
    session.commit()

    # Populating food table
    all_foods = []
    for food in all_foods_df.itertuples():
        food = Food(
            id = food.food_code,
            name = food.food_name,
            group_id = food.group
        )
        all_foods.append(food)

    session.add_all(all_foods)
    session.commit()

    # For testing
    foods = session.query(Food).all()
    with open("food_dataset/foods.txt", "w") as f:
        for food in foods:
            f.write(f"{food.id}\t{food.name}\t{food.group_id}\n")
        f.write(f"Number of foods: {len(foods)}")



    # Populating proximates table
    prox_rows = []
    for row in proximates_df.itertuples():
        prox = Proximates(
            food_id = row.food_code,
            water = row.water,
            protein = row.protein,
            fat = row.fat,
            carbohydrate = row.carbohydrate,
            calories = row.energy,
            sugar = row.total_sugars
        )
        prox_rows.append(prox)

    session.add_all(prox_rows)
    session.commit()

    proxs = session.query(Proximates).all()
    with open("food_dataset/prox.txt", "w") as f:
        for prox in proxs:
            f.write(f"{prox.food_id}\t{prox.water}\t{prox.protein}\n")
        f.write(f"Number of foods: {len(proxs)}")


    # Populating inorganics table
    inorg_rows = []
    for row in inorganics_df.itertuples():
        inorg = Inorganics(
            food_id = row.food_code,
            sodium = row.sodium,
            potassium = row.potassium,
            calcium = row.calcium,
            magnesium = row.magnesium,
            iron = row.iron,
            copper = row.copper,
            zinc = row.zinc,
            manganese = row.manganese
        )
        inorg_rows.append(inorg)

    session.add_all(inorg_rows)
    session.commit()

    inorgs = session.query(Inorganics).all()
    with open("food_dataset/inorg.txt", "w") as f:
        for inorg in inorgs:
            f.write(f"{inorg.food_id}\t{inorg.sodium}\t{inorg.potassium}\n")
        f.write(f"Number of foods: {len(inorgs)}")


    # Populating vitamins table
    vit_rows = []
    for row in vitamins_df.itertuples():
        vit = Vitamins(
            food_id = row.food_code,
            vitD = row.vitamin_d,
            vitE = row.vitamin_e,
            vitB12 = row.vitamin_b6,
            vitC = row.vitamin_c,
        )
        vit_rows.append(vit)

    session.add_all(vit_rows)
    session.commit()

    vits = session.query(Vitamins).all()
    with open("food_dataset/vits.txt", "w") as f:
        for vit in vits:
            f.write(f"{vit.food_id}\t{vit.vitD}\t{vit.vitE}\n")
        f.write(f"Number of foods: {len(vits)}")