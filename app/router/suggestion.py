from fastapi import APIRouter,Depends
from app.core.security import get_current_user
from random import choice
from pydantic import BaseModel
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.db.database import engine 
from app.models.activity import ActivityEvent
from app.models.features import Features
import joblib
from app.agents.orchestrator import run_agent




router = APIRouter(prefix="/suggestion",tags=["Suggestions"])

# @router.get('/suggest')
# def get_suggestion(current_user = Depends(get_current_user)):

#     model_prod = joblib.load('app/models_storage/productivity.pkl')
#     model_burn = joblib.load('app/models_storage/burnout.pkl')

#     with Session(engine) as session:
#         data = session.query(Features).filter_by(userid=current_user.id).order_by(Features.date.desc()).first()

#     if not data:
#         return {"message": "no data found for current user"}
    
#     X = [[
#         data.total_work_minutes,
#         data.total_break_minutes,
#         data.context_switch_rate,
#         data.fatigue_score
#     ]]

#     predicted_focus = model_prod.predict(X)[0]
#     predicted_burnout = model_burn.predict(X)[0]

#     if predicted_burnout == 'high':
#         suggestion = "Take a break, hydrate, and stop context switching."
#     elif predicted_burnout == 'medium':
#         suggestion = "Slow down a bit today, schedule planned breaks."
#     else:
#         suggestion = "You're doing great, plan deep work sessions today!"


#     return {
#         'predicted focus' : predicted_focus,
#         'predicted burnout' : predicted_burnout,
#         'Suggestion' : suggestion
#     }




@router.get('/suggest')
def get_suggestion(current_user = Depends(get_current_user)):
    return {'suggestion ' : run_agent(current_user.id)}
