from fastapi import APIRouter,Request,Header,Depends
from sqlalchemy.orm import Session
from app.db.database import engine
from app.models.activity_text import ActivityText
from datetime import datetime
from app.core.security import get_current_user
from uuid import uuid4

router = APIRouter(prefix='/github', tags=['Github Webhooks'])

@router.post('/events')
async def events(request:Request, x_github_events:str=Header(None),current_user=Depends(get_current_user)):
    payload = await request.json()

    if x_github_events=='push':
        msg = payload['head_commit']['message']

    if x_github_events=='pull_request':
        msg = f"PR {payload['action']} : {payload['pull_request']['title']}"

    if msg:
        with Session(engine) as session:
            activity_text = ActivityText(
                id = str(uuid4()),
                userid = current_user,
                message = msg,         # commit message, task update, PR comment
                created_at = datetime.utcnow()
            )
            session.add(activity_text)
            session.commit()
            session.refresh(activity_text)
    return {'status':'okay'}


