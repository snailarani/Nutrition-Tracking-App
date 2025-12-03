from sqlalchemy.orm import Session
from sqlalchemy import delete, select
import pandas as pd
from engine import engine
from models import Users, FoodLogs

# Later add login details
def add_user():
    with Session(engine) as session:
        with session.begin():
            user = Users()
            session.add(user)
        return user.id


def add_food_log(uid, fcode, quantity, date, time):
    log = FoodLogs(
        user_id = uid,
        food_code = fcode,
        quantity = quantity,
        date_created = date,
        time_created = time
    )

    with Session(engine) as session:
        with session.begin():
            session.add(log)
        return log.id
    

# ---------- Seed data - Temporary ------------#
import pandas as pd
from datetime import date, time

with Session(engine) as session:
    with session.begin():
        session.execute(delete(FoodLogs))
        session.execute(delete(Users))

for i in range(20):
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

session = Session(engine)
stmt = select(FoodLogs).where(FoodLogs.user_id.in_([2, 3]))
# for log in session.scalars(stmt):
    # print(log.quantity)
