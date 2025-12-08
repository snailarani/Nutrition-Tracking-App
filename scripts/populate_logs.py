
from app import db
from app.models import Users, FoodLogs

from sqlalchemy import delete, select
import pandas as pd

from datetime import date, time


# Later add login details
def add_user():
    user = Users()
    db.session.add(user)
    db.session.commit()
    return user.id


def add_food_log(uid, fcode, quantity, date, time):
    log = FoodLogs(
        user_id = uid,
        food_code = fcode,
        quantity = quantity,
        date_created = date,
        time_created = time
    )
    db.session.add(log)
    db.session.commit()
    return log.id
    

def main():
    # ---------- Seed data - Temporary ------------#
    db.session.execute(delete(FoodLogs))
    db.session.execute(delete(Users))
    db.session.commit()

    for i in range(21):
        add_user()

    food_logs_df = pd.read_csv("seed_data/seed_food_logs", header=0)

    print(food_logs_df.head(10))

    # Populating food logs table with seed data
    for i, row in food_logs_df.iterrows():
        add_food_log(
            int(row["user_id"]),
            str(row["food_code"]),
            float(row["quantity"]),
            date(int(row["year"]), int(row["month"]), int(row["day"])),
            time(int(row["hour"]), int(row["minute"]))
        )


    stmt = select(FoodLogs).where(FoodLogs.user_id.in_([2, 3]))
    print(db.session.scalars(stmt).all())
    # for log in session.scalars(stmt):
        # print(log.quantity)
