from uuid import UUID
from pydantic import BaseModel, ConfigDict


class DepartmentDto(BaseModel):
    id: UUID
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class DepartmentCreateDto(BaseModel):
    name: str
    description: str


class DepartmentUpdateDto(BaseModel):
    name: str | None = None
    description: str | None = None
