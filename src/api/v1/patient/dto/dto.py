from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import List, Optional
from uuid import UUID

class PatientDto(BaseModel):
    id: UUID
    name: str
    gender: str
    dob: date
    phone: str
    address: str
    chronic_conditions: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)

class PatientCreateDto(BaseModel):
    name: str
    gender: str
    dob: date
    phone: str
    address: str
    chronic_conditions: Optional[List[str]] = None

class PatientUpdateDto(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    chronic_conditions: Optional[List[str]] = None