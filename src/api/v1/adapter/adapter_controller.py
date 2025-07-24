from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .adapter_service import AdapterService
from src.api.v1.adapter.dto.dto import CommandDto
from src.config.db import get_db


router = APIRouter(prefix="/v1/adapter", tags=["Adapter"])

@router.post("/command")
async def handle_command(db: Annotated[AsyncSession, Depends(get_db)], dto: CommandDto):
  """
  Handle incoming commands from external systems.
  """
  return await AdapterService.handle_command(db, dto)