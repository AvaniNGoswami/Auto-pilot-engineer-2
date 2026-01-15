from datetime import datetime
from sqlalchemy import String,Column, Boolean, DateTime, ForeignKey
from app.db.base import Base

class AuthSession(Base):
    __tablename__ = "auth_session"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    token_id = Column(String, nullable=True, unique=True)
    is_active = Column(Boolean,default=True,nullable=False)
    created_at = Column(DateTime(timezone=True),default=datetime.utcnow,nullable=False)