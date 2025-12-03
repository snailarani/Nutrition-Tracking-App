from engine import engine
from models import Base

# Create the tables
Base.metadata.create_all(engine)