from fastapi import APIRouter

router = APIRouter(prefix="/patients", tags=["patients"])
@router.get("/")
async def list_patients():
  pass