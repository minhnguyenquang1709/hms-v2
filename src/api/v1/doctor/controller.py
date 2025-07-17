from fastapi import APIRouter

router = APIRouter(prefix="/doctors", tags=["doctors"])

@router.get("/")
async def list_doctors():
  pass