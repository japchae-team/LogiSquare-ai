from fastapi import HTTPException, UploadFile, status

from app.models.yolo_detector import yolo_detector
from app.schemas.safety import DetectionResponse


class SafetyService:
    async def detect(self, file: UploadFile) -> DetectionResponse:
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image file is required",
            )

        detections = await yolo_detector.detect(file)
        return DetectionResponse(detections=detections, count=len(detections))


safety_service = SafetyService()

