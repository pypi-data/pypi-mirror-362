import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from passlib.context import CryptContext
from fastapi import Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from datetime import datetime, timedelta, timezone
from app.core.settings import Settings
from app.api.deps import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_settings = Settings().auth
credentials_exceptions = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate token",
    headers={"WWW-Authenticate": "Bearer"}
)

def verify_token(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def has_password(plain_password):
    return pwd_context.hash(plain_password)

def get_user(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email, password) -> User | bool:
    user = get_user(db, email)
    if not user:
        return False
    if not verify_token(password, user.password):
        return False
    return user

def create_acess_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=1)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, auth_settings.secret, algorithm=auth_settings.algorith)
    return encoded_jwt

async def get_token_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise credentials_exceptions
    return token

async def get_current_user(
        token: Annotated[str, Depends(get_token_from_cookie)],
        db: Annotated[Session, Depends(get_db)]
):
    try:
        payload = jwt.decode(token, auth_settings.secret, algorithms=[auth_settings.algorithm])
        email = payload.get("sub")
        if email is None:
            raise credentials_exceptions
    except InvalidTokenError:
        raise credentials_exceptions
    user = get_user(db, email)
    if not user:
        raise credentials_exceptions
    return user




