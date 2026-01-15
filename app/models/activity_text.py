from sqlalchemy import Column, String, DateTime, ForeignKey
from app.db.base import Base
from datetime import datetime

class ActivityText(Base):
    __tablename__ = "activity_text"

    id = Column(String, primary_key=True)
    userid = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message = Column(String, nullable=False)         # commit message, task update, PR comment
    created_at = Column(DateTime, default=datetime.utcnow)

