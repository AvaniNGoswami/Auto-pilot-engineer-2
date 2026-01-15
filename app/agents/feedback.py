from sqlalchemy.orm import Session
from app.db.database import engine
from app.models.feedback import Feedback
from uuid import uuid4
from datetime import datetime

def record(userid, suggestion, rating, accepted):
    with Session(engine) as session:
        fb = Feedback(
            id = str(uuid4()),
            userid = userid,
            suggestion = suggestion,
            accepted = accepted,
            rating = rating,  # 0-5 stars
            created_at = datetime.utcnow()
        )
        session.add(fb)
        session.commit()
        session.refresh(fb)