
from app import create_app, db
from app.models import Proximates, Inorganics, Vitamins, Food, Groups, DailyIntake

from sqlalchemy import delete
import pandas as pd

"""
TODO: maybe move loading/cleaning data functions here?
TODO: use batch commits instead - will refactor this entire file later
"""

def main():

    app = create_app()

    with app.app_context():

        cofid_path = "data/cofid_clean.xlsx"

        proximates_df = pd.read_excel(cofid_path, sheet_name="proximates")
        inorganics_df = pd.read_excel(cofid_path, sheet_name="inorganics")
        vitamins_df = pd.read_excel(cofid_path, sheet_name="vitamins")
        groups_df = pd.read_csv("data/food_groups.txt")
        daily_nutrition_df = pd.read_csv("data/daily_nutrition.txt")

        # Making column names python compatible 
        dfs = [proximates_df, inorganics_df, vitamins_df, groups_df, daily_nutrition_df]
        for df in dfs:
            df.columns = (
                df.columns.str.replace(r"\s+", "_", regex=True)  #  Replace spaces with _
                .str.lower()                                     # Convert to lowercase
                .str.replace(r"\(.*", "", regex=True)            # Remove evrything after first ( - we dont need units here
                .str.strip("_")                                 # Remove trailing underscores
            )

        # print(daily_nutrition_df['food_code'].duplicated().any())

        # Getting all foods from all tables:
        food_columns = ["food_code", "food_name", "group"]
        all_foods_df = pd.concat([proximates_df[food_columns], 
                                inorganics_df[food_columns], 
                                vitamins_df[food_columns]])

        # Remove duplicate foods
        all_foods_df = all_foods_df.drop_duplicates(subset="food_code")

        # print(daily_nutrition_df)

        # Populating database
        # Temporary So that we don't keep populating the table multiple times
        db.session.execute(delete(Food))
        db.session.execute(delete(Inorganics))
        db.session.execute(delete(Vitamins))
        db.session.execute(delete(Proximates))
        db.session.execute(delete(Groups))
        db.session.execute(delete(DailyIntake))
        db.session.commit()

        # Populating food table
        all_foods = []
        for food in all_foods_df.itertuples():
            food = Food(
                id = food.food_code,
                name = food.food_name,
                group_id = food.group
            )
            all_foods.append(food)

        db.session.add_all(all_foods)
        db.session.commit()

        # For testing
        foods = db.session.query(Food).all()
        with open("data/foods.txt", "w") as f:
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

        db.session.add_all(prox_rows)
        db.session.commit()

        proxs = db.session.query(Proximates).all()
        with open("data/prox.txt", "w") as f:
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

        db.session.add_all(inorg_rows)
        db.session.commit()

        inorgs = db.session.query(Inorganics).all()
        with open("data/inorg.txt", "w") as f:
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

        db.session.add_all(vit_rows)
        db.session.commit()

        vits = db.session.query(Vitamins).all()
        with open("data/vits.txt", "w") as f:
            for vit in vits:
                f.write(f"{vit.food_id}\t{vit.vitD}\t{vit.vitE}\n")
            f.write(f"Number of foods: {len(vits)}")


        # Populating group table
        group_rows = []
        for row in groups_df.itertuples():
            group = Groups(
                id = row.code,
                name = row.category
            )
            group_rows.append(group)

        db.session.add_all(group_rows)
        db.session.commit()

        groups = db.session.query(Groups).all()
        with open("data/groups.txt", "w") as f:
            for g in groups:
                f.write(f"{g.id}\t{g.name}\n")
            f.write(f"Number of foods: {len(groups)}")


        # Populating daily nutrition table
        daily_rows = []
        for row in daily_nutrition_df.itertuples():
            daily = DailyIntake(
                sex = row.sex,
                age_min = row.age_min,
                age_max = row.age_max,
                nutrient = row.nutrient,
                value = row.value
            )
            daily_rows.append(daily)
        db.session.add_all(daily_rows)
        db.session.commit()


        # daily = db.session.query(DailyIntake).all()
        # with open("data/ahhh.txt", "w") as f:
        #     for d in daily:
        #         print(f"{d.nutrient}\t{d.value}\t{d.age_min}\t{d.sex}\n")
        #     print(f"Number of reccs: {len(daily)}")

if __name__ == "__main__":
    main()