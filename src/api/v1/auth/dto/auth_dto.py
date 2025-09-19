import uuid
from pydantic import BaseModel, ConfigDict
import datetime

from src.api.v1.models.auth import Role


class TokenDto(BaseModel):
    access_token: str
    token_type: str


class TokenDataDto(BaseModel):
    username: str


class UserDto(BaseModel):
    id: uuid.UUID
    username: str
    role: Role


class UserProfileResponse(BaseModel):
    user_id: uuid.UUID
    username: str
    role: Role
    full_name: str
    gender: str
    dob: datetime.date

    model_config = ConfigDict(from_attributes=True)
