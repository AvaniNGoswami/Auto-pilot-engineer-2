from sqlmodel import Column, String, Boolean,Integer,DateTime
from app.db.base import Base
from datetime import datetime

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(String, primary_key=True)
    userid = Column(String, nullable=False)
    suggestion = Column(String, nullable=False)
    accepted = Column(Boolean)
    rating = Column(Integer)  
    created_at = Column(DateTime, default=datetime.utcnow)
