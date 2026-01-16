from sqlalchemy import Column, String
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String)
    role = Column(String) #student, developer, freelancer4
    github_id = Column(String, unique=True)


