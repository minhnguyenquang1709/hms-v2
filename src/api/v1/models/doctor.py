from typing import TYPE_CHECKING, List
from sqlalchemy import Text, ForeignKey, UUID, Date
from sqlalchemy.orm import (
    mapped_column,
    relationship,
    Mapped,
)
import uuid
from datetime import date

from ....config.db import Base

if TYPE_CHECKING:
    from .appointment import Appointment
    from .emr import EMR
    from .department import Department

class Doctor(Base):
    __tablename__ = "doctor"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    specialty: Mapped[str] = mapped_column(Text, nullable=False)
    gender: Mapped[str] = mapped_column(Text, nullable=False)
    dob: Mapped[date] = mapped_column(Date, nullable=False)
    phone: Mapped[str] = mapped_column(Text, nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    # Foreign Keys
    # user_id: Mapped[uuid.UUID] = mapped_column(
    #     ForeignKey("users.id"), unique=True, nullable=False
    # )
    department_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("department.id"), nullable=False
    )

    # --- Relationships ---
    # user: Mapped["User"] = relationship(back_populates="doctor")

    # 1 doctor - 1 department
    department: Mapped["Department"] = relationship(back_populates="doctors")

    # 1 doctor - many appointments
    appointments: Mapped[List["Appointment"]] = relationship(back_populates="doctor")

    # 1 doctor - many medical records
    emrs: Mapped[List["EMR"]] = relationship(back_populates="doctor")

