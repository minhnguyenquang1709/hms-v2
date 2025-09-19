# import uuid
# from datetime import time
# from typing import TYPE_CHECKING, Optional

# from sqlalchemy import (
#     UUID,
#     ForeignKey,
#     Integer,
#     Time,
# )
# from sqlalchemy.orm import Mapped, mapped_column, relationship

# from ....config.db import Base

# if TYPE_CHECKING:
#     from .department import Department


# class WorkingHours(Base):
#     __tablename__ = "working_hour"

#     id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
#     )
#     department_id: Mapped[uuid.UUID] = mapped_column(
#         ForeignKey("department.id"), nullable=False
#     )
#     # 1=Monday, 2=Tuesday, ..., 7=Sunday by ISO 8601
#     day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)

#     start_time_morning: Mapped[Optional[time]] = mapped_column(Time)
#     end_time_morning: Mapped[Optional[time]] = mapped_column(Time)
#     start_time_afternoon: Mapped[Optional[time]] = mapped_column(Time)
#     end_time_afternoon: Mapped[Optional[time]] = mapped_column(Time)

#     # --- Relationships ---
#     # 1 working hours - 1 department
#     department: Mapped["Department"] = relationship(back_populates="working_hours")
