from db import db
from models import Users, FoodLogs

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