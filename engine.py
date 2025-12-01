from sqlalchemy import create_engine
from models import Base

# Start with sqlite for now (easier for prototypeing) then migrate to postgres later
engine = create_engine("sqlite:///nutrition.db")

Base.metadata.drop_all(engine)

# Create the tables
Base.metadata.create_all(engine)

