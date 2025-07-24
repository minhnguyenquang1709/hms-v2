from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status

from src.api.v1.models.appointment import Appointment
from src.config.db import get_db
from .dto import *
import logging
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/appointments", tags=["Appointments"])
logger = logging.getLogger(__name__)


@router.get("", response_model=List[AppointmentDto], status_code=status.HTTP_200_OK)
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
    except IntegrityError as e:
        logger.error(f"Integrity error while listing appointments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error occurred."
        )
    except Exception as e:
        logger.error(f"Error listing appointments: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while listing appointments.",
        )


@router.post(
    "", response_model=AppointmentCreateDto, status_code=status.HTTP_201_CREATED
)
async def create_appointment(
    db: Annotated[AsyncSession, Depends(get_db)],
    appointment_create_dto: AppointmentCreateDto,
):
    try:
        appt = Appointment(**appointment_create_dto.model_dump())
        db.add(appt)
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Integrity error while creating appointment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error occurred."
        )
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating appointment: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the appointment\n{appointment_create_dto.model_dump()}.",
        )


@router.get(
    "/{appointment_id}", response_model=AppointmentDto, status_code=status.HTTP_200_OK
)
async def get_appointment(
    db: Annotated[AsyncSession, Depends(get_db)], appointment_id: UUID
):
    try:
        query = select(Appointment).where(Appointment.id == appointment_id)
        result = await db.execute(query)
        appt = result.scalars().first()
        if not appt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found."
            )
        return AppointmentDto.model_validate(appt)

    except HTTPException:
        logger.error(f"Appointment with id {appointment_id} not found.")
        raise
    except IntegrityError as e:
        logger.error(f"Integrity error while fetching appointment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Integrity error occurred while fetching appointment with id {appointment_id}.",
        )
    except Exception as e:
        logger.error(f"Error fetching appointment: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching the appointment with id {appointment_id}.",
        )


@router.patch(
    "/{appointment_id}",
    response_model=AppointmentUpdateDto,
    status_code=status.HTTP_200_OK,
)
async def update_appointment(
    db: Annotated[AsyncSession, Depends(get_db)],
    appointment_id: UUID,
):
    try:
        query = select(Appointment).where(Appointment.id == appointment_id)
        result = await db.execute(query)
        appt = result.scalars().first()
        if not appt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Appointment {appointment_id} not found.",
            )
        appointment_data = AppointmentUpdateDto.model_validate(appt)
        for key, value in appointment_data.model_dump().items():
            if value is not None:
                setattr(appt, key, value)
        await db.commit()
        await db.refresh(appt)
        return AppointmentDto.model_validate(appt)
    except HTTPException:
        logger.error(f"Appointment with id {appointment_id} not found.")
        raise
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Integrity error while updating appointment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Integrity error occurred while updating appointment with id {appointment_id}.",
        )
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating appointment: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the appointment with id {appointment_id}.",
        )


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(
    db: Annotated[AsyncSession, Depends(get_db)], appointment_id: UUID
):
    try:
        query = select(Appointment).where(Appointment.id == appointment_id)
        result = await db.execute(query)
        appt = result.scalars().first()
        if not appt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Appointment {appointment_id} not found.",
            )
        await db.delete(appt)
        await db.commit()
    except HTTPException:
        logger.error(f"Appointment with id {appointment_id} not found.")
        raise
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Integrity error while deleting appointment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Integrity error occurred while deleting appointment with id {appointment_id}.",
        )
    except Exception as e:
        await db.rollback()
        logger.error(f"Error deleting appointment: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the appointment with id {appointment_id}.",
        )
