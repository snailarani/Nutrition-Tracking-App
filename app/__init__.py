import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

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
    




    return app
