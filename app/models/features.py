from sqlalchemy import Column, String, Float, ForeignKey,Integer,Date
from app.db.base import Base

class Features(Base):
    __tablename__ = "features"
    id = Column(String,primary_key=True)
    userid = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    focus_score = Column(Float)
    fatigue_score = Column(Float)
    context_switch_rate = Column(Float)
    date = Column(Date, nullable=False)
    total_work_minutes = Column(Integer)
    total_break_minutes = Column(Integer)






