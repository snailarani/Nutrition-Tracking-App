from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from .insights_engine import calc_average_nutrients
from datetime import date

"""
TODO: make a new folder for routes
"""


class Base(DeclarativeBase):
    pass

# create sqlalchemy instance to be imported everywhere
db = SQLAlchemy(model_class=Base)

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
        avg = calc_average_nutrients(1, date(2025, 1, 1), date(2025, 12, 31))
        return f"<h1>{avg}</h1>"

    return app
