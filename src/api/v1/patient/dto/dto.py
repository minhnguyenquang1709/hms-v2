from pydantic import BaseModel, ConfigDict
import datetime
from typing import Optional, Literal
from uuid import UUID


class PatientProfileDto(BaseModel):
    id: UUID
    user_id: UUID
    full_name: str
    gender: Literal["Male", "Female"]
    dob: datetime.date
    phone: str
    address: str

    model_config = ConfigDict(from_attributes=True)


# class PatientCreateDto(BaseModel):
#     name: str
#     gender: Literal["Male", "Female"]
#     dob: date
#     phone: str
#     address: str
#     chronic_conditions: Optional[List[str]] = None


class PatientUpdateDto(BaseModel):
    full_name: Optional[str] = None
    gender: Optional[Literal["Male", "Female"]] = None
    dob: Optional[datetime.date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
