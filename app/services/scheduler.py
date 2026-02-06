from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.services.feature_engineering import run_feature_engineering

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(
        run_feature_engineering,
        trigger=IntervalTrigger(minutes=2),
        id="feature_job",
        replace_existing=True,
    )
    scheduler.start()
    print("🕒 APScheduler started...")
