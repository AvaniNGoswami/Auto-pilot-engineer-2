import os
from sqlalchemy import create_engine

# DATABASEURL =  "postgresql+psycopg2://postgres:admin123@localhost:5432/autopilot_engineer"
DATABASE_URL = os.getenv("DATABASE_URL") 

engine = create_engine(DATABASE_URL, echo=True,connect_args={"options": "-c timezone=utc"})
