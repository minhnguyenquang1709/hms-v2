from pydantic import BaseModel, ConfigDict
from datetime import date
from uuid import UUID


class DoctorCreate(BaseModel):
    pass


class DoctorResponse(BaseModel):
    id: UUID
    name: str
    gender: str
    dob: date
    specialty: str
    phone: str
    address: str
    department_id: UUID

    model_config = ConfigDict(from_attributes=True)
