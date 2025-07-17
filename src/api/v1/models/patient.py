from typing import TYPE_CHECKING, Optional, List
from sqlalchemy import Text, ForeignKey, TIMESTAMP, UUID, func, Date, ARRAY
from sqlalchemy.orm import (
    mapped_column,  # detailed column configuration (constraints, defaults, etc.)
    relationship,  # link b/w ORM classes (not db columns), bidirectional with back_populates
    Mapped,  # annotation that maps Python datatypes to table column datatypes, e.g. int->INTEGER, str->VARCHAR, Optional for nullability
)
import uuid
from datetime import datetime, date
from ....config.db import Base

if TYPE_CHECKING:
    from .appointment import Appointment
    from .emr import EMR


class Patient(Base):
    __tablename__ = "patients"

    # --- Columns (Tất cả đều là NOT NULL) ---
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    gender: Mapped[str] = mapped_column(Text, nullable=False)
    dob: Mapped[date] = mapped_column(Date, nullable=False)
    phone: Mapped[str] = mapped_column(Text, nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    chronic_conditions: Mapped[List[str]] = mapped_column(ARRAY(Text), nullable=False)

    # --- Relationships ---
    # 1-many
    appointments: Mapped[List["Appointment"]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )

    # 1-many
    medical_records: Mapped[List["EMR"]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )
