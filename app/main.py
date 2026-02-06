from fastapi import FastAPI
from app.router.auth import router as auth_router
from app.router.suggestion import router as suggest_router
from app.router import feedback, explanation, github, me_dashboard, github_api, in_out
from app.services.feature_engineering import run_feature_engineering
from app.services.scheduler import start_scheduler
import threading


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

@app.on_event("startup")
async def startup_event():
    thread = threading.Thread(target=start_scheduler)
    thread.daemon = True
    thread.start()

