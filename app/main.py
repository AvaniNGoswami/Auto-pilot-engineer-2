from fastapi import FastAPI
from app.router.auth import router as auth_router
from app.router.suggestion import router as suggest_router
from app.router import feedback, explanation, github, me_dashboard, github_api, in_out
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.services.feature_engineering import run_feature_engineering
import atexit

app = FastAPI(title="Auto Pilot Engineer")

@app.get("/")
def health_check():
    return {"msg": "Heyy, Welcome to Auto Pilot Engineer 😊"}

app.include_router(auth_router)
app.include_router(suggest_router)
app.include_router(feedback.router)
app.include_router(explanation.router)
app.include_router(github.router)
app.include_router(me_dashboard.router) 
app.include_router(github_api.router)
app.include_router(in_out.router)


scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(
        run_feature_engineering,
        trigger=IntervalTrigger(minutes=60),
        id="feature_job",
        replace_existing=True,
    )
    scheduler.start()
    print("🕒 APScheduler started... ")


atexit.register(lambda: scheduler.shutdown())

@app.on_event("startup")
def startup_event():
    start_scheduler()

