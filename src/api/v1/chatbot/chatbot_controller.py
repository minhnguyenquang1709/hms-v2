from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.appointment.appointment_service import AppointmentService
from src.api.v1.appointment.dto.dto import AppointmentCreateDto
from src.api.v1.auth.dto.auth_dto import UserDto
from src.api.v1.chatbot.dto.dto import ChatbotAppointmentCreateDto
from src.api.v1.department.department_service import DepartmentService
from src.api.v1.utils.security import get_current_user
from ....config.db import get_db


router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


@router.post("/appointment")
async def create_appointment_via_chatbot(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[UserDto, Depends(get_current_user)],
    payload: ChatbotAppointmentCreateDto,
):
    """
    Create a new appointment from a chatbot's request.
    """
    try:
        appointment_data = AppointmentCreateDto(
            patient_id=current_user.id,
            department_id=payload.department_id,
            start_time=datetime.fromisoformat(payload.start_time),
            # end_time=datetime.fromisoformat(payload.start_time)
            # + timedelta(minutes=30),
        )
    except ValueError as e:
        return {
            "error": e,
            "message": "Invalid date format. Please use ISO 8601 format.",
        }

    return await AppointmentService.create_appointment(db, appointment_data)

@router.get("/departments")
async def list_departments(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    List all departments.
    """
    data = await DepartmentService.list_departments(db)
    return {"data": data, "status": status.HTTP_200_OK}