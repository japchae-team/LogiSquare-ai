from fastapi import APIRouter, File, UploadFile

from app.schemas.common import ApiResponse
from app.schemas.safety import DetectionResponse
from app.services.safety_service import safety_service

router = APIRouter()


@router.post("/detect", response_model=ApiResponse[DetectionResponse])
async def detect_safety_equipment(file: UploadFile = File(...)) -> ApiResponse[DetectionResponse]:
    result = await safety_service.detect(file)
    return ApiResponse(success=True, data=result, message="Detection completed")

