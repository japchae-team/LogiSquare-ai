from fastapi import APIRouter

from app.api.v1.safety_controller import router as safety_router

api_router = APIRouter()
api_router.include_router(safety_router, prefix="/safety", tags=["Safety"])

