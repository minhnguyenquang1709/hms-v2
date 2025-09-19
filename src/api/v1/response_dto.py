from typing import Any
from pydantic import BaseModel


class ResponseDto(BaseModel):
    data: Any
    status: int
