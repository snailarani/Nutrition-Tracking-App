from engine import engine
from models import Food, Proximates, Vitamins, Inorganics, Users, FoodLogs
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date

print(engine.url)

def calc_nutrition_range(uid, date_start, date_end):
    pass


calc_nutrition_range(2, date(2025, 11, 1), date(2025, 12, 31))

def calc_daily_nutrition():
    pass

def calc_weekly_nutrition():
    pass
