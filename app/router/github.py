# from fastapi import APIRouter,Request,Header,Depends
# from sqlalchemy.orm import Session
# from app.db.database import engine
# from app.models.activity_text import ActivityText
# from datetime import datetime
# from app.core.security import get_current_user
# from uuid import uuid4

# router = APIRouter(prefix='/github', tags=['Github Webhooks'])

# @router.post('/events')
# async def events(request:Request, x_github_events:str=Header(None),current_user=Depends(get_current_user)):
#     payload = await request.json()

#     if x_github_events=='push':
#         msg = payload['head_commit']['message']

#     if x_github_events=='pull_request':
#         msg = f"PR {payload['action']} : {payload['pull_request']['title']}"

#     if msg:
#         with Session(engine) as session:
#             activity_text = ActivityText(
#                 id = str(uuid4()),
#                 userid = current_user,
#                 message = msg,         # commit message, task update, PR comment
#                 created_at = datetime.utcnow()
#             )
#             session.add(activity_text)
#             session.commit()
#             session.refresh(activity_text)
#     return {'status':'okay'}


from fastapi import APIRouter, Request, Header,Depends
from sqlalchemy.orm import Session
from app.db.database import engine
from app.models.activity_text import ActivityText
from datetime import datetime
from uuid import uuid4
from fastapi.responses import PlainTextResponse
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix='/github', tags=['Github Webhooks'])

# current_user = Depends(get_current_user)

@router.get("/test")
async def test():
    print("GET route reached!")
    return {"status": "ok"}



@router.post('/events')
async def events(request: Request, x_github_event: str = Header(None, alias="X-GitHub-Event")):
    print("😊Received webhook!")
    print("😊Headers:", request.headers)
    print("😊Payload:", await request.body())

    payload = await request.json()
    msg = None
    user_id = payload['sender'].get('id')
    name = payload['sender'].get('login')


    if x_github_event == 'push':
        msg = payload.get('head_commit', {}).get('message')
    
    elif x_github_event == 'pull_request':
        msg = f"PR {payload.get('action')} : {payload.get('pull_request', {}).get('title')}"
    
    elif x_github_event == 'issues':
        msg = f"Issue {payload.get('action')} : {payload.get('issue', {}).get('title')}"
    
    elif x_github_event == 'issue_comment':
        msg = f"Issue Comment {payload.get('action')} : {payload.get('comment', {}).get('body')}"

    if msg:
        with Session(engine) as session:
            gh_user = session.query(User).filter_by(id=user_id).first()

            if not gh_user:
                user = User(
                    id = user_id,
                    name = name,
                    role = 'developer'
                )
                session.add(user)
                session.commit()
                session.refresh(user)

            activity_text = ActivityText(
                id=str(uuid4()),
                userid=user_id,   # Since no user auth, you can mark as github
                message=msg,
                created_at=datetime.utcnow()
            )
            session.add(activity_text)
            session.commit()
            session.refresh(activity_text)

    return PlainTextResponse("Webhook received", status_code=200)

