
from .db import db

from app.models import Proximates, Vitamins, Inorganics, FoodLogs, Food
from sqlalchemy import select
from sqlalchemy.sql import func


def calc_daily_nutrition(uid, date_start, date_end):
    session = db.session

    # do the same as calc_average nutrients, but aggregate on day
    # then return dictionary of dictionaries? {day1:{calories:x, water:x, ..}, ...}

    proximates = [col.key for col in(Proximates.__table__.c[1:])]
    inorganics = [col.key for col in(Inorganics.__table__.c[1:])]
    vitamins = [col.key for col in(Vitamins.__table__.c[1:])]

    tables = [Proximates, Inorganics, Vitamins]
    columns = [proximates, inorganics, vitamins]

    nutrient_sum = []
    for i in range(3):
        # Getting all the averages from the columns from each table
        for col in columns[i]:
            date = FoodLogs.date_created
            nutrient_sum.append(
                func.round(
                    func.sum(
                        # Coalesce to fill the empty nutrient values with 0
                        FoodLogs.quantity * func.coalesce(getattr(tables[i], col), 0)
                    ), 2
                ).label(col)
            )

    # Is outer bc not all tables will contain all food items
    stmt = select(
        FoodLogs.date_created.label("date"),
        *nutrient_sum
    ).select_from(FoodLogs)\
    .join(Food, FoodLogs.food_code == Food.id)\
    .join(Proximates, FoodLogs.food_code == Proximates.food_id, isouter=True)\
    .join(Inorganics, FoodLogs.food_code == Inorganics.food_id, isouter=True)\
    .join(Vitamins, FoodLogs.food_code == Vitamins.food_id, isouter=True)\
    .where(FoodLogs.user_id == uid)\
    .where(FoodLogs.date_created >= date_start)\
    .where(FoodLogs.date_created <= date_end)\
    .group_by(FoodLogs.date_created)
        

    daily_sums = session.execute(stmt).all()

    daily_sums_dict = {}
    for day in daily_sums:
        nutrients_dict = dict(day._mapping)
        date = str(nutrients_dict["date"])
        nutrients_dict.pop("date")
        daily_sums_dict[date] = nutrients_dict
        
    return daily_sums_dict



def calc_weekly_nutrition():
    pass


# This works, just need to make it look nicer
def calc_average_nutrients(uid, date_start, date_end):
    session = db.session

    proximates = [col.key for col in(Proximates.__table__.c[1:])]
    inorganics = [col.key for col in(Inorganics.__table__.c[1:])]
    vitamins = [col.key for col in(Vitamins.__table__.c[1:])]

    tables = [Proximates, Inorganics, Vitamins]
    columns = [proximates, inorganics, vitamins]

    nutrient_avg = []
    for i in range(3):
        # Getting all the averages from the columns from each table
        for col in columns[i]:
            nutrient_avg.append(
                # Coalesce to fill the empty nutrient values with 0
                func.coalesce(
                    func.round(
                        func.avg(FoodLogs.quantity * getattr(tables[i], col)), 2
                    ), 0
                )
                .label(col)
            )

    # Is outer bc not all tables will contain all food items
    stmt = select(*nutrient_avg
        # func.avg(FoodLogs.quantity*Proximates.calories),
        # func.avg(FoodLogs.quantity*Proximates.carbohydrate),
        # func.avg(FoodLogs.quantity*Proximates.protein),
        # func.avg(FoodLogs.quantity*Proximates.water),
        # func.avg(FoodLogs.quantity*Proximates.fat),
        # func.avg(FoodLogs.quantity*Proximates.sugar),
    ).select_from(FoodLogs)\
    .join(Proximates, FoodLogs.food_code == Proximates.food_id, isouter=True)\
    .join(Inorganics, FoodLogs.food_code == Inorganics.food_id, isouter=True)\
    .join(Vitamins, FoodLogs.food_code == Vitamins.food_id, isouter=True)\
    .where(FoodLogs.user_id == uid)\
    .where(FoodLogs.date_created >= date_start)\
    .where(FoodLogs.date_created <= date_end)

    averages = session.execute(stmt).all()

    return averages[0]._mapping



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
    food_logs = session.scalars(get_food_stmt).all()

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
        
    nutrient_sums = {nutr: round(val,2) for nutr, val in nutrient_sums.items()}

    return nutrient_sums


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

    proximates_sums = calc_nutrient_sums(Proximates, "proximates", food_logs)
    inorganics_sums = calc_nutrient_sums(Inorganics, "inorganics", food_logs)
    vitamins_sums = calc_nutrient_sums(Vitamins, "vitamins", food_logs)


    return [proximates_sums, inorganics_sums, vitamins_sums]
    
    
    
