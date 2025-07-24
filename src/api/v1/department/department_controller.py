from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from src.config.db import get_db
from .dto import *
from sqlalchemy.ext.asyncio import AsyncSession
from .department_service import DepartmentService

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("", response_model=List[DepartmentDto], status_code=status.HTTP_200_OK)
async def list_departments(db: Annotated[AsyncSession, Depends(get_db)]):
    return await DepartmentService.list_departments(db)


@router.post("", response_model=DepartmentDto, status_code=status.HTTP_201_CREATED)
async def create_department(
    db: Annotated[AsyncSession, Depends(get_db)], department_data: DepartmentCreateDto
):
    return await DepartmentService.create_department(db, department_data)


@router.get(
    "/{department_id}", response_model=DepartmentDto, status_code=status.HTTP_200_OK
)
async def get_department_by_id(
    db: Annotated[AsyncSession, Depends(get_db)], department_id: UUID
):
    return await DepartmentService.get_department_by_id(db, department_id)


@router.patch(
    "/{department_id}", response_model=DepartmentDto, status_code=status.HTTP_200_OK
)
async def update_department(
    db: Annotated[AsyncSession, Depends(get_db)],
    department_id: UUID,
    update_data: DepartmentUpdateDto,
):
    return await DepartmentService.update_department(db, department_id, update_data)


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    db: Annotated[AsyncSession, Depends(get_db)], department_id: UUID
):
    return await DepartmentService.delete_department(db, department_id)
