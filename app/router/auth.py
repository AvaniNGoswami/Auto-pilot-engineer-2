from fastapi import APIRouter, Depends,HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from datetime import timedelta
from app.core.security import create_access_token, decode_access_token, get_current_user,security
from sqlalchemy.orm import Session
from jwt import decode
from app.core.config import SECRET_KEY,ALGORITHM
from app.models.user import User
from app.models.auth_session import AuthSession
from fastapi.security import OAuth2PasswordBearer
from app.db.database import engine
from uuid import uuid4

router = APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/login")
def login(email:str):
    with Session(engine) as session:
        user = session.query(User).filter(User.email==email).first()
        if not user:
            raise HTTPException(status_code=400,detail="invalid credentials")

    # token = create_access_token(user_id=user.id,expires_delta=timedelta(days=1))
    token = create_access_token(user_id=user.id)
    return {"access_token":token, "token_type":"Bearer"}



@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(get_current_user)
):
    token = credentials.credentials
    payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    jti = payload["jti"]

    with Session(engine) as session:
        auth_session = (
            session.query(AuthSession)
            .filter_by(token_id=jti, is_active=True)
            .first()
        )
        if auth_session:
            auth_session.is_active = False
            session.commit()

    return {"message": "Logged out successfully"}

 

# @router.post("/logout")
# def logout(
#     token: str = Depends(oath2_schema),
#     current_user: User = Depends(get_current_user)
# ):
#     payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     jti = payload["jti"]

#     with Session(engine) as session:
#         auth_session = (
#             session.query(AuthSession)
#             .filter_by(token_id=jti, is_active=True)
#             .first()
#         )
#         if auth_session:
#             auth_session.is_active = False
#             session.commit()

#     return {"message": "Logged out successfully"}

