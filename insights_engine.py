from engine import engine
from models import Food, Proximates, Vitamins, Inorganics, Users, FoodLogs
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date

# TODO: handle none values (e.g when food has no vitamins)
# Skip if vitamins data is missing
# if food_vits is None:
# continue
def calc_nutrition_range(uid, date_start, date_end):
    session = Session(engine)
    # Get all foods from logs with uid in date range
    get_food_stmt = (
        select(FoodLogs)
        .where(FoodLogs.user_id == uid)
        .where(FoodLogs.date_created >= date_start)
        .where(FoodLogs.date_created <= date_end)
    )

    # List of all food logs
    food_logs = session.scalars(get_food_stmt).all()

    proximates_sums = calculate_nutrient_sums(Proximates, food_logs, "proximates")
    inorganics_sums = calculate_nutrient_sums(Inorganics, food_logs, "inorganics")
    vitamins_sums = calculate_nutrient_sums(Vitamins, food_logs, "vitamins")


    print(proximates_sums)
    print(inorganics_sums)
    print(vitamins_sums)



# Calculates nutrient sums for a particular table (proximates, inorganics, vitamins)
def calculate_nutrient_sums(table, food_logs, table_name):
    # Getting all nutrients from the proximates table
    nutrient_cols = [col.key for col in(table.__table__.c[1:])]
    nutrient_sums = {n:0 for n in nutrient_cols}

    # For each proximate, find the total value 
    for log in food_logs:
        food = log.food
        food_nutrients = getattr(food, table_name)
        for n in nutrient_cols:
            nutrient_sums[n] += log.quantity * getattr(food_nutrients, n)

    return nutrient_sums



calc_nutrition_range(18, date(2025, 1, 1), date(2025, 12, 31))

def calc_daily_nutrition():
    pass

def calc_weekly_nutrition():
    pass
