from flask import Flask
from .models import Users, FoodLogs
from .db import db

from flask import Flask, render_template

"""
TODO: make a new folder for routes
"""

# factory pattern to avoid import issues and make it easier for testing later
def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "dev" #dev for testing - change later
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nutrition.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # avoids warnings

    db.init_app(app)

    # a simple page that says hello
    @app.route("/")
    def hello():
        return "<h1>Home Page</h1>"

    @app.route("/users")
    def user_list():
        get_users_stmt = db.select(Users)
        users = db.session.execute(get_users_stmt).scalars().all()

        user_ids = [str(user.id) for user in users]
        return f"User IDs: {', '.join(user_ids)}"
    
    @app.route("/food_log")
    def food_log():
        user = db.session.execute(db.select(Users).where(Users.id==1)).scalars().one()
        food_logs = user.food_logs #food_logs is a list of FoodLog objects

        return render_template("food_logs.html", userid=user.id, food_logs=food_logs)
    

    return app
