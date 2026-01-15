from sqlalchemy.orm import Session
from app.db.database import engine
from app.models.features import Features
from uuid import uuid4
from datetime import date, timedelta
from app.models.user import User
from random import randint, uniform

with Session(engine) as session:
    id = str(uuid4())
    name = "Avani"
    role = "developer"
    user = User(id=id,name=name,role=role)
    session.add(user)
    session.commit()
    session.refresh(user)

    for i in range(7):
        d=date.today()
        f = d - timedelta(days=i)
        feature = Features(
            id = str(uuid4()),
            userid = user.id,
            focus_score = uniform(0.1, 5.0),
            fatigue_score = uniform(0.1, 5.0),
            context_switch_rate = uniform(0.5, 2.5),
            date = f,
            total_work_minutes = randint(60, 300),
            total_break_minutes = randint(10, 80),
        )
        session.add(feature)
        session.commit()
        session.refresh()

print("inserted fake features 😊")
    

