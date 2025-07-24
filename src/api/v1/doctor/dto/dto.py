from typing import Literal
from pydantic import BaseModel, ConfigDict
from datetime import date
from uuid import UUID


class DoctorDto(BaseModel):
    id: UUID
    name: str
    gender: str
    dob: date
    specialty: str
    phone: str
    address: str
    department_id: UUID

    model_config = ConfigDict(from_attributes=True)


class DoctorCreateDto(BaseModel):
    name: str
    gender: str
    dob: date
    specialty: str
    phone: str
    address: str
    department_id: UUID

    model_config = ConfigDict(from_attributes=True)


class DoctorUpdateDto(BaseModel):
    name: str | None = None
    gender: Literal["Male", "Female"] | None = None
    dob: date | None = None
    specialty: str | None = None
    phone: str | None = None
    address: str | None = None
    department_id: UUID | None = None

    model_config = ConfigDict(from_attributes=True)

class DoctorFilterDto(BaseModel):
    id: UUID | None = None
    name: str | None = None
    name: str | None = None
    gender: Literal["Male", "Female"] | None = None
    dob: date | None = None
    specialty: str | None = None
    phone: str | None = None
    address: str | None = None
