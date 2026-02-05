from sqlalchemy.orm import Session
from app.db.database import engine
from app.models.activity_text import ActivityText
from pydantic import BaseModel
from app.services.nlp_utils import get_most_relevant_message, generate_natural_explanation
from fastapi import APIRouter,Depends
from app.core.security import get_current_user

class request_model(BaseModel):
    suggestion : str

class response_model(BaseModel):
    suggestion : str
    explanation: str

router = APIRouter(prefix='/explain', tags=['Explanation'])
@router.post('/',response_model=response_model)
def explain(data : request_model, current_user=Depends(get_current_user)):
    with Session(engine) as session:
        messages = session.query(ActivityText).filter(ActivityText.userid==current_user.id).order_by(ActivityText.created_at.desc()).limit(20).all()
        messages = [m.message for m in messages]
    
    if not messages:
        explain = f"No previous messages found. Suggestion: {data.suggestion}"
        return response_model(suggestion=data.suggestion, explanation=explain)

    relevant_message = get_most_relevant_message(data.suggestion,messages)
    explain = generate_natural_explanation(data.suggestion,relevant_message)
    return response_model(suggestion=data.suggestion,explanation=explain)