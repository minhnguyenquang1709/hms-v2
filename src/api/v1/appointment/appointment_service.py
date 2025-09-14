from fastapi import HTTPException, status
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from .dto import *
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.v1.models.appointment import Appointment

logger = logging.getLogger(__name__)


class AppointmentService:
    def __init__(self):
        pass

    @staticmethod
    async def list_appointments(db: AsyncSession):
        try:
            query = select(Appointment)
            result = await db.execute(query)
            appointments = result.scalars().all()

            return [AppointmentDto.model_validate(a) for a in appointments]
        except IntegrityError as e:
            logger.error(f"Integrity error while listing appointments: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Integrity error occurred.",
            )
        except Exception as e:
            logger.error(f"Error listing appointments: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while listing appointments.",
            )

    @staticmethod
    async def create_appointment(
        db: AsyncSession, appointment_create_dto: AppointmentCreateDto
    ):
        try:
            appt = Appointment(**appointment_create_dto.model_dump())
            db.add(appt)
            await db.commit()
        except IntegrityError as e:
            await db.rollback()
            logger.error(f"Integrity error while creating appointment: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Integrity error occurred.",
            )
        except Exception as e:
            await db.rollback()
            logger.error(f"Error creating appointment: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while creating the appointment\n{appointment_create_dto.model_dump()}.",
            )

    @staticmethod
    async def get_appointment(db: AsyncSession, appointment_id: UUID):
        try:
            query = select(Appointment).where(Appointment.id == appointment_id)
            result = await db.execute(query)
            appt = result.scalars().first()
            if not appt:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Appointment not found.",
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

    @staticmethod
    async def update_appointment(
        db: AsyncSession, appointment_id: UUID, update_data: AppointmentUpdateDto
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
            for key, value in update_data.model_dump().items():
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

    @staticmethod
    async def delete_appointment(db: AsyncSession, appointment_id: UUID):
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

    @staticmethod
    async def list_departments(db: AsyncSession):
        try:
            result = await db.execute(select(Appointment.department_id).distinct())
            departments = result.scalars().all()
            return departments
        except IntegrityError as e:
            logger.error(f"Integrity error while listing departments: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Integrity error occurred.",
            )
        except Exception as e:
            logger.error(f"Error listing departments: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while listing departments.",
            )