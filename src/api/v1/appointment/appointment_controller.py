from typing import Annotated, List
from fastapi import APIRouter, Depends, status

from .appointment_service import AppointmentService
from src.config.db import get_db
from .dto import *
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.get("", response_model=List[AppointmentDto], status_code=status.HTTP_200_OK)
async def list_appointments(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    List all appointments.
    """
    return await AppointmentService.list_appointments(db)


@router.post(
    "", response_model=AppointmentCreateDto, status_code=status.HTTP_201_CREATED
)
async def create_appointment(
    db: Annotated[AsyncSession, Depends(get_db)],
    appointment_create_dto: AppointmentCreateDto,
):
    return await AppointmentService.create_appointment(db, appointment_create_dto)


@router.get(
    "/{appointment_id}", response_model=AppointmentDto, status_code=status.HTTP_200_OK
)
async def get_appointment(
    db: Annotated[AsyncSession, Depends(get_db)], appointment_id: UUID
):
    return await AppointmentService.get_appointment(db, appointment_id)


@router.patch(
    "/{appointment_id}",
    response_model=AppointmentUpdateDto,
    status_code=status.HTTP_200_OK,
)
async def update_appointment(
    db: Annotated[AsyncSession, Depends(get_db)],
    appointment_id: UUID,
    update_data: AppointmentUpdateDto,
):
    return await AppointmentService.update_appointment(db, appointment_id, update_data)


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(
    db: Annotated[AsyncSession, Depends(get_db)], appointment_id: UUID
):
    return await AppointmentService.delete_appointment(db, appointment_id)

