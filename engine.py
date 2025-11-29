import sqlalchemy as db
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy import String


# Start with sqlite for now (easier for prototypeing) then migrate to postgres later
engine = db.create_engine("sqlite:///nutrition.db")



# Models

class Base(DeclarativeBase):
    pass

# Holds basic information on ALL food in the database
class Food(Base):
    __tablename__ = "food"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(500))

    # To get proximate/inorganic/vitamin data on a particular food
    proximates: Mapped["Proximates"] = relationship(back_populates="food")
    inorganics: Mapped["Proximates"] = relationship(back_populates="food")
    vitamins: Mapped["Proximates"] = relationship(back_populates="food")


# Holds data on macros 
class Proximates(Base):
    __tablename__ = "proxmiates"
    pass

# Holds data on inorganics (e.g sodium, calcium)
class Inorganics(Base):
    __tablename__ = "inorganics"
    pass


# Holds data on vitamins
class Vitamins(Base):
    __tablename__ = "vitamins"
    pass