import pandas as pd
from sqlalchemy.orm import Session
from app.db.database import engine
from app.models.activity import ActivityEvent
from app.models.features import Features
from app.models.activity_text import ActivityText
from uuid import uuid4
from sqlalchemy import Date

def run_feature_engineering():
    print("running daily feature computation")
    with Session(engine) as session:
        existing_dates = session.query(Features.date).distinct().all()
        existing_dates = {d[0] for d in existing_dates}

        events = session.query(ActivityEvent).filter(
            ~ActivityEvent.timestamp.cast(Date).in_(existing_dates)
        ).all()


        events_github = session.query(ActivityText).filter(
            ~ActivityText.created_at.cast(Date).in_(existing_dates)
        ).all()

        if not events and not events_github:
            print("✨ No new events found (Activity + GitHub). Nothing to compute.")
            return

        if events:
            df_activity = pd.DataFrame([{
                "userid": e.userid,
                "event_type": e.event_type,
                "duration_minutes": e.duration_minutes,
                "timestamp": e.timestamp
            } for e in events])
            df_activity["date"] = pd.to_datetime(df_activity['timestamp']).dt.date
        else:
            df_activity = pd.DataFrame(columns=["userid","event_type","duration_minutes","timestamp","date"])


        if events_github:
            df_github = pd.DataFrame([{
                "userid": e.userid,
                "message": e.message,
                "created_at": e.created_at
            } for e in events_github])
            df_github["date"] = pd.to_datetime(df_github['created_at']).dt.date
        else:
            df_github = pd.DataFrame(columns=["userid","message","created_at","date"])


        grouped_activity = df_activity.groupby(['userid','date']) if not df_activity.empty else {}
        grouped_github = df_github.groupby(['userid','date']) if not df_github.empty else {}

        keys = set(list(grouped_activity.groups.keys()) if grouped_activity else []) | \
               set(list(grouped_github.groups.keys()) if grouped_github else [])

        for (userid, date) in keys:

            group_activity = grouped_activity.get_group((userid,date)) if (grouped_activity and (userid,date) in grouped_activity.groups) else pd.DataFrame()
            total_work = group_activity[group_activity['event_type']=='work']['duration_minutes'].sum() if not group_activity.empty else 0
            total_break = group_activity[group_activity['event_type']=='break']['duration_minutes'].sum() if not group_activity.empty else 0
            context_switch = group_activity[group_activity['event_type']=='task switch'].shape[0] if not group_activity.empty else 0

            coding_min = 0
            context_switch_count = 0
            if grouped_github and (userid,date) in grouped_github.groups:
                group_github = grouped_github.get_group((userid,date))
                for msg in group_github['message']:
                    msg = msg.lower()
                    if 'issue' in msg or 'pr' in msg:
                        context_switch_count += 1
                    else:
                        coding_min += 20

    
            context_switch += context_switch_count
            total_work += coding_min

            denominator = total_work + total_break + context_switch*5
            focus_score = total_work / denominator if denominator > 0 else 1
            fatigue_score = total_break / denominator if denominator > 0 else 1


            feature = Features(
                id=str(uuid4()),
                userid=userid,
                date=date,
                total_work_minutes=int(total_work),
                total_break_minutes=int(total_break),
                context_switch_rate=int(context_switch),
                fatigue_score=float(fatigue_score),
                focus_score=float(focus_score)
            )
            session.add(feature)
            session.commit()
            session.refresh(feature)

    print("👍👍👍👍👍👍👍👍👍👍👍👍 Feature computation done for all available data")
