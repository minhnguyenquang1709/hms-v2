from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.models.department import Department
from .dto import *
import logging
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.api.v1.models.doctor import Doctor
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


class DoctorService:
    @staticmethod
    async def list_doctors(db: AsyncSession, doctor_filter_dto: DoctorFilterDto):
        try:
            query = select(Doctor)

            if doctor_filter_dto.id:
                query = query.where(Doctor.id == id)
            if doctor_filter_dto.name:
                query = query.where(Doctor.name.icontains(doctor_filter_dto.name))
            if doctor_filter_dto.gender:
                query = query.where(Doctor.gender == doctor_filter_dto.gender)
            if doctor_filter_dto.dob:
                query = query.where(Doctor.dob == doctor_filter_dto.dob)
            if doctor_filter_dto.specialty:
                query = query.where(
                    Doctor.specialty.icontains(doctor_filter_dto.specialty)
                )
            if doctor_filter_dto.phone:
                query = query.where(Doctor.phone.ilike(f"%{doctor_filter_dto.phone}%"))
            if doctor_filter_dto.address:
                query = query.where(Doctor.address.icontains(doctor_filter_dto.address))

            logger.debug(f"Executing query: {query}")

            result = await db.execute(query)
            doctors = result.scalars().all()  # returns a list

            return [DoctorDto.model_validate(d) for d in doctors]

        except Exception as e:
            logger.error(f"Error fetching doctors: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Error retrieving doctors")

    @staticmethod
    async def create_doctor(db: AsyncSession, dto: DoctorCreateDto):
        try:
            doctor = Doctor(**dto.model_dump())

            db.add(doctor)
            await db.commit()
            await db.refresh(
                doctor
            )  # doctor now contains the database-generated values

            DoctorDto.model_validate(doctor)

            return doctor
        except (
            IntegrityError
        ) as e:  # client sent data that violates database constraints
            await db.rollback()
            logger.error(f"Error creating doctor: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Integrity error occurred.",
            )

        except Exception as e:
            await db.rollback()
            logger.error(f"Error creating doctor: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating doctor",
            )

    @staticmethod
    async def get_doctor_by_id(db: AsyncSession, doctor_id: UUID):
        try:
            query = select(Doctor).where(Doctor.id == doctor_id)
            result = await db.execute(query)

            doctor = result.scalars().first()
            if not doctor:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Doctor with id {doctor_id} not found",
                )

            return doctor
        except HTTPException:
            logger.error(f"Doctor with id {doctor_id} not found.")
            raise
        except IntegrityError as e:
            logger.error(f"Database error while fetching doctor {doctor_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database error while fetching doctor: {e}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error",
            )

    @staticmethod
    async def update_doctor(db: AsyncSession, doctor_id: UUID, dto: DoctorUpdateDto):
        try:
            # 1. fetch existing entity
            query = select(Doctor).where(Doctor.id == doctor_id)
            result = await db.execute(query)
            doctor = result.scalars().first()
            if not doctor:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Doctor with id {doctor_id} not found",
                )

            # 2. validate department if provided
            if dto.department_id:
                dept_query = select(Department).where(
                    Department.id == dto.department_id
                )
                dept_result = await db.execute(dept_query)
                department = dept_result.scalars().first()
                if not department:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Department with id {dto.department_id} not found",
                    )

            # 3. apply partial updates
            update_dict = dto.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(doctor, key, value)

            # 4. commit changes
            await db.commit()
            await db.refresh(doctor)  # refresh to get updated values

            return doctor

        except HTTPException:
            logger.error(f"Doctor with id {doctor_id} not found.")
            raise
        except IntegrityError as e:
            await db.rollback()
            logger.error(f"Database error while updating doctor {doctor_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database error while updating doctor: {e}",
            )
        except Exception as e:
            await db.rollback()
            logger.error(f"Error updating doctor {doctor_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating doctor: {e}",
            )

    @staticmethod
    async def delete_doctor(db: AsyncSession, doctor_id: UUID):
        try:
            query = select(Doctor).where(Doctor.id == doctor_id)
            result = await db.execute(query)
            doctor = result.scalars().first()
            if not doctor:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Doctor with id {doctor_id} not found",
                )

            await db.delete(doctor)
            await db.commit()

        except HTTPException:
            logger.error(f"Doctor with id {doctor_id} not found.")
            raise

        except IntegrityError as e:
            await db.rollback()
            logger.error(f"Database error while deleting doctor {doctor_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database error while deleting doctor: {e}",
            )
        except Exception as e:
            await db.rollback()
            logger.error(f"Error deleting doctor {doctor_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting doctor: {e}",
            )
