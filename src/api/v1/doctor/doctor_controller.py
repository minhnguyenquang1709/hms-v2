from datetime import date
from typing import Annotated, Literal
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from src.api.v1.models.department import Department
from src.config.db import get_db

from ..models.doctor import Doctor
from .dto import *
import logging
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/doctors", tags=["doctors"])
logger = logging.getLogger(__name__)


@router.get("", response_model=list[DoctorDto], status_code=status.HTTP_200_OK)
async def list_doctors(
    # user_data: Annotated[
    #     UserData, Depends(require_permission(EPermission.READ_DOCTOR))
    # ],
    db: Annotated[AsyncSession, Depends(get_db)],
    doctor_id: UUID | None = None,
    name: str | None = None,
    gender: Literal["Male", "Female"] | None = None,
    dob: date | None = None,
    specialty: str | None = None,
    phone: str | None = None,
    address: str | None = None,
):
    """
    List doctors.
    """
    try:
        query = select(Doctor)

        if doctor_id:
            query = query.where(Doctor.id == doctor_id)
        if name:
            query = query.where(Doctor.name.icontains(name))
        if gender:
            query = query.where(Doctor.gender == gender)
        if dob:
            query = query.where(Doctor.dob == dob)
        if specialty:
            query = query.where(Doctor.specialty.icontains(specialty))
        if phone:
            query = query.where(Doctor.phone.ilike(f"%{phone}%"))
        if address:
            query = query.where(Doctor.address.icontains(address))

        logger.debug(f"Executing query: {query}")

        result = await db.execute(query)
        doctors = result.scalars().all()  # returns a list

        return [DoctorDto.model_validate(d) for d in doctors]

    except Exception as e:
        logger.error(f"Error fetching doctors: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error retrieving doctors")


@router.post("", response_model=DoctorDto, status_code=status.HTTP_201_CREATED)
async def create_doctor(
    # user_data: Annotated[
    #     UserData, Depends(require_permission(EPermission.CREATE_DOCTOR))
    # ],
    db: Annotated[AsyncSession, Depends(get_db)],
    doctor_data: DoctorCreateDto,
):
    """Create a new doctor in database."""
    try:
        doctor = Doctor(**doctor_data.model_dump())

        db.add(doctor)
        await db.commit()
        await db.refresh(doctor)  # doctor now contains the database-generated values

        DoctorDto.model_validate(doctor)

        return doctor
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Error creating doctor: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating doctor"
        )

    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating doctor: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating doctor",
        )


@router.get("/{doctor_id}", response_model=DoctorDto, status_code=status.HTTP_200_OK)
async def get_doctor_by_id(
    db: Annotated[AsyncSession, Depends(get_db)],
    doctor_id: UUID,
):
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


@router.patch("/{doctor_id}", response_model=DoctorDto)
async def update_doctor(
    # user_data: Annotated[
    #     UserData, Depends(require_permission(EPermission.UPDATE_DOCTOR))
    # ],
    db: Annotated[AsyncSession, Depends(get_db)],
    doctor_id: UUID,
    update_data: DoctorUpdateDto,
):
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
        if update_data.department_id:
            dept_query = select(Department).where(
                Department.id == update_data.department_id
            )
            dept_result = await db.execute(dept_query)
            department = dept_result.scalars().first()
            if not department:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Department with id {update_data.department_id} not found",
                )

        # 3. apply partial updates
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(doctor, key, value)

        # 4. commit changes
        await db.commit()
        await db.refresh(doctor)  # refresh to get updated values

        return doctor
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


@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(
    # user_data: Annotated[
    #     UserData, Depends(require_permission(EPermission.DELETE_DOCTOR))
    # ],
    db: Annotated[AsyncSession, Depends(get_db)],
    doctor_id: UUID,
):
    """Delete a doctor."""
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
