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

    # Getting all nutrients from the proximates table
    proximates = [col.key for col in(Proximates.__table__.c[1:])]
    proximates_sums = {p:0 for p in proximates}

    # For each proximate, find the total value 
    for log in food_logs:
        print(log.food_code)
        food = log.food
        food_prox = food.proximates
        for p in proximates:
            proximates_sums[p] += log.quantity * getattr(food_prox, p)
        

    # Getting all nutrients from the inorganics table
    inorganics = [col.key for col in(Inorganics.__table__.c[1:])]
    inorganics_sums = {i:0 for i in inorganics}

    # For each inorganics, find the total value 
    for log in food_logs:
        food = log.food
        food_inorg = food.inorganics
        for i in inorganics:
            inorganics_sums[i] += log.quantity * getattr(food_inorg, i)


    # Getting all nutrients from the vitamins table
    vitamins = [col.key for col in(Vitamins.__table__.c[1:])]
    vitamins_sums = {v:0 for v in vitamins}

    # For each vitamins, find the total value 
    for log in food_logs:
        food = log.food
        food_vits = food.vitamins
        for v in vitamins:
            vitamins_sums[v] += log.quantity * getattr(food_vits, v)


    print(proximates_sums)
    print(inorganics_sums)
    print(vitamins_sums)

             

calc_nutrition_range(2, date(2025, 1, 1), date(2025, 12, 31))

def calc_daily_nutrition():
    pass

def calc_weekly_nutrition():
    pass
