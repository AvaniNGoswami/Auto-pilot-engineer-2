from app.models.features import Features
from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from app.db.database import engine


def history(userid):
    days = 20
    since = datetime.now() - timedelta(days=days)
    with Session(engine) as session:
        feature = session.query(Features).filter(Features.userid==userid).filter(Features.date >= since).order_by(Features.date).all()
        hist = []
        for h in feature:
            hist.append({
                'focus':h.focus_score,
                'fatigue':h.fatigue_score,
                'break':h.total_break_minutes,
                'work':h.total_work_minutes,
                'context switch':h.context_switch_rate
            })
    return hist
    