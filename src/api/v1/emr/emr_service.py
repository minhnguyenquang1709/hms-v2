from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import logging

from src.api.v1.emr.dto.dto import EMRFilterDto
from .dto import EMRDto, EMRCreateDto, EMRUpdateDto
from src.api.v1.models.emr import EMR
from src.api.v1.models.appointment import Appointment
from src.api.v1.models.patient import Patient
from src.api.v1.models.doctor import Doctor

logger = logging.getLogger(__name__)


class EMRService:
    @staticmethod
    async def list_emrs(db: AsyncSession, dto: EMRFilterDto):
        try:
            result = await db.execute(select(EMR))
            emrs = result.scalars().all()
            return [EMRDto.model_validate(e) for e in emrs]

        except Exception as e:
            logger.error(f"Error listing EMRs: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving medical records",
            )

    @staticmethod
    async def create_emr(db: AsyncSession, dto: EMRCreateDto):
        try:
            # Validate relationships
            appointment = await db.get(Appointment, dto.appointment_id)
            if not appointment:
                raise HTTPException(404, "Appointment not found")

            patient = await db.get(Patient, dto.patient_id)
            if not patient:
                raise HTTPException(404, "Patient not found")

            doctor = await db.get(Doctor, dto.doctor_id)
            if not doctor:
                raise HTTPException(404, "Doctor not found")

            # Create EMR
            emr = EMR(**dto.model_dump())
            db.add(emr)
            await db.commit()
            await db.refresh(emr)
            return EMRDto.model_validate(emr)

        except HTTPException:
            raise  # Re-raise validation errors

        except IntegrityError as e:
            await db.rollback()
            logger.error(f"Integrity error creating EMR: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data integrity violation",
            )

        except Exception as e:
            await db.rollback()
            logger.error(f"Error creating EMR: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating medical record",
            )

    @staticmethod
    async def get_emr_by_id(db: AsyncSession, emr_id: UUID):
        try:
            result = await db.execute(select(EMR).where(EMR.id == emr_id))
            emr = result.scalars().first()

            if not emr:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Medical record not found",
                )

            return EMRDto.model_validate(emr)

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"Error retrieving EMR: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving medical record",
            )

    @staticmethod
    async def update_emr(db: AsyncSession, emr_id: UUID, dto: EMRUpdateDto):
        try:
            result = await db.execute(select(EMR).where(EMR.id == emr_id))
            emr = result.scalars().first()

            if not emr:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Medical record not found",
                )

            # Apply partial updates
            update_dict = dto.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(emr, key, value)

            await db.commit()
            await db.refresh(emr)
            return EMRDto.model_validate(emr)

        except HTTPException:
            raise

        except IntegrityError as e:
            await db.rollback()
            logger.error(f"Integrity error updating EMR: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data integrity violation",
            )

        except Exception as e:
            await db.rollback()
            logger.error(f"Error updating EMR: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating medical record",
            )

    @staticmethod
    async def delete_emr(db: AsyncSession, emr_id: UUID):
        try:
            result = await db.execute(select(EMR).where(EMR.id == emr_id))
            emr = result.scalars().first()

            if not emr:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Medical record not found",
                )

            await db.delete(emr)
            await db.commit()
            return None

        except HTTPException:
            raise

        except Exception as e:
            await db.rollback()
            logger.error(f"Error deleting EMR: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting medical record",
            )
