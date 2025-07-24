from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Annotated
import logging

from src.config.db import get_db
from .dto import EMRDto, EMRCreateDto, EMRUpdateDto
from src.api.v1.models.emr import EMR
from src.api.v1.models.appointment import Appointment
from src.api.v1.models.patient import Patient
from src.api.v1.models.doctor import Doctor

router = APIRouter(prefix="/emrs", tags=["Electronic Medical Records"])
logger = logging.getLogger(__name__)

@router.get("", response_model=List[EMRDto], status_code=status.HTTP_200_OK)
async def list_emrs(
    db: Annotated[AsyncSession, Depends(get_db)]
):
    try:
        result = await db.execute(select(EMR))
        emrs = result.scalars().all()
        return [EMRDto.model_validate(e) for e in emrs]
    
    except Exception as e:
        logger.error(f"Error listing EMRs: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving medical records"
        )

@router.post("", response_model=EMRDto, status_code=status.HTTP_201_CREATED)
async def create_emr(
    db: Annotated[AsyncSession, Depends(get_db)],
    emr_data: EMRCreateDto
):
    try:
        # Validate relationships
        appointment = await db.get(Appointment, emr_data.appointment_id)
        if not appointment:
            raise HTTPException(404, "Appointment not found")
            
        patient = await db.get(Patient, emr_data.patient_id)
        if not patient:
            raise HTTPException(404, "Patient not found")
            
        doctor = await db.get(Doctor, emr_data.doctor_id)
        if not doctor:
            raise HTTPException(404, "Doctor not found")
        
        # Create EMR
        emr = EMR(**emr_data.model_dump())
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
            detail="Data integrity violation"
        )
    
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating EMR: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating medical record"
        )

@router.get("/{emr_id}", response_model=EMRDto, status_code=status.HTTP_200_OK)
async def get_emr(
    db: Annotated[AsyncSession, Depends(get_db)],
    emr_id: UUID
):
    try:
        result = await db.execute(
            select(EMR).where(EMR.id == emr_id)
        )
        emr = result.scalars().first()
        
        if not emr:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical record not found"
            )
            
        return EMRDto.model_validate(emr)
    
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Error retrieving EMR: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving medical record"
        )

@router.patch("/{emr_id}", response_model=EMRDto, status_code=status.HTTP_200_OK)
async def update_emr(
    db: Annotated[AsyncSession, Depends(get_db)],
    emr_id: UUID,
    update_data: EMRUpdateDto
):
    try:
        result = await db.execute(
            select(EMR).where(EMR.id == emr_id)
        )
        emr = result.scalars().first()
        
        if not emr:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical record not found"
            )
            
        # Apply partial updates
        update_dict = update_data.model_dump(exclude_unset=True)
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
            detail="Data integrity violation"
        )
    
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating EMR: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating medical record"
        )

@router.delete("/{emr_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_emr(
    db: Annotated[AsyncSession, Depends(get_db)],
    emr_id: UUID
):
    try:
        result = await db.execute(
            select(EMR).where(EMR.id == emr_id)
        )
        emr = result.scalars().first()
        
        if not emr:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical record not found"
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
            detail="Error deleting medical record"
        )