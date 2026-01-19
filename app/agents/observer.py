from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.models.features import Features
from app.db.database import engine

def observe(userid:str):
    with Session(engine) as session:
        today = date.today()
        last_7 = today - timedelta(days=7)

        data = session.query(Features).filter(Features.userid == userid).filter(Features.date>=last_7).order_by(Features.date.desc()).all()
        return data