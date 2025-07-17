from fastapi import APIRouter
from . import appointment, doctor, patient, emr

api_v1_router = APIRouter(prefix="/v1")
api_v1_router.include_router(appointment.router)
api_v1_router.include_router(doctor.router)
api_v1_router.include_router(patient.router)
api_v1_router.include_router(emr.router)