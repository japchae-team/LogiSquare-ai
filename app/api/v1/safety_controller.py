from fastapi import APIRouter, File, UploadFile

from app.schemas.common import ApiResponse, ErrorResponse
from app.schemas.safety import DetectionResponse
from app.services.safety_service import safety_service

router = APIRouter()


@router.post(
    "/detect",
    response_model=ApiResponse[DetectionResponse],
    responses={
        400: {"model": ErrorResponse, "description": "Invalid image file"},
        422: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def detect_safety_equipment(file: UploadFile = File(...)) -> ApiResponse[DetectionResponse]:
    result = await safety_service.detect(file)
    return ApiResponse(success=True, data=result, message="Detection completed")

