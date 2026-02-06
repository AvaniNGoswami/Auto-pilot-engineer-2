import os
from sqlalchemy import create_engine
from app.db.base import Base

DATABASE_URL = os.getenv("DATABASE_URL") 

engine = create_engine(DATABASE_URL, echo=True,connect_args={"options": "-c timezone=utc"})

Base.metadata.create_all(engine)
print("✅ All tables created successfully!")
