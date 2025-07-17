from fastapi import APIRouter

router = APIRouter(prefix="/departments", tags=["departments"])


@router.get("/")
async def list_departments():
    return {"message": "List of departments"}


@router.post("/")
async def create_departments():
    pass


@router.get("/{appointment_id}")
async def get_department(department_id: int):
    pass


@router.patch("/{appointment_id}")
async def update_department(department_id: int):
    pass


@router.delete("/{appointment_id}")
async def delete_department(department_id: int):
    pass
