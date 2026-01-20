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

@router.get('/suggest')
def get_suggestion(current_user = Depends(get_current_user)):
    return {'suggestion ' : run_agent(current_user.id)}
