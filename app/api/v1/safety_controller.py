from fastapi import APIRouter, File, Form, UploadFile

from app.schemas.common import ApiResponse, ErrorResponse
from app.schemas.safety import CameraCode, DetectionResponse
from app.services.safety_service import safety_service

router = APIRouter()


@router.post(
    "/detect",
    response_model=ApiResponse[DetectionResponse],
    response_model_exclude_none=True,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid image file"},
        422: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def detect_safety_equipment(
    file: UploadFile = File(...),
    cameraCode: CameraCode = Form(...),
) -> ApiResponse[DetectionResponse]:
    result = await safety_service.detect(file=file, camera_code=cameraCode.value)
    return ApiResponse(success=True, data=result, message="Detection completed")
