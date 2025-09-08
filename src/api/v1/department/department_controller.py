from typing import Annotated
from fastapi import APIRouter, Depends, status
from src.config.db import get_db
from .dto import *
from sqlalchemy.ext.asyncio import AsyncSession
from .department_service import DepartmentService

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("", response_model=dict, status_code=status.HTTP_200_OK)
async def list_departments(db: Annotated[AsyncSession, Depends(get_db)]):
    data = await DepartmentService.list_departments(db)
    return {"data": data, "status": status.HTTP_200_OK}


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_department(
    db: Annotated[AsyncSession, Depends(get_db)], department_data: DepartmentCreateDto
):
    data = await DepartmentService.create_department(db, department_data)
    return {"data": data, "status": status.HTTP_201_CREATED}


@router.get("/{department_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def get_department_by_id(
    db: Annotated[AsyncSession, Depends(get_db)], department_id: UUID
):
    data = await DepartmentService.get_department_by_id(db, department_id)
    return {"data": data, "status": status.HTTP_200_OK}


@router.patch("/{department_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def update_department(
    db: Annotated[AsyncSession, Depends(get_db)],
    department_id: UUID,
    update_data: DepartmentUpdateDto,
):
    data = await DepartmentService.update_department(db, department_id, update_data)
    return {"data": data, "status": status.HTTP_200_OK}


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    db: Annotated[AsyncSession, Depends(get_db)], department_id: UUID
):
    data = await DepartmentService.delete_department(db, department_id)
    return {"data": data, "status": status.HTTP_204_NO_CONTENT}
