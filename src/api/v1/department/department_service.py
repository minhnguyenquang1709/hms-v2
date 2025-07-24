from sqlalchemy.ext.asyncio import AsyncSession
from .dto import *
import logging
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.api.v1.models.department import Department
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


class DepartmentService:
    @staticmethod
    async def list_departments(db: AsyncSession):
        try:
            result = await db.execute(select(Department))
            departments = result.scalars().all()
            return [DepartmentDto.model_validate(d) for d in departments]

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving departments",
            )

    @staticmethod
    async def create_department(db: AsyncSession, department_data: DepartmentCreateDto):
        try:
            department = Department(**department_data.model_dump())
            db.add(department)
            await db.commit()
            await db.refresh(department)
            return DepartmentDto.model_validate(department)

        except IntegrityError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department name must be unique",
            )

        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating department",
            )

    @staticmethod
    async def get_department_by_id(db: AsyncSession, department_id: UUID):
        try:
            result = await db.execute(
                select(Department).where(Department.id == department_id)
            )
            department = result.scalars().first()

            if not department:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
                )

            return DepartmentDto.model_validate(department)

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving department",
            )

    @staticmethod
    async def update_department(
        db: AsyncSession, department_id: UUID, update_data: DepartmentUpdateDto
    ):
        try:
            result = await db.execute(
                select(Department).where(Department.id == department_id)
            )
            department = result.scalars().first()

            if not department:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
                )

            update_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(department, key, value)

            await db.commit()
            await db.refresh(department)
            return DepartmentDto.model_validate(department)

        except IntegrityError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department name must be unique",
            )

        except HTTPException:
            raise

        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating department",
            )

    @staticmethod
    async def delete_department(db: AsyncSession, department_id: UUID):
        try:
            result = await db.execute(
                select(Department).where(Department.id == department_id)
            )
            department = result.scalars().first()

            if not department:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
                )

            await db.delete(department)
            await db.commit()
            return None

        except IntegrityError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete department with associated doctors or appointments",
            )

        except HTTPException:
            raise

        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting department",
            )
