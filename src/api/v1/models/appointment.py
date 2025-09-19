from enum import Enum
from ....config.db import Base
from typing import TYPE_CHECKING, Optional
from sqlalchemy import (
    DateTime,
    Text,
    ForeignKey,
    TIMESTAMP,
    UUID,
    func,
    Enum as SQLAlchemyEnum,
    INTEGER,
)
from sqlalchemy.orm import (
    mapped_column,  # detailed column configuration (constraints, defaults, etc.)
    relationship,  # link b/w ORM classes (not db columns), bidirectional with back_populates
    Mapped,  # annotation that maps Python datatypes to table column datatypes, e.g. int->INTEGER, str->VARCHAR, Optional for nullability
)
import uuid
import datetime

# avoid circular imports
if TYPE_CHECKING:
    from .department import Department
    from .auth import User, PatientProfile, DoctorProfile


class AppointmentStatus(str, Enum):
    BOOKED = "booked"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"
    NOSHOW = "noshow"


class Reason(Base):
    __tablename__ = "reason"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    display: Mapped[str] = mapped_column(Text, nullable=False)


class Appointment(Base):
    __tablename__ = "appointment"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    status: Mapped[AppointmentStatus] = mapped_column(
        SQLAlchemyEnum(AppointmentStatus, create_type=True),
        nullable=False,
        default=AppointmentStatus.BOOKED,
        index=True,
        doc="Trạng thái hiện tại của cuộc hẹn, dựa trên vòng đời của FHIR.",
    )

    start_time: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        doc="Thời điểm bắt đầu cuộc hẹn (theo chuẩn ISO 8601, múi giờ UTC).",
    )

    end_time: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        doc="Thời điểm kết thúc cuộc hẹn (theo chuẩn ISO 8601, múi giờ UTC).",
    )

    # Foreign Keys
    patient_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("patient_profile.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        doc="Tham chiếu đến bệnh nhân (User) tham gia cuộc hẹn.",
    )

    doctor_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("doctor_profile.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
        doc="Tham chiếu đến bác sĩ cụ thể (nếu có).",
    )

    department_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("department.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        doc="Tham chiếu đến khoa thực hiện dịch vụ (tương đương serviceType trong FHIR).",
    )

    reason: Mapped[Reason] = mapped_column(
        ForeignKey("reason.code", ondelete="RESTRICT"),
        nullable=False,
        doc="Lý do/triệu chứng chính của cuộc hẹn do người dùng cung cấp.",
    )

    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Ghi chú nội bộ của nhân viên y tế (tương đương comment trong FHIR).",
    )

    patient_instruction: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, doc="Hướng dẫn cụ thể cho bệnh nhân trước cuộc hẹn."
    )

    # Metadata
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # relationships
    patient: Mapped["PatientProfile"] = relationship(back_populates="appointments")
    doctor: Mapped[Optional["DoctorProfile"]] = relationship(back_populates="appointments")
    department: Mapped["Department"] = relationship(back_populates="appointments")
