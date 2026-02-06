from sqlalchemy.orm import Session
from app.db.database import engine
from app.models.features import Features
from uuid import uuid4
from datetime import date, timedelta
from random import randint, uniform

with Session(engine) as session:

    for i in range(500):
        d=date.today()
        f = d - timedelta(days=i)
        feature = Features(
            id = str(uuid4()),
            userid = '8529bd10-6f51-49b3-a9ff-3ec9edb331ab',
            focus_score = uniform(0.1, 5.0),
            fatigue_score = uniform(0.1, 5.0),
            context_switch_rate = uniform(0.5, 2.5),
            date = d,
            total_work_minutes = randint(60, 300),
            total_break_minutes = randint(10, 80),
        )
        session.add(feature)
        session.commit()
        session.refresh(feature)

print("inserted fake features 😊")
    
