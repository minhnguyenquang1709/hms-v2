from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Annotated
import logging

from src.config.db import get_db
from .dto import PatientDto, PatientCreateDto, PatientUpdateDto
from src.api.v1.models.patient import Patient

router = APIRouter(prefix="/patients", tags=["Patients"])
logger = logging.getLogger(__name__)

@router.get("", response_model=List[PatientDto], status_code=status.HTTP_200_OK)
async def list_patients(
    db: Annotated[AsyncSession, Depends(get_db)]
):
    try:
        result = await db.execute(select(Patient))
        patients = result.scalars().all()
        return [PatientDto.model_validate(p) for p in patients]
    
    except Exception as e:
        logger.error(f"Error listing patients: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving patients"
        )

@router.post("", response_model=PatientDto, status_code=status.HTTP_201_CREATED)
async def create_patient(
    db: Annotated[AsyncSession, Depends(get_db)],
    patient_data: PatientCreateDto
):
    try:
        patient = Patient(**patient_data.model_dump())
        db.add(patient)
        await db.commit()
        await db.refresh(patient)
        return PatientDto.model_validate(patient)
    
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Integrity error creating patient: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data integrity violation (e.g., duplicate phone number)"
        )
    
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating patient: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating patient"
        )

@router.get("/{patient_id}", response_model=PatientDto, status_code=status.HTTP_200_OK)
async def get_patient(
    db: Annotated[AsyncSession, Depends(get_db)],
    patient_id: UUID
):
    try:
        result = await db.execute(
            select(Patient).where(Patient.id == patient_id)
        )
        patient = result.scalars().first()
        
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
            
        return PatientDto.model_validate(patient)
    
    except HTTPException:
        raise  # Re-raise handled exceptions
        
    except Exception as e:
        logger.error(f"Error retrieving patient: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving patient"
        )

@router.patch("/{patient_id}", response_model=PatientDto, status_code=status.HTTP_200_OK)
async def update_patient(
    db: Annotated[AsyncSession, Depends(get_db)],
    patient_id: UUID,
    update_data: PatientUpdateDto
):
    try:
        result = await db.execute(
            select(Patient).where(Patient.id == patient_id)
        )
        patient = result.scalars().first()
        
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
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
            detail="Data integrity violation"
        )
    
    except HTTPException:
        raise
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating patient: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating patient"
        )

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(
    db: Annotated[AsyncSession, Depends(get_db)],
    patient_id: UUID
):
    try:
        result = await db.execute(
            select(Patient).where(Patient.id == patient_id)
        )
        patient = result.scalars().first()
        
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
            
        await db.delete(patient)
        await db.commit()
        return None
    
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Integrity error deleting patient: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete patient with associated appointments or medical records"
        )
    
    except HTTPException:
        raise
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Error deleting patient: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting patient"
        )