from typing import TYPE_CHECKING, List
from sqlalchemy import Text, UUID, ARRAY, Date
from sqlalchemy.orm import (
    mapped_column,
    relationship, 
    Mapped,
)
import uuid
from datetime import date

from ....config.db import Base

if TYPE_CHECKING:
    # from .user import User
    from .appointment import Appointment
    from .emr import EMR


class Patient(Base):
    __tablename__ = "patient"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    # user_id: Mapped[uuid.UUID] = mapped_column(
    #     UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False
    # )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    gender: Mapped[str] = mapped_column(Text, nullable=False)
    dob: Mapped[date] = mapped_column(Date, nullable=False)
    phone: Mapped[str] = mapped_column(Text, nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    chronic_conditions: Mapped[List[str]] = mapped_column(ARRAY(Text), nullable=False)

    # --- Relationships ---
    # 1 patient - 1 user
    # user: Mapped["User"] = relationship(back_populates="patient")

    # 1 patient - many appointments
    appointments: Mapped[List["Appointment"]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )

    # 1 patient - many medical records
    medical_records: Mapped[List["EMR"]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )
