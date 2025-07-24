from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.v1.adapter.dto.dto import CommandDto
from src.api.v1.patient.dto.dto import PatientCreateDto
from src.api.v1.patient.patient_service import PatientService
from src.api.v1.utils.type import Command


class AdapterService:
    @staticmethod
    async def handle_command(db: AsyncSession, dto: CommandDto):
        try:
            command = dto.command
            payload = dto.payload

            if command == Command.CREATE_PATIENT.value:
                patient_create_dto = PatientCreateDto(**payload)
                return await PatientService.create_patient(db, patient_create_dto)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error handling command: {str(e)}",
            )
