# file: auth/security.py
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from jwt import PyJWTError
from src.api.v1.auth.dto.auth_dto import TokenDataDto, UserDto
from src.api.v1.models.auth import User
from src.config.db import get_db
from src.api.v1.auth.auth_service import AuthService

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "my-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    payload = {**to_encode, "exp": expire, "iat": datetime.now(timezone.utc)}
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserDto:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenDataDto(username=username)
    except PyJWTError:
        raise credentials_exception

    user = await AuthService.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return UserDto(id=user.id, username=user.username)
