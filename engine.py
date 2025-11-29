import sqlalchemy as db
from models import Base

# Start with sqlite for now (easier for prototypeing) then migrate to postgres later
engine = db.create_engine("sqlite:///nutrition.db")

# Create the tables
Base.metadata.create_all(engine)

