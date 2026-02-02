from fastapi import APIRouter, Depends
from app.services.work_break import work_calculator,break_calculator
from app.core.security import get_current_user
from typing import Optional
from pydantic import BaseModel

class projectid(BaseModel):
    project_id : Optional[str]=None


router = APIRouter(prefix='/in_out',tags=['In Out'])

@router.post('/in')
def in_(data: projectid,userid = Depends(get_current_user)):
    break_calculator(userid=userid.id,project_id=data.project_id)
    return {"status":"ok"}

@router.post('/out')
def out_(data: projectid,userid=Depends(get_current_user)):
    work_calculator(userid=userid.id,project_id=data.project_id)
    return {"status":"ok"}
