from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

class EMRDto(BaseModel):
    id: UUID
    subjective_notes: str
    objective_notes: Dict[str, Any]
    assessment: str
    plan: str
    prescription: Dict[str, Any]
    created_at: datetime
    appointment_id: UUID
    patient_id: UUID
    doctor_id: UUID

    model_config = ConfigDict(from_attributes=True)

class EMRCreateDto(BaseModel):
    subjective_notes: str
    objective_notes: Dict[str, Any]
    assessment: str
    plan: str
    prescription: Dict[str, Any]
    appointment_id: UUID
    patient_id: UUID
    doctor_id: UUID

class EMRUpdateDto(BaseModel):
    subjective_notes: Optional[str] = None
    objective_notes: Optional[Dict[str, Any]] = None
    assessment: Optional[str] = None
    plan: Optional[str] = None
    prescription: Optional[Dict[str, Any]] = None