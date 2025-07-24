from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Annotated
import logging
from .patient_service import PatientService
from src.config.db import get_db
from .dto import PatientDto, PatientCreateDto, PatientUpdateDto
from src.api.v1.models.patient import Patient

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.get("", response_model=List[PatientDto], status_code=status.HTTP_200_OK)
async def list_patients(db: Annotated[AsyncSession, Depends(get_db)]):
    return await PatientService.list_patients(db)


@router.post("", response_model=PatientDto, status_code=status.HTTP_201_CREATED)
async def create_patient(
    db: Annotated[AsyncSession, Depends(get_db)], patient_data: PatientCreateDto
):
    return await PatientService.create_patient(db, patient_data)


@router.get("/{patient_id}", response_model=PatientDto, status_code=status.HTTP_200_OK)
async def get_patient(db: Annotated[AsyncSession, Depends(get_db)], patient_id: UUID):
    return await PatientService.get_patient(db, patient_id)


@router.patch(
    "/{patient_id}", response_model=PatientDto, status_code=status.HTTP_200_OK
)
async def update_patient(
    db: Annotated[AsyncSession, Depends(get_db)],
    patient_id: UUID,
    update_data: PatientUpdateDto,
):
    return await PatientService.update_patient(db, patient_id, update_data)


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(
    db: Annotated[AsyncSession, Depends(get_db)], patient_id: UUID
):
    return await PatientService.delete_patient(db, patient_id)
