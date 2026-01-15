from sqlalchemy.orm import Session
from app.db.database import engine
from app.models.features import Features
import pandas as pd

def load_dataframe():
    with Session(engine) as session:
        rows = session.query(Features).all()

    df = pd.DataFrame([{
        "userid":r.userid,
        "focus_score":r.focus_score,
        "fatigue_score":r.fatigue_score,
        "total_break_minutes":r.total_break_minutes,
        "total_work_minutes":r.total_work_minutes,
        "context_switch_rate":r.context_switch_rate,
        "date":r.date
    } for r in rows])

    return df