from datetime import timedelta
from typing import Annotated, Optional, cast
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jwt import PyJWTError
import jwt
from src.api.v1.models.auth import Role, User
from src.api.v1.utils.security import (
    ALGORITHM,
    SECRET_KEY,
    get_current_user,
    verify_password,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
)

from ....config.db import get_db
from .dto.auth_dto import TokenDto, UserDto, UserProfileResponse
from .auth_service import AuthService

CLIENT_ID = "chatbot"
CLIENT_SECRET = "chatbotsecret"

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    username: str = Form(...),
    password: str = Form(...),
    role: Role = Form(...),
):
    existing_user = await AuthService.get_user_by_username(db, username=username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    new_user = await AuthService.create_account(
        db, username=username, password=password, role=role
    )
    return {
        "data": UserDto.model_validate(new_user, from_attributes=True),
        "status": status.HTTP_201_CREATED,
    }


@router.get("/authorize")
async def authorize(
    request: Request,
    # response_type: str,
    # client_id: str,
    redirect_uri: str,
    state: Optional[str] = None,
):
    # ignore client_id for now
    # display login form
    return HTMLResponse(
        f"""
        <html>
            <head><title>Hospital Login</title></head>
            <body>
                <h1>Login to Hospital System</h1>
                <form action="/api/v1/auth/authorize/login" method="post">
                    <input type="hidden" name="redirect_uri" value="{redirect_uri}">
                    <input type="hidden" name="state" value="{state}">
                    <label>Username: <input type="text" name="username"></label><br>
                    <label>Password: <input type="password" name="password"></label><br>
                    <input type="submit" value="Log In and Authorize">
                </form>
            </body>
        </html>
        """
    )


@router.post("/authorize/login")
async def login_username_password(
    db: Annotated[AsyncSession, Depends(get_db)],
    username: str = Form(...),
    password: str = Form(...),
    redirect_uri: str = Form(...),
    state: Optional[str] = Form(None),
):
    user = await AuthService.get_user_by_username(db, username=username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    cast(User, user)
    # create authorization code
    # in a real system, save in DB/Redis with short TTL
    authorization_code = create_access_token(
        data={"sub": user.id.__str__(), "scope": "auth_code"},
        expires_delta=timedelta(minutes=1),
    )

    # redirect
    redirect_url = f"{redirect_uri}?code={authorization_code}"
    if state:
        redirect_url += f"&state={state}"

    return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)


# check token
@router.get("/users/me")
async def get_me(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[UserDto, Depends(get_current_user)],
):
    if current_user.role != Role.PATIENT and current_user.role != Role.DOCTOR:
        raise HTTPException(status_code=403, detail="Forbidden")

    if current_user.role == Role.PATIENT:
        profile = await AuthService.get_patient_profile_by_user_id(db, current_user.id)
        if not profile:
            raise HTTPException(status_code=404, detail="Patient profile not found")

        patient_profile_response = UserProfileResponse(
            user_id=current_user.id,
            username=current_user.username,
            role=current_user.role,
            full_name=profile.full_name,
            gender=profile.gender,
            dob=profile.dob,
        )
        return {"data": patient_profile_response, "status": status.HTTP_200_OK}


@router.post("/token", response_model=TokenDto)
async def exchange_code_for_token(
    db: Annotated[AsyncSession, Depends(get_db)],
    # Các tham số này được gửi trong body của request từ BE Chatbot
    grant_type: str = Form(...),
    code: str = Form(...),
    redirect_uri: str = Form(...),
    client_id: str = Form(...),
    client_secret: str = Form(...),  # Bổ sung client_secret
):
    # 1. check grant type
    if grant_type != "authorization_code":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unsupported grant_type"
        )

    # 2. authenticate Client (BE Chatbot)
    # real case: check in DB
    if client_id != CLIENT_ID or client_secret != CLIENT_SECRET:
        raise HTTPException(status_code=401, detail="Invalid client credentials")

    # 3. decode and authenticate the auth code
    try:
        payload: dict = jwt.decode(code, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("scope") != "auth_code":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization code scope",
            )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization code payload",
            )

        user = await AuthService.get_user_by_user_id(db, user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=404, detail="User not found for the provided code"
            )

    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authorization code",
        )

    # 4. return an access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "user_id": str(user.id),
            "role": user.role.value,
        },
        expires_delta=access_token_expires,
    )
    return TokenDto(access_token=access_token, token_type="bearer")
