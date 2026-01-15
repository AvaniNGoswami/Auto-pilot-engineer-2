from sqlalchemy import create_engine

DATABASEURL =  "postgresql+psycopg2://postgres:admin123@localhost:5432/autopilot_engineer"

engine = create_engine(DATABASEURL, echo=True)

# def create_db():
#     SQLModel.metadata.create_all(engine)
