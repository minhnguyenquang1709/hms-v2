import uuid
from pydantic import BaseModel


class TokenDto(BaseModel):
    access_token: str
    token_type: str


class TokenDataDto(BaseModel):
    username: str

class UserDto(BaseModel):
    id: uuid.UUID
    username: str