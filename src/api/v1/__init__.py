from fastapi import APIRouter
from ...api import api_router

api_v1_router = APIRouter(prefix="/v1")
api_v1_router.include_router(api_router)
