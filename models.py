from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Float
from typing import List


# Models
class Base(DeclarativeBase):
    pass

# Holds basic information on ALL food in the database
class Food(Base):
    __tablename__ = "food"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(500))
    group_code: Mapped[str] = mapped_column(String(3))

    # To get proximate/inorganic/vitamin data on a particular food
    proximates: Mapped["Proximates"] = relationship(back_populates="food", cascade="all, delete-orphan", uselist=False)
    inorganics: Mapped["Inorganics"] = relationship(back_populates="food", cascade="all, delete-orphan", uselist=False)
    vitamins: Mapped["Vitamins"] = relationship(back_populates="food", cascade="all, delete-orphan", uselist=False)

    # To get the group of a particular food
    group: Mapped["Groups"] = relationship(back_populates="food", cascade="all, delete-orphan", uselist=False)


# Holds data on macros 
class Proximates(Base):
    __tablename__ = "proximates"

    food_id: Mapped[int] = mapped_column(ForeignKey("food.id"), primary_key=True)

    water: Mapped[float] = mapped_column(Float, nullable=False)
    protein: Mapped[float] = mapped_column(Float, nullable=False)
    fat: Mapped[float] = mapped_column(Float, nullable=False)
    carbohydrate: Mapped[float] = mapped_column(Float, nullable=False)
    calories: Mapped[float] = mapped_column(Float, nullable=False)
    sugar: Mapped[float] = mapped_column(Float, nullable=False)

    # Get the food name for a proximate row - do i need this?
    food: Mapped["Food"] = relationship(back_populates="proximates", uselist=False)

# Holds data on inorganics (e.g sodium, calcium)
class Inorganics(Base):
    __tablename__ = "inorganics"

    food_id: Mapped[int] = mapped_column(ForeignKey("food.id"), primary_key=True)

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
class Vitamins(Base):
    __tablename__ = "vitamins"

    food_id: Mapped[int] = mapped_column(ForeignKey("food.id"), primary_key=True)

    vitD: Mapped[float] = mapped_column(Float, nullable=False)
    vitE: Mapped[float] = mapped_column(Float, nullable=False)
    vitB12: Mapped[float] = mapped_column(Float, nullable=False)
    vitC: Mapped[float] = mapped_column(Float, nullable=False)
    
    food: Mapped["Food"] = relationship(back_populates="vitamins", uselist=False)


# Holds group names for each code
class Groups(Base):
    __tablename__ = "groups"

    id: Mapped[str] = mapped_column(ForeignKey("food.group_code"), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    # Get all foods for a particular group
    food: Mapped[List["Food"]] = relationship(back_populates="group")
    