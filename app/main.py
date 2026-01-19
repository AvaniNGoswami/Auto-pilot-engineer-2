# from fastapi import FastAPI
# from app.router.auth import router as auth_router
# from app.router.suggestion import router as suggest_router
# from app.router import feedback
# from app.router import explanation
# from app.router import github
# from apscheduler.schedulers.background import BackgroundScheduler
# from app.services.feature_engineering import run_feature_engineering

    
# app=FastAPI(title="Auto pilot Engineer")

# @app.get("/")
# def health_check():
#     return "Heyy, Welcome to Auto Pilot Engineer 😊"

# app.include_router(auth_router)
# app.include_router(suggest_router)
# app.include_router(feedback.router)
# app.include_router(explanation.router)
# app.include_router(github.router)

# def start_schedular():
#     schedular = BackgroundScheduler()
#     schedular.add_job(run_feature_engineering,'interval',minutes=1)
#     schedular.start()
#     print("🕒 APScheduler started...")


# @app.on_event("startup")
# def startup_event():
#     start_schedular()



from fastapi import FastAPI
from app.router.auth import router as auth_router
from app.router.suggestion import router as suggest_router
from app.router import feedback, explanation, github
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

# ---- SCHEDULER ----
scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(
        run_feature_engineering,
        trigger=IntervalTrigger(minutes=1),
        id="feature_job",
        replace_existing=True,
    )
    scheduler.start()
    print("🕒 APScheduler started... running every 1 minute")

# Stop scheduler when API shuts down (clean exit)
atexit.register(lambda: scheduler.shutdown())

@app.on_event("startup")
def startup_event():
    start_scheduler()

