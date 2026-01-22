from app.db.database import engine
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User
from fastapi import APIRouter,Depends

router = APIRouter(prefix="/me", tags=['ME'])

@router.get('/')
def get_user(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role
    }
