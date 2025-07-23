from datetime import date
from typing import Literal
from fastapi import APIRouter
from uuid import UUID
from .dto import *
import logging

router = APIRouter(prefix="/doctors", tags=["doctors"])
logger = logging.getLogger(__name__)


@router.get("", response_model=list[Doctor])
async def list_doctors(
    # user_data: Annotated[
    #     UserData, Depends(require_permission(EPermission.READ_DOCTOR))
    # ],
    doctor_id: UUID | None = None,
    name: str | None = None,
    gender: Literal["Male", "Female"] | None = None,
    dob: date | None = None,
    specialty: str | None = None,
    phone: str | None = None,
    address: str | None = None,
):
    """
    List doctors.
    """
    try:
        async with async_session_factory() as session:
            query = select(Doctor)

            filters = []
            if doctor_id:
                filters.append(Doctor.id == doctor_id)
            if name:
                filters.append(Doctor.name.ilike(f"%{name}%"))
            if gender:
                filters.append(Doctor.gender == gender)
            if dob:
                filters.append(Doctor.dob == dob)
            if specialty:
                filters.append(Doctor.specialty.ilike(f"%{specialty}%"))
            if phone:
                filters.append(Doctor.phone.ilike(f"%{phone}%"))
            if address:
                filters.append(Doctor.address.ilike(f"%{address}%"))

            if filters:
                query = query.where(and_(*filters))

            logger.debug(f"Executing query: {query}")

            result = await session.execute(query)
            doctors = result.scalars().all()

            return [DoctorResponse.model_validate(d) for d in doctors]

    except Exception as e:
        logger.error(f"Error fetching doctors: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error retrieving doctors")


@router.post("")
async def create_doctor(
    # user_data: Annotated[
    #     UserData, Depends(require_permission(EPermission.CREATE_DOCTOR))
    # ],
    doctor: Doctor,
):
    """Create a new doctor in database."""
    query = """INSERT INTO doctors (doctor_id, name, gender, dob, specialty, phone, email, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id, doctor_id, name, gender, dob, specialty, phone, email, address;"""
    try:
        with pool.connection() as conn, conn.cursor(row_factory=dict_row) as cur:
            created_doctor = cur.execute(
                query=query,
                params=(
                    doctor.doctor_id,
                    doctor.name,
                    doctor.gender,
                    doctor.dob,
                    doctor.specialty,
                    doctor.phone,
                    doctor.email,
                    doctor.address,
                ),
            ).fetchone()
            conn.commit()

            if not created_doctor:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create doctor",
                )
            return Doctor(**created_doctor)
    except psycopg.Error as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


@router.get("/{doctor_id}")
async def get_doctor_by_id(doctor_id: UUID):
    try:
        with pool.connection() as conn, conn.cursor(row_factory=dict_row) as cur:
            doctor_data = cur.execute(
                "SELECT * FROM doctors WHERE doctor_id = %s;", params=(doctor_id,)
            ).fetchone()

            if not doctor_data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Could not find doctor with id {doctor_id}",
                )

            return Doctor(**doctor_data)

    except psycopg.Error as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


@router.patch("/{doctor_id}", response_model=Doctor)
async def update_doctor(
    # user_data: Annotated[
    #     UserData, Depends(require_permission(EPermission.UPDATE_DOCTOR))
    # ],
    doctor_id: UUID,
    doctor_data: DoctorUpdate,
):

    data_to_update = doctor_data.model_dump(exclude_unset=True)

    if not data_to_update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided in the request to update.",
        )

    # Ensure doctor_id is not in the update set
    if "doctor_id" in data_to_update:
        del data_to_update["doctor_id"]

    if not data_to_update:  # Re-check after potentially removing doctor_id
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields to update provided after filtering.",
        )

    cols_to_set = [f"{key} = %s" for key in data_to_update.keys()]
    params_values = list(data_to_update.values())
    params_values.append(doctor_id)  # For WHERE doctor_id = %s

    # Corrected RETURNING clause
    query = f"""
      UPDATE doctors
      SET {', '.join(cols_to_set)}
      WHERE doctor_id = %s
      RETURNING doctor_id, name, gender, dob, specialty, phone, email, address;
    """
    try:
        with pool.connection() as conn, conn.cursor(row_factory=dict_row) as cur:
            updated_doctor_data = cur.execute(
                query=query,
                params=tuple(params_values),
            ).fetchone()
            conn.commit()

            if not updated_doctor_data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Doctor with id {doctor_id} not found or no update was performed.",
                )

            return Doctor(**updated_doctor_data)
    except psycopg.Error as e:
        logger.error(f"Database error while updating doctor {doctor_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while updating doctor: {e}",
        )


@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(
    # user_data: Annotated[
    #     UserData, Depends(require_permission(EPermission.DELETE_DOCTOR))
    # ],
    doctor_id: UUID,
):
    """Delete a doctor."""
    try:
        with pool.connection() as conn, conn.cursor() as cur:
            cur.execute("DELETE FROM doctors WHERE doctor_id = %s;", (doctor_id,))
            if cur.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Doctor with id {doctor_id} not found",
                )
            conn.commit()
            return  # 204 No Content

    except psycopg.Error as e:
        logger.error(f"Database error while deleting doctor {doctor_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while deleting doctor: {e}",
        )
