from sqlmodel import Column, DateTime,String,ForeignKey
from app.db.base import Base

class In_Out(Base):
    __tablename__='in_out'
    id = Column(String,primary_key=True)
    userid = Column(String,ForeignKey("users.id", ondelete="CASCADE"))
    in_time = Column(DateTime)
    out_time = Column(DateTime)
    project_id = Column(String, nullable=True)