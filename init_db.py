from engine import engine
from models import Base

# Create the tables
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)