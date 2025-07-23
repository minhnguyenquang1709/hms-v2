from typing import Annotated
from fastapi import APIRouter, Depends

from src.api.v1.models.appointment import Appointment
from src.config.db import get_db
from .dto import *
import logging
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.get("")
async def list_appointments(
  db: Annotated[AsyncSession, Depends(get_db)],
):
  """
  List all appointments.
  """
  try:
    query = select(Appointment)
    result = await db.execute(query)
    appointments = result.scalars().all()
    return [AppointmentDto.model_validate(a) for a in appointments]

@router.post("")
async def create_appointment():
  pass

@router.get("/{appointment_id}")
async def get_appointment(appointment_id: int):
  pass

@router.patch("/{appointment_id}")
async def update_appointment(appointment_id: int):
  pass

@router.delete("/{appointment_id}")
async def delete_appointment(appointment_id: int):
  pass