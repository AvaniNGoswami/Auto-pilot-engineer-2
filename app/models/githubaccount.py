from sqlmodel import Column, String, DateTime, ForeignKey
from app.db.base import Base
from datetime import datetime

class GitHubAccount(Base):
    __tablename__='github_accounts'
    id = Column(String, primary_key=True)
    userid = Column(String, ForeignKey("users.id", ondelete="CASCADE"))
    github_username = Column(String)
    access_token = Column(String)   # encrypt later, plain for demo
    created_at = Column(DateTime, default=datetime.utcnow)