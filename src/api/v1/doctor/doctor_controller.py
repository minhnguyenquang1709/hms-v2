from datetime import date
from typing import Annotated, Literal
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from src.api.v1.models.department import Department
from src.config.db import get_db
from .doctor_service import DoctorService
from ..models.doctor import Doctor
from .dto import *
import logging
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.get("", response_model=list[DoctorDto], status_code=status.HTTP_200_OK)
async def list_doctors(
    # user_data: Annotated[
    #     UserData, Depends(require_permission(EPermission.READ_DOCTOR))
    # ],
    db: Annotated[AsyncSession, Depends(get_db)],
    dto: DoctorFilterDto,
):
    """
    List doctors.
    """
    return await DoctorService.list_doctors(db, dto)


@router.post("", response_model=DoctorDto, status_code=status.HTTP_201_CREATED)
async def create_doctor(
    # user_data: Annotated[
    #     UserData, Depends(require_permission(EPermission.CREATE_DOCTOR))
    # ],
    db: Annotated[AsyncSession, Depends(get_db)],
    dto: DoctorCreateDto,
):
    """Create a new doctor in database."""
    return await DoctorService.create_doctor(db, dto)


@router.get("/{doctor_id}", response_model=DoctorDto, status_code=status.HTTP_200_OK)
async def get_doctor_by_id(
    db: Annotated[AsyncSession, Depends(get_db)],
    doctor_id: UUID,
):
    return await DoctorService.get_doctor_by_id(db, doctor_id)


@router.patch("/{doctor_id}", response_model=DoctorDto)
async def update_doctor(
    # user_data: Annotated[
    #     UserData, Depends(require_permission(EPermission.UPDATE_DOCTOR))
    # ],
    db: Annotated[AsyncSession, Depends(get_db)],
    doctor_id: UUID,
    dto: DoctorUpdateDto,
):
    return await DoctorService.update_doctor(db, doctor_id, dto)


@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(
    # user_data: Annotated[
    #     UserData, Depends(require_permission(EPermission.DELETE_DOCTOR))
    # ],
    db: Annotated[AsyncSession, Depends(get_db)],
    doctor_id: UUID,
):
    """Delete a doctor."""
    return await DoctorService.delete_doctor(db, doctor_id)
