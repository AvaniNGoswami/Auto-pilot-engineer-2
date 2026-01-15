import pandas as pd
from sqlalchemy.orm import Session
from app.db.database import engine
from app.models.activity import ActivityEvent
from app.models.features import Features
from uuid import uuid4
from sqlalchemy import Date

def run_feature_engineering():
    print("running daily feature computation")
    with Session(engine) as session:
        # Get dates already processed in features table
        existing_dates = session.query(Features.date).distinct().all()
        existing_dates = {d[0] for d in existing_dates}

        # Pull only events whose date is not processed
        events = session.query(ActivityEvent).filter(
            ~ActivityEvent.timestamp.cast(Date).in_(existing_dates)
        ).all()
        if not events:
            print("✨ No new events found. Nothing to compute.")
            return


        df = pd.DataFrame([{
            "userid":e.userid,
            "event_type":e.event_type,
            "duration_minutes":e.duration_minutes,
            "timestamp":e.timestamp
        }for e in events])

        df["date"] = pd.to_datetime(df['timestamp']).dt.date
        grouped = df.groupby(['userid','date'])

        for (userid,date),group in grouped:
            total_work = group[group['event_type']=='work']['duration_minutes'].sum()
            total_break = group[group['event_type']=='break']['duration_minutes'].sum()
            context_switch = group[group['event_type']=='task switch'].shape[0]

            focus_score = total_work/(total_work+total_break+context_switch*5)
            fatique_score = total_break/(total_work+total_break+context_switch*5)

            feature = Features(
                id = str(uuid4()),
                userid = userid,
                date = date,
                total_work_minutes = int(total_work),           
                total_break_minutes = int(total_break),         
                context_switch_rate = int(context_switch),     
                fatigue_score = float(fatique_score),          
                focus_score = float(focus_score)              
            )
            session.add(feature)
            session.commit()
            session.refresh(feature)


    print("👍👍👍👍👍👍computed")