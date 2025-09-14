from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AppointmentDto(BaseModel):
    id: UUID
    patient_id: UUID
    department_id: UUID
    doctor_id: Optional[UUID]
    start_time: datetime
    end_time: datetime
    status: str
    notes: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AppointmentCreateDto(BaseModel):
    patient_id: UUID
    department_id: UUID
    doctor_id: Optional[UUID] = None
    start_time: datetime
    # end_time: datetime
    status: Optional[str] = "scheduled"
    notes: Optional[str] = None

class AppointmentUpdateDto(BaseModel):
    patient_id: Optional[UUID] = None
    department_id: Optional[UUID] = None
    doctor_id: Optional[UUID] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None