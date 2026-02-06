from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from uuid import uuid4
from app.db.database import engine
from app.models.activity import ActivityEvent
from app.models.in_out import In_Out

def work_calculator(userid: str, project_id: str):
    now = datetime.utcnow()

    with Session(engine) as session:
        in_out = (
            session.query(In_Out)
            .filter(
                and_(
                    In_Out.userid == userid,
                    In_Out.in_time.isnot(None),
                    In_Out.out_time.is_(None)
                )
            )
            .order_by(In_Out.in_time.desc())
            .with_for_update()
            .first()
        )
        if in_out.in_time.date() != now.date():
            raise Exception('no active session found for today')
        if project_id and in_out.project_id != project_id:
            raise Exception('Project ID mismatch')

        if not in_out:
            raise Exception("No active IN session found")

        diff_minutes = (now - in_out.in_time).total_seconds() / 60

        if diff_minutes <= 0:
            raise Exception("Invalid work duration")

        activity_event = ActivityEvent(
            id=str(uuid4()),
            userid=userid,
            event_type="work",
            duration_minutes=int(diff_minutes),
            timestamp=in_out.in_time
        )
        session.add(activity_event)

        in_out.out_time = now

        session.commit()


def break_calculator(userid: str,project_id:str):
    now = datetime.utcnow()

    with Session(engine) as session:
        last_out = (
            session.query(In_Out)
            .filter(
                and_(
                    In_Out.userid == userid,
                    In_Out.out_time.isnot(None)
                )
            )
            .order_by(In_Out.out_time.desc())
            .with_for_update()
            .first()
        )
        if last_out and last_out.out_time.date() != now.date():
            last_out = None

        if not last_out:
            diff_minutes = 0
            new_in = In_Out(
            id=str(uuid4()),
            userid=userid,
            in_time=now,
            project_id = project_id
            )
            session.add(new_in)

        else:
            diff_minutes = (now - last_out.out_time).total_seconds() / 60

            if diff_minutes <= 0:
                raise Exception("Invalid break duration")
            if last_out.project_id != project_id:
                activity_event = ActivityEvent(
                id=str(uuid4()),
                userid=userid,
                event_type="task switch",
                duration_minutes=0,
                timestamp=last_out.out_time
                )
                session.add(activity_event)

            else:
                activity_event = ActivityEvent(
                    id=str(uuid4()),
                    userid=userid,
                    event_type="break",
                    duration_minutes=int(diff_minutes),
                    timestamp=last_out.out_time
                )
                session.add(activity_event)
                new_in = In_Out(
                    id=str(uuid4()),
                    userid=userid,
                    in_time=now,
                    project_id=project_id
                )
                session.add(new_in)

        session.commit()
