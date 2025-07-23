from typing import TYPE_CHECKING, Optional, Dict, Any
from sqlalchemy import Text, ForeignKey, TIMESTAMP, UUID, func, JSON
from sqlalchemy.orm import (
    mapped_column,
    relationship,
    Mapped,
)
import uuid
from datetime import datetime

from ....config.db import Base

if TYPE_CHECKING:
    from .patient import Patient
    from .doctor import Doctor
    from .appointment import Appointment


class EMR(Base):
    __tablename__ = "medical_record"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    subjective_notes: Mapped[Optional[str]] = mapped_column(Text)
    objective_notes: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    assessment: Mapped[str] = mapped_column(Text, nullable=False)
    plan: Mapped[Optional[str]] = mapped_column(Text)
    prescription: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )

    # Foreign Keys
    appointment_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("appointment.id"), unique=True, nullable=False
    )
    patient_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("patient.id"), nullable=False
    )
    doctor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("doctor.id"), nullable=False
    )

    # --- Relationships ---
    # 1 medical record - 1 appointment
    appointment: Mapped["Appointment"] = relationship(back_populates="emr")
    # 1 medical record - 1 patient
    patient: Mapped["Patient"] = relationship(back_populates="emrs")
    # 1 medical record - 1 doctor
    doctor: Mapped["Doctor"] = relationship(back_populates="emrs")
