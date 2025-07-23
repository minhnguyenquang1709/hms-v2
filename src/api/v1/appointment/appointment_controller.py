from fastapi import APIRouter

router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.get("/")
async def list_appointments():
  return {"message": "List of appointments"}

@router.post("/")
async def create_appointment():
  pass

@router.get("/{appointment_id}")
async def get_appointment(appointment_id: int):
  pass

@router.patch("/{appointment_id}")
async def update_appointment(appointment_id: int):
  pass

@router.delete("/{appointment_id}")
async def delete_appointment(appointment_id: int):
  pass