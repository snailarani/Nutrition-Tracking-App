from app import db

from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey, String, Float, Integer, Date, Time
from typing import List
from datetime import date, time


"""
TODO: Add checks for invalid entries
"""


# Holds basic information on ALL food in the database
class Food(db.Model):
    __tablename__ = "food"

    id: Mapped[str] = mapped_column(String(7), primary_key=True)
    name: Mapped[str] = mapped_column(String(500))
    group_id: Mapped[str] = mapped_column(ForeignKey("groups.id"))

    # To get proximate/inorganic/vitamin data on a particular food
    proximates: Mapped["Proximates"] = relationship(back_populates="food", cascade="all, delete-orphan", uselist=False)
    inorganics: Mapped["Inorganics"] = relationship(back_populates="food", cascade="all, delete-orphan", uselist=False)
    vitamins: Mapped["Vitamins"] = relationship(back_populates="food", cascade="all, delete-orphan", uselist=False)

    # To get the group of a particular food
    group: Mapped["Groups"] = relationship(back_populates="food", uselist=False)


# Holds data on macros 
class Proximates(db.Model):
    __tablename__ = "proximates"

    food_id: Mapped[str] = mapped_column(ForeignKey("food.id"), primary_key=True)

    water: Mapped[float] = mapped_column(Float, nullable=False)
    protein: Mapped[float] = mapped_column(Float, nullable=False)
    fat: Mapped[float] = mapped_column(Float, nullable=False)
    carbohydrate: Mapped[float] = mapped_column(Float, nullable=False)
    calories: Mapped[float] = mapped_column(Float, nullable=False)
    sugar: Mapped[float] = mapped_column(Float, nullable=False)

    # Get the food name for a proximate row - do i need this?
    food: Mapped["Food"] = relationship(back_populates="proximates", uselist=False)

# Holds data on inorganics (e.g sodium, calcium)
class Inorganics(db.Model):
    __tablename__ = "inorganics"

    food_id: Mapped[str] = mapped_column(ForeignKey("food.id"), primary_key=True)

    sodium: Mapped[float] = mapped_column(Float, nullable=False)
    potassium: Mapped[float] = mapped_column(Float, nullable=False)
    calcium: Mapped[float] = mapped_column(Float, nullable=False)
    magnesium: Mapped[float] = mapped_column(Float, nullable=False)
    iron: Mapped[float] = mapped_column(Float, nullable=False)
    copper: Mapped[float] = mapped_column(Float, nullable=False)
    zinc: Mapped[float] = mapped_column(Float, nullable=False)
    manganese: Mapped[float] = mapped_column(Float, nullable=False)
    
    food: Mapped["Food"] = relationship(back_populates="inorganics", uselist=False)


# Holds data on vitamins
class Vitamins(db.Model):
    __tablename__ = "vitamins"

    food_id: Mapped[str] = mapped_column(ForeignKey("food.id"), primary_key=True)

    vitD: Mapped[float] = mapped_column(Float, nullable=False)
    vitE: Mapped[float] = mapped_column(Float, nullable=False)
    vitB12: Mapped[float] = mapped_column(Float, nullable=False)
    vitC: Mapped[float] = mapped_column(Float, nullable=False)
    
    food: Mapped["Food"] = relationship(back_populates="vitamins", uselist=False)


# Holds group names for each code
class Groups(db.Model):
    __tablename__ = "groups"

    id: Mapped[str] = mapped_column(String(3), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    # Get all foods for a particular group
    food: Mapped[List["Food"]] = relationship(back_populates="group")
    

# Holds recommended daily intake of nutrients
# Keep all data in one table for now, maybe normalise later
class DailyIntake(db.Model):
    __tablename__ = "dailyintake"

    id: Mapped[int] = mapped_column(primary_key=True)

    sex: Mapped[str] = mapped_column(String(1), nullable=False)
    age_min: Mapped[int] = mapped_column(Integer, nullable=False)
    age_max: Mapped[int] = mapped_column(Integer, nullable=False)
    nutrient: Mapped[str] = mapped_column(String(20), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    



# ---------- Put this here for now, can move later ---------- #
class Users(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    # age: Mapped[int] = mapped_column(Integer, nullable=False)
    # sex: Mapped[str] = mapped_column(String(1), nullable=False)

    food_logs: Mapped[List["FoodLogs"]] = relationship(back_populates="user")

    # username: Mapped[str] = mapped_column(String(100))
    # password: Mapped[str] = mapped_column(String(100))


class FoodLogs(db.Model):
    __tablename__ = "foodlog"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    food_code: Mapped[str] = mapped_column(ForeignKey("food.id"), nullable=False) #False for now but will change when meals are added
    # nutrient measurements taken per 100g
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    date_created: Mapped[date] = mapped_column(Date, nullable=False)
    time_created: Mapped[time] = mapped_column(Time, nullable=False)

    user: Mapped["Users"] = relationship(back_populates="food_logs", uselist=False)
    # May want to turn this into a bidirectional relationship later
    food: Mapped["Food"] = relationship("Food", uselist=False)

# Stores pre made meals - for later!
# class UserMeals(Base):
#     __tablename__ = "usermeals"
#     pass


