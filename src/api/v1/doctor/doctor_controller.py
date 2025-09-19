from datetime import date
from typing import Annotated, Literal
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from src.api.v1.models.department import Department
from src.api.v1.response_dto import ResponseDto
from src.config.db import get_db
from .doctor_service import DoctorService
from .dto import *
import logging
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.get("", response_model=ResponseDto, status_code=status.HTTP_200_OK)
async def list_doctors(
    # user_data: Annotated[
    #     UserData, Depends(require_permission(EPermission.READ_DOCTOR))
    # ],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    List doctors.
    """
    data = await DoctorService.list_doctors(db)
    return {"data": data, "status": status.HTTP_200_OK}


@router.post("", response_model=ResponseDto, status_code=status.HTTP_201_CREATED)
async def create_doctor(
    # user_data: Annotated[
    #     UserData, Depends(require_permission(EPermission.CREATE_DOCTOR))
    # ],
    db: Annotated[AsyncSession, Depends(get_db)],
    dto: DoctorProfileDto,
):
    """Create a new doctor in database."""
    data = await DoctorService.create_doctor(db, dto)
    return {"data": data, "status": status.HTTP_201_CREATED}


@router.get("/{doctor_id}", response_model=ResponseDto, status_code=status.HTTP_200_OK)
async def get_doctor_by_id(
    db: Annotated[AsyncSession, Depends(get_db)],
    doctor_id: UUID,
):
    data = await DoctorService.get_doctor_by_id(db, doctor_id)
    return {"data": data, "status": status.HTTP_200_OK}


@router.patch(
    "/{doctor_id}", response_model=ResponseDto, status_code=status.HTTP_202_ACCEPTED
)
async def update_doctor(
    # user_data: Annotated[
    #     UserData, Depends(require_permission(EPermission.UPDATE_DOCTOR))
    # ],
    db: Annotated[AsyncSession, Depends(get_db)],
    doctor_id: UUID,
    dto: DoctorUpdateDto,
):
    data = await DoctorService.update_doctor(db, doctor_id, dto)
    return {"data": data, "status": status.HTTP_202_ACCEPTED}


@router.delete("/{doctor_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_doctor(
    # user_data: Annotated[
    #     UserData, Depends(require_permission(EPermission.DELETE_DOCTOR))
    # ],
    db: Annotated[AsyncSession, Depends(get_db)],
    doctor_id: UUID,
):
    """Delete a doctor."""
    data = await DoctorService.delete_doctor(db, doctor_id)
    return {"data": data, "status": status.HTTP_202_ACCEPTED}
