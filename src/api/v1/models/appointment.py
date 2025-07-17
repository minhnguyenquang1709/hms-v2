from ....config.db import Base
from typing import TYPE_CHECKING, Optional
from sqlalchemy import Text, ForeignKey, TIMESTAMP, UUID, func
from sqlalchemy.orm import (
    mapped_column,  # detailed column configuration (constraints, defaults, etc.)
    relationship,  # link b/w ORM classes (not db columns), bidirectional with back_populates
    Mapped,  # annotation that maps Python datatypes to table column datatypes, e.g. int->INTEGER, str->VARCHAR, Optional for nullability
)
import uuid
from datetime import datetime

if TYPE_CHECKING:
    from .patient import Patient
    from .doctor import Doctor
    from .emr import EMR
    from .department import Department


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    start_time: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    end_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(
        Text, nullable=False, default="scheduled"
    )  # scheduled, completed, canceled
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )

    # Foreign Keys
    patient_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("patients.id"), nullable=False
    )
    department_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("departments.id"), nullable=False
    )
    doctor_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("doctors.id"))

    # --- Relationships ---
    patient: Mapped["Patient"] = relationship(back_populates="appointments")
    department: Mapped["Department"] = relationship(back_populates="appointments")
    doctor: Mapped[Optional["Doctor"]] = relationship(back_populates="appointments")

    emr: Mapped[Optional["EMR"]] = relationship(
        back_populates="appointment", cascade="all, delete-orphan"
    )
