from fastapi import FastAPI
from app.router.auth import router as auth_router
from app.router.suggestion import router as suggest_router
from app.router import feedback
from app.router import explanation
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.feature_engineering import run_feature_engineering

    
app=FastAPI(title="Auto pilot Engineer")

@app.get("/")
def health_check():
    return "Heyy, Welcome to Auto Pilot Engineer 😊"

app.include_router(auth_router)
app.include_router(suggest_router)
app.include_router(feedback.router)
app.include_router(explanation.router)

def start_schedular():
    schedular = BackgroundScheduler()
    schedular.add_job(run_feature_engineering,'interval',hours=24)
    schedular.start()
    print("🕒 APScheduler started...")


@app.on_event("startup")
def startup_event():
    start_schedular()
