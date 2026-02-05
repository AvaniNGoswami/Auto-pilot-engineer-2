from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
from app.core.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
import jwt
from jwt import PyJWTError
from app.models.user import User
from app.models.auth_session import AuthSession
from sqlalchemy.orm import Session
from app.db.database import engine
from uuid import uuid4

# oath2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def create_access_token(user_id:str, expires_delta:Optional[timedelta]=None) -> str:
    jti = str(uuid4())
    expire = (
    datetime.utcnow() + expires_delta
    if expires_delta
    else datetime.utcnow() + ACCESS_TOKEN_EXPIRE
    )

    payload = {
                "sub":user_id,
                "jti":jti,
                "iat":datetime.utcnow(),
                "exp":expire,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    with Session(engine) as session:
        auth_session = AuthSession(
            id = str(uuid4()),
            user_id = user_id,
            token_id = jti,
            is_active = True,
            created_at = datetime.utcnow()
        )
        session.add(auth_session)
        session.commit()
    return token






def decode_access_token(token:str) -> dict:
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        if "sub" not in payload or "jti" not in payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid token payload")
        return payload
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid or expired token", headers={"WWW-Authentication":"Bearer"})

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)

    user_id = payload["sub"]
    jti = payload["jti"]

    with Session(engine) as session:
        auth_session = session.query(AuthSession).filter_by(
            token_id=jti, is_active=True
        ).first()

        if not auth_session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="session expired or logged out"
            )

        user = session.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="user not found"
            )

        return user

# def get_current_user(token:str=Depends(oath2_schema)) -> User:
#     payload = decode_access_token(token)
#     user_id = payload["sub"]
#     jti = payload["jti"]

#     with Session(engine) as session: 
#         auth_session = session.query(AuthSession).filter_by(token_id=jti, is_active=True).first()
#         if not auth_session:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="session expired or logged out"
#             )
#         user = session.get(User, user_id)
#         if not user:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="user not found"
#             )
        
#         return user
                                                            