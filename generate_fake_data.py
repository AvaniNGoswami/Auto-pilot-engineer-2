from faker import Faker
from random import choice, randint
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.db.database import engine
from app.models.activity import ActivityEvent
from app.models.user import User

from uuid import uuid4

faker = Faker()

with Session(engine) as session:
    # user = User(id=str(uuid4()), name="test dev", role="developer")
    # session.add(user)
    # session.commit()

    now=datetime.now()

    for i in range(500):
        event = ActivityEvent(
            id=str(uuid4()), 
            userid='8529bd10-6f51-49b3-a9ff-3ec9edb331ab', 
            event_type=choice(["work","break","task switch"]), 
            duration_minutes=randint(5,120), 
            timestamp = now-timedelta(minutes=randint(0,10000))
        )
        session.add(event)
    session.commit()
print("fake data generated 😍")




