import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    UUID,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ....config.db import Base

if TYPE_CHECKING:
    from .appointment import Appointment
    from .emr import EMR
    from .working_hours import WorkingHours
    from .doctor import Doctor


class Department(Base):
    __tablename__ = "department"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    # --- Relationships ---
    # 1 department - many doctors
    doctors: Mapped[List["Doctor"]] = relationship(back_populates="department")
    
    # 1 department - many appointments
    appointments: Mapped[List["Appointment"]] = relationship(back_populates="department")

    # 1 department - many working hours
    working_hours: Mapped[List["WorkingHours"]] = relationship(
        back_populates="department", cascade="all, delete-orphan"
    )