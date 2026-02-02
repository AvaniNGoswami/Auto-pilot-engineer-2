from sqlalchemy.orm import Session
from app.db.database import engine
from app.models.githubaccount import GitHubAccount
from uuid import uuid4
from datetime import datetime
def connect_github(username:str,access_token:str,user_id:str):
    with Session(engine) as session:
        gh_user = session.query(GitHubAccount).filter(GitHubAccount.userid==user_id).first()
        
        if gh_user:
            gh_user.access_token = access_token
            gh_user.github_username = username
        else:
            gh = GitHubAccount(
                id = str(uuid4()),
                userid = user_id,
                github_username = username,
                access_token = access_token,
                created_at = datetime.utcnow()
            )
            session.add(gh)
        session.commit()
