from sqlalchemy import create_engine
from models import Base

# Start with sqlite for now (easier for prototypeing) then migrate to postgres later
engine = create_engine("sqlite:///nutrition.db")

print("Engine run successfully")



