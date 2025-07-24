from pydantic import BaseModel


class CommandDto(BaseModel):
  command: str
  payload: dict

class CommandResponseDto(BaseModel):
  status: int
  data: dict