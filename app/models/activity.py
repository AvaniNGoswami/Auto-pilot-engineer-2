from sqlalchemy import Column, String, Integer, DateTime
from app.db.base import Base
from datetime import datetime

class ActivityEvent(Base):
    __tablename__ = "activity_events"
    id = Column(String, primary_key=True)
    userid = Column(String)
    event_type = Column(String)
    duration_minutes = Column(Integer)
    timestamp = Column(DateTime)
    