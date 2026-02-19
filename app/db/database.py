import os
from sqlalchemy import create_engine
from app.db.base import Base
from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True,connect_args={"options": "-c timezone=utc"})

Base.metadata.create_all(engine)
print("✅ All tables created successfully!")
