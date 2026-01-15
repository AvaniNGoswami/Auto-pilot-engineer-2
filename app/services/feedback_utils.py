from app.db.database import engine
from sqlalchemy.orm import Session
from app.models.feedback import Feedback
import numpy as np

def user_score(userid:str):
    with Session(engine) as session:
        rows = session.query(Feedback).filter_by(userid=userid).all()
        if not rows:
            return {"acceptance_rate":None, "avg_rate":None}
        
        acceptance_vals = [1 if r.accepted else 0 for r in rows if r.accepted is not None]
        rate = [r.rating for r in rows if r.rating is not None]

        acceptance_rate = np.mean(acceptance_vals) if acceptance_vals else None
        avg_rate = np.mean(rate) if rate else None
        return {"acceptance_rate":acceptance_rate, "avg_rate":avg_rate}

