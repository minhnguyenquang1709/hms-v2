import datetime
from enum import Enum
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UUID, Enum as SQLAlchemyEnum, ForeignKey, Text, Date
from ....config.db import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .appointment import Appointment
    from .department import Department


class Role(str, Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    PATIENT = "patient"


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[Role] = mapped_column(
        SQLAlchemyEnum(Role, create_type=True), nullable=False, default=Role.PATIENT
    )

    # relationships
    patient_profile: Mapped["PatientProfile"] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    doctor_profile: Mapped["DoctorProfile"] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


class PatientProfile(Base):
    __tablename__ = "patient_profile"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="RESTRICT"),
        unique=True,
        nullable=False,
    )
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    gender: Mapped[str] = mapped_column(Text, nullable=False)
    dob: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    phone: Mapped[str] = mapped_column(Text, nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)

    # relationships
    user: Mapped["User"] = relationship(back_populates="patient_profile")
    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="patient", foreign_keys="[Appointment.patient_id]"
    )


class DoctorProfile(Base):
    __tablename__ = "doctor_profile"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="RESTRICT"),
        unique=True,
        nullable=False,
    )
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    gender: Mapped[str] = mapped_column(Text, nullable=False)
    dob: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    phone: Mapped[str] = mapped_column(Text, nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)

    department_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("department.id"), nullable=False
    )

    # relationships
    user: Mapped["User"] = relationship(back_populates="doctor_profile")

    # 1 doctor - 1 department
    department: Mapped["Department"] = relationship(back_populates="doctors")

    # 1 doctor - many appointments
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="doctor")
