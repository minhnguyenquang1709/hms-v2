from fastapi import APIRouter

router = APIRouter(prefix="/emrs", tags=["Electronic Medical Records"])

@router.get("/")
async def list_emrs():
  return {"message": "List of electronic medical records"}