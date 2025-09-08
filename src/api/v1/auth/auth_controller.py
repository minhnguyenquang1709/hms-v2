from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.utils.security import (
    verify_password,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
)

from ....config.db import get_db
from .dto.auth_dto import TokenDto
from .auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/authorize")
async def authorize():
    pass


@router.post("/token", response_model=TokenDto)
async def login_for_access_token(
    db: Annotated[AsyncSession, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """
    Authenticate user and return an access token.
    """
    # 1. find in DB
    user = await AuthService.get_user_by_username(db, username=form_data.username)

    # 2. check password
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        # save username into 'sub' field of JWT
        data={"sub": user.username, "user_id": str(user.id)},
        expires_delta=access_token_expires,
    )

    # 4. return Token
    return TokenDto.model_validate(
        {"access_token": access_token, "token_type": "bearer"}
    )
