from fastapi import APIRouter,Depends
from groq import Groq
from app.core.security import get_current_user
from openai import OpenAI
import os
from app.services.history import history
from pydantic import BaseModel
from app.services.llm_service import answer_question as llm_answer_question

class que(BaseModel):
    que:str

router = APIRouter(prefix='/ask',tags=['Ask'])
client = client = Groq(api_key=os.getenv("GROQ_API_KEY"))
@router.post('/')
def answer_question(data:que,current_user=Depends(get_current_user)):
    hist= history(userid=current_user.id)

    response = llm_answer_question(data.que, hist)

    return {'answer': response}

    


