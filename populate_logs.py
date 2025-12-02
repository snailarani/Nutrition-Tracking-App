from sqlalchemy.orm import Session
from sqlalchemy import delete
import pandas as pd
from engine import engine
from models import User, FoodLogs

# Later add login details
def add_user():
    with Session(engine) as session:
        with session.begin():
            user = User()
            session.add(user)
        return user.id


def add_food_log(uid, fcode, quantity, date, date_time):
    log = FoodLogs(
        user_id = uid,
        food_code = fcode,
        quantity = quantity,
        date_created = date,
        date_time_created = date_time
    )

    with Session(engine) as session:
        with session.begin():
            session.add(log)
        return log.id
    

# Temporary
with Session(engine) as session:
    with session.begin():
        session.execute(delete(FoodLogs))

for i in range(20):
    print(add_user())
