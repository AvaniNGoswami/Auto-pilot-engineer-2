from sqlalchemy.orm import Session
from app.db.database import engine
from app.models.activity_text import ActivityText
from app.models.githubaccount import GitHubAccount
import requests
from uuid import uuid4
from datetime import datetime


GITHUB_API = "https://api.github.com"


def ingest_github_activity(user_id:str):
    """
    pulls PRs, commits, issues from github and store into activity_text and activity_events tables.
    """
    with Session(engine) as session:
        gh_account = session.query(GitHubAccount).filter(GitHubAccount.userid==user_id).first()
        if not gh_account:
            raise Exception("No github account found!")

        header = {
            "Authorization": f"token {gh_account.access_token}",
            "Accept": "application/vnd.github+json"
        }
        page = 1
        repos = []
        while True:
            resp = requests.get(
                f'{GITHUB_API}/users/{gh_account.github_username}/repos',
                headers=header,
                params={'per_page':50, 'page':page}
            )
            if not resp:
                break
            data = resp.json()
            if not data:
                break
            repos.extend(data)
            page+=1
        
       

        for repo in repos:
            owner = repo['owner']['login']
            repo_name = repo['name']
            full_name = repo['full_name']

            #commits
            try:
                commits_resp = requests.get(
                    f'{GITHUB_API}/repos/{owner}/{repo_name}/commits',
                    headers=header,
                    params={'per_page':50}
                )
                commits_resp.raise_for_status()
            except Exception:
                continue

            for commits in commits_resp.json():
                commit_msg = commits["commit"]["message"]
                msg = f"Commit: {full_name} - {commit_msg}"

                commit_date = datetime.fromisoformat(commits["commit"]["author"]["date"].replace("Z", "+00:00"))
                activity_text=ActivityText(
                        id = str(uuid4()),
                        userid = user_id,
                        message = msg,
                        created_at = commit_date
                    )
                
                session.add(activity_text)


            #pr
            try:
                pr_resp = requests.get(
                    f'{GITHUB_API}/repos/{owner}/{repo_name}/pulls',
                    headers=header,
                    params={'state':'all','per_page':10}
                )
                pr_resp.raise_for_status()
            except Exception:
                continue

            pr_resp.raise_for_status()
            for pull in pr_resp.json():
                merge = pull.get('merged_at')
                pr_date = datetime.fromisoformat(pull["created_at"].replace("Z", "+00:00"))
                if merge:
                    msg = f"pr merged: {pull['title']}"
                else:
                    msg = f'pr opened: {pull["title"]}'
                activity_text=ActivityText(
                    id = str(uuid4()),
                    userid = user_id,
                    message = msg,
                    created_at = pr_date
                    )
                session.add(activity_text)
            


            #issue
            try:
                issue_resp = requests.get(
                    f'{GITHUB_API}/repos/{owner}/{repo_name}/issues',
                    headers=header,
                    params={'state':'all','per_page':10}
                )
                issue_resp.raise_for_status()
            except Exception:
                continue

            for issue in issue_resp.json():
                if 'pull_request' in issue:
                    continue
                msg = f"issue: {issue['title']}"
                issue_date = datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
                activity_text=ActivityText(
                        id = str(uuid4()),
                        userid = user_id,
                        message = msg,
                        created_at = issue_date
                    )
                session.add(activity_text)
                
        session.commit()
        
  











