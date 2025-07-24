from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import logging

from src.config.db import get_db
from .dto import PatientDto, PatientCreateDto, PatientUpdateDto
from src.api.v1.models.patient import Patient

logger = logging.getLogger(__name__)


class PatientService:
    @staticmethod
    async def list_patients(db: AsyncSession):
        try:
            result = await db.execute(select(Patient))
            patients = result.scalars().all()
            return [PatientDto.model_validate(p) for p in patients]

        except Exception as e:
            logger.error(f"Error listing patients: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving patients",
            )

    @staticmethod
    async def create_patient(db: AsyncSession, dto: PatientCreateDto):
        try:
            patient = Patient(**dto.model_dump())
            db.add(patient)
            await db.commit()
            await db.refresh(patient)
            return PatientDto.model_validate(patient)

        except IntegrityError as e:
            await db.rollback()
            logger.error(f"Integrity error creating patient: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data integrity violation (e.g., duplicate phone number)",
            )

        except Exception as e:
            await db.rollback()
            logger.error(f"Error creating patient: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating patient",
            )

    @staticmethod
    async def get_patient(db: AsyncSession, patient_id: UUID):
        try:
            result = await db.execute(select(Patient).where(Patient.id == patient_id))
            patient = result.scalars().first()

            if not patient:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
                )

            return PatientDto.model_validate(patient)

        except HTTPException:
            raise  # Re-raise handled exceptions

        except Exception as e:
            logger.error(f"Error retrieving patient: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving patient",
            )

    @staticmethod
    async def update_patient(
        db: AsyncSession, patient_id: UUID, update_data: PatientUpdateDto
    ):
        try:
            result = await db.execute(select(Patient).where(Patient.id == patient_id))
            patient = result.scalars().first()

            if not patient:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
                )

            # Apply partial updates
            update_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(patient, key, value)

            await db.commit()
            await db.refresh(patient)
            return PatientDto.model_validate(patient)

        except IntegrityError as e:
            await db.rollback()
            logger.error(f"Integrity error updating patient: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data integrity violation",
            )

        except HTTPException:
            raise

        except Exception as e:
            await db.rollback()
            logger.error(f"Error updating patient: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating patient",
            )

    @staticmethod
    async def delete_patient(db: AsyncSession, patient_id: UUID):
        try:
            result = await db.execute(select(Patient).where(Patient.id == patient_id))
            patient = result.scalars().first()

            if not patient:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
                )

            await db.delete(patient)
            await db.commit()
            return None

        except IntegrityError as e:
            await db.rollback()
            logger.error(f"Integrity error deleting patient: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete patient with associated appointments or medical records",
            )

        except HTTPException:
            raise

        except Exception as e:
            await db.rollback()
            logger.error(f"Error deleting patient: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting patient",
            )
