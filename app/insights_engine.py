
from .db import db

from app.models import Proximates, Vitamins, Inorganics, FoodLogs
from sqlalchemy import select

# Returns a list of dictionaries of the sums of the nutrients consumed in a particular time period
def calc_nutrition_range(uid, date_start, date_end):
    session = db.session
    # Get all foods from logs with uid in date range
    get_food_stmt = (
        select(FoodLogs)
        .where(FoodLogs.user_id == uid)
        .where(FoodLogs.date_created >= date_start)
        .where(FoodLogs.date_created <= date_end)
    )

    # List of all food logs
    food_logs = session.scalars(get_food_stmt).all()

    proximates_sums = calculate_nutrient_sums(Proximates, "proximates", food_logs)
    inorganics_sums = calculate_nutrient_sums(Inorganics, "inorganics", food_logs)
    vitamins_sums = calculate_nutrient_sums(Vitamins, "vitamins", food_logs)

    return [proximates_sums, inorganics_sums, vitamins_sums]



# Calculates nutrient sums for a particular table (proximates, inorganics, vitamins)
def calculate_nutrient_sums(table, table_name, food_logs):
    # Getting all nutrients from the proximates table
    nutrient_cols = [col.key for col in(table.__table__.c[1:])]
    nutrient_sums = {n:0 for n in nutrient_cols}

    # For each proximate, find the total value 
    for log in food_logs:
        food = log.food
        food_nutrients = getattr(food, table_name)
        # If food has empty value for a particular nutrient, it has no values for this nutrient table
        if food_nutrients == None:
            continue
        for n in nutrient_cols:
            nutrient_sums[n] += log.quantity * getattr(food_nutrients, n)

    # Round all values to 2.d.p
    nutrient_sums = {nutrient: round(value, 2) for nutrient, value in nutrient_sums.items()}

    return nutrient_sums


def calc_daily_nutrition():
    pass

def calc_weekly_nutrition():
    pass

