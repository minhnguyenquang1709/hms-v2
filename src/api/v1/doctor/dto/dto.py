from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict
import datetime
from uuid import UUID


class DoctorProfileDto(BaseModel):
    id: UUID
    user_id: UUID
    full_name: str
    gender: str
    dob: datetime.date
    phone: str
    address: str
    department_id: UUID

    model_config = ConfigDict(from_attributes=True)


class DoctorUpdateDto(BaseModel):
    full_name: Optional[str] = None
    gender: Optional[Literal["Male", "Female"]] = None
    dob: Optional[datetime.date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    department_id: Optional[UUID] = None
