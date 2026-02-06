from faker import Faker
from random import choice, randint
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.db.database import engine
from app.models.activity import ActivityEvent
from app.models.user import User
from uuid import uuid4

faker = Faker()

user_cases = {
    "high_burnout": [],
    "moderate_stress": [],
    "peak_focus": [],
    "normal_productivity": [],
    "low_productivity": []
}


with Session(engine) as session:
    users = {}
    for case in user_cases.keys():
        user_id = str(uuid4())
        user = User(id=user_id, name=faker.name(), role="dev")
        session.add(user)
        session.commit()
        users[case] = user_id
    print("✅ Users created for each test case")

    now = datetime.now()


    for case, user_id in users.items():
        for i in range(50):  
            if case == "high_burnout":
                event_type = choice(["work"]*8 + ["break"])  
                duration = randint(90, 120) 
            elif case == "moderate_stress":
                event_type = choice(["work"]*5 + ["break"]*2 + ["task switch"]) 
                duration = randint(50, 90)
            elif case == "peak_focus":
                event_type = "work"
                duration = randint(60, 90)
            elif case == "normal_productivity":
                event_type = choice(["work", "break"])
                duration = randint(30, 60)
            elif case == "low_productivity":
                event_type = choice(["task switch", "break"])
                duration = randint(5, 30)

            timestamp = now - timedelta(minutes=randint(0, 10000))
            event = ActivityEvent(
                id=str(uuid4()),
                userid=user_id,
                event_type=event_type,
                duration_minutes=duration,
                timestamp=timestamp
            )
            session.add(event)
    session.commit()
    print("✅ Fake activity events generated for all scenarios ")

