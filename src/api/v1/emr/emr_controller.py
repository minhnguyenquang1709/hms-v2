from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Annotated
import logging
from .emr_service import EMRService
from src.config.db import get_db
from .dto import *
from src.api.v1.models.emr import EMR
from src.api.v1.models.appointment import Appointment
from src.api.v1.models.patient import Patient
from src.api.v1.models.doctor import Doctor

router = APIRouter(prefix="/emrs", tags=["Electronic Medical Records"])


@router.get("", response_model=List[EMRDto], status_code=status.HTTP_200_OK)
async def list_emrs(db: Annotated[AsyncSession, Depends(get_db)], dto: EMRFilterDto):
    return await EMRService.list_emrs(db, dto)


@router.post("", response_model=EMRDto, status_code=status.HTTP_201_CREATED)
async def create_emr(db: Annotated[AsyncSession, Depends(get_db)], dto: EMRCreateDto):
    return await EMRService.create_emr(db, dto)


@router.get("/{emr_id}", response_model=EMRDto, status_code=status.HTTP_200_OK)
async def get_emr_by_id(db: Annotated[AsyncSession, Depends(get_db)], emr_id: UUID):
    return await EMRService.get_emr_by_id(db, emr_id)


@router.patch("/{emr_id}", response_model=EMRDto, status_code=status.HTTP_200_OK)
async def update_emr(
    db: Annotated[AsyncSession, Depends(get_db)],
    emr_id: UUID,
    update_data: EMRUpdateDto,
):
    return await EMRService.update_emr(db, emr_id, update_data)


@router.delete("/{emr_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_emr(db: Annotated[AsyncSession, Depends(get_db)], emr_id: UUID):
    return await EMRService.delete_emr(db, emr_id)
