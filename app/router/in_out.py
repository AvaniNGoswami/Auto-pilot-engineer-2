from fastapi import APIRouter, Depends
from app.services.work_break import work_calculator,break_calculator
from app.core.security import get_current_user

router = APIRouter(prefix='/in_out',tags=['In Out'])

@router.post('/in')
def in_(userid = Depends(get_current_user)):
    break_calculator(userid=userid.id)
    return {"status":"ok"}

@router.post('/out')
def out_(userid=Depends(get_current_user)):
    work_calculator(userid=userid.id)
    return {"status":"ok"}
