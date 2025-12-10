
from .db import db

from app.models import Proximates, Vitamins, Inorganics, FoodLogs, Food
from sqlalchemy import select
from sqlalchemy.sql import func


def calc_daily_nutrition():
    pass

def calc_weekly_nutrition():
    pass


def calc_average_nutrients(uid, date_start, date_end):
    session = db.session

    stmt = select(
        func.avg(FoodLogs.quantity*Proximates.calories),
        func.avg(FoodLogs.quantity*Proximates.carbohydrate),
        func.avg(FoodLogs.quantity*Proximates.protein),
        func.avg(FoodLogs.quantity*Proximates.water),
        func.avg(FoodLogs.quantity*Proximates.fat),
        func.avg(FoodLogs.quantity*Proximates.sugar),
    ).select_from(FoodLogs)\
        .join(Proximates, FoodLogs.food_code == Proximates.food_id)\
        .where(FoodLogs.user_id == uid)\
        .where(FoodLogs.date_created >= date_start)\
        .where(FoodLogs.date_created <= date_end)

    averages = session.execute(stmt).all()

    return averages



# Gets all the food logs for a particular user within a particular date range
def get_logs_in_date_range(uid, date_start, date_end):
    session = db.session
    # Get all foods from logs with uid in date range
    get_food_stmt = (
        select(FoodLogs)
        .where(FoodLogs.user_id == uid)
        .where(FoodLogs.date_created >= date_start)
        .where(FoodLogs.date_created <= date_end)
    )

    # List of all food logs
    food_logs = session.query(get_food_stmt)

    proximates_sums = calculate_nutrient_sums(Proximates, "proximates", food_logs)
    inorganics_sums = calculate_nutrient_sums(Inorganics, "inorganics", food_logs)
    vitamins_sums = calculate_nutrient_sums(Vitamins, "vitamins", food_logs)


    print(proximates_sums)
    print(inorganics_sums)
    print(vitamins_sums)



def calc_daily_nutrition():
    pass

def calc_weekly_nutrition():
    pass


def calc_average_nutrients(uid, date_start, date_end):
    session = db.session

    stmt = select(
        func.avg(FoodLogs.quantity*Proximates.calories),
        func.avg(FoodLogs.quantity*Proximates.carbohydrate),
        func.avg(FoodLogs.quantity*Proximates.protein),
        func.avg(FoodLogs.quantity*Proximates.water),
        func.avg(FoodLogs.quantity*Proximates.fat),
        func.avg(FoodLogs.quantity*Proximates.sugar),
    ).select_from(FoodLogs)\
        .join(Proximates.food_id)\
        .join(Inorganics.food_id)\
        .join(Vitamins.food_id)\
        .where(FoodLogs.user_id == uid)\
        .where(FoodLogs.date_created >= date_start)\
        .where(FoodLogs.date_created <= date_end)

    averages = session.execute(stmt).all()

    return averages



# Gets all the food logs for a particular user within a particular date range
def get_logs_in_date_range(uid, date_start, date_end):
    session = db.session
    # Get all foods from logs with uid in date range
    get_food_stmt = (
        select(FoodLogs)
        .where(FoodLogs.user_id == uid)
        .where(FoodLogs.date_created >= date_start)
        .where(FoodLogs.date_created <= date_end)
    )

    # List of all food logs
    food_logs = session.query(get_food_stmt)

    return food_logs


# Calculates nutrient sums for a particular table (proximates, inorganics, vitamins)
def calc_nutrient_sums(table, table_name, food_logs):
    # Getting all nutrients from the proximates table
    nutrient_cols = [col.key for col in(table.__table__.c[1:])]
    nutrient_sums = {n:0 for n in nutrient_cols}

    # Rewrite this with sqlalchemy sum functions

    # For each proximate, find the total value 
    for log in food_logs:
        food = log.food
        food_nutrients = getattr(food, table_name)
        # If food has empty value for a particular nutrient, it has no values for this nutrient table
        if food_nutrients == None:
            continue
        for n in nutrient_cols:
            nutrient_sums[n] += log.quantity * getattr(food_nutrients, n)

    return nutrient_sums



calc_nutrition_range(18, date(2025, 1, 1), date(2025, 12, 31))

def calc_daily_nutrition():
    pass

def calc_weekly_nutrition():
    pass

