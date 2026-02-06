from fastapi import APIRouter, Depends,HTTPException
from pydantic import BaseModel
from app.models.feedback import Feedback
from sqlalchemy.orm import Session
from app.db.database import engine
from app.core.security import get_current_user
from uuid import uuid4


class feedbackrequest(BaseModel):
    suggestion_id:str
    accepted: bool
    rating:int
    


class feedbackresponse(BaseModel):
    message:str

router = APIRouter(prefix="/feedback",tags=["Feedback"])

@router.post("/")
def update_feedback(data: feedbackrequest, current_user = Depends(get_current_user)):
    with Session(engine) as session:
        fb = session.query(Feedback).filter_by(
            id=data.suggestion_id,
            userid=current_user.id
        ).first()

        if not fb:
            raise HTTPException(status_code=404, detail="Feedback entry not found")

        fb.accepted = data.accepted
        fb.rating = data.rating
        session.commit()
        session.refresh(fb)

    return {"message": "Feedback updated successfully"}