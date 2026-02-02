from fastapi import APIRouter, Depends
from app.services.github_ingest import ingest_github_activity
from app.core.security import get_current_user
from app.services.github_services import connect_github
from pydantic import BaseModel

class GitHubConnectRequest(BaseModel):
    username: str
    access_token: str


router = APIRouter(prefix='/github',tags=['Github API'])

@router.post('/connect')
def connect(payload: GitHubConnectRequest, user=Depends(get_current_user)):
    connect_github(username=payload.username, access_token=payload.access_token,user_id=user.id)
    return {'status' : 'Github connected'}


@router.post('/sync')
def sync_github(user=Depends(get_current_user)):
    ingest_github_activity(user.id)
    return {"status":"github synced"}