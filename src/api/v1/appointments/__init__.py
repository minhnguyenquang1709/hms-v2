from fastapi import APIRouter
from ...v1 import api_v1_router

router = APIRouter(prefix="/appointments")
router.include_router(api_v1_router)
