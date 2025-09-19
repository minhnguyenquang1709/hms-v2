from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Annotated
import logging

from src.api.v1.patient.dto.dto import PatientProfileDto, PatientUpdateDto
from src.api.v1.response_dto import ResponseDto
from .patient_service import PatientService
from src.config.db import get_db

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.get("", response_model=ResponseDto, status_code=status.HTTP_200_OK)
async def list_patients(db: Annotated[AsyncSession, Depends(get_db)]):
    data = await PatientService.list_patients(db)
    return {"data": data, "status": status.HTTP_200_OK}


@router.post("", response_model=ResponseDto, status_code=status.HTTP_201_CREATED)
async def create_patient(
    db: Annotated[AsyncSession, Depends(get_db)], patient_data: PatientProfileDto
):
    data = await PatientService.create_patient(db, patient_data)
    return {"data": data, "status": status.HTTP_201_CREATED}


@router.get("/{patient_id}", response_model=ResponseDto, status_code=status.HTTP_200_OK)
async def get_patient(db: Annotated[AsyncSession, Depends(get_db)], patient_id: UUID):
    data = await PatientService.get_patient(db, patient_id)
    return {"data": data, "status": status.HTTP_200_OK}


@router.patch(
    "/{patient_id}", response_model=ResponseDto, status_code=status.HTTP_202_ACCEPTED
)
async def update_patient(
    db: Annotated[AsyncSession, Depends(get_db)],
    patient_id: UUID,
    update_data: PatientUpdateDto,
):
    data = await PatientService.update_patient(db, patient_id, update_data)
    return {"data": data, "status": status.HTTP_200_OK}


@router.delete(
    "/{patient_id}", response_model=ResponseDto, status_code=status.HTTP_202_ACCEPTED
)
async def delete_patient(
    db: Annotated[AsyncSession, Depends(get_db)], patient_id: UUID
):
    data = await PatientService.delete_patient(db, patient_id)
    return {"data": data, "status": status.HTTP_202_ACCEPTED}
