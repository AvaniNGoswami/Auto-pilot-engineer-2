from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.activity_text import ActivityText
from app.models.feedback import Feedback
from app.models.githubaccount import GitHubAccount
from app.models.activity import Activity
from app.models.auth_session import AuthSession
from app.models.user import User
from app.models.in_out import In_Out
from app.models.features import Features

