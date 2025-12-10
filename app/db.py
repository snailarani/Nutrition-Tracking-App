
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# create sqlalchemy instance to be imported everywhere
db = SQLAlchemy(model_class=Base)