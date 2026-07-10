from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class CameraCode(str, Enum):
    CCTV_A_01 = "CCTV-A-01"
    CCTV_A_02 = "CCTV-A-02"
    CCTV_B_01 = "CCTV-B-01"
    CCTV_C_01 = "CCTV-C-01"


class DetectionItem(BaseModel):
    label: str
    confidence: float
    bbox: list[float]


class DetectionSummary(BaseModel):
    label: str
    confidence: float


class DetectionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    camera_code: str = Field(alias="cameraCode")
    source_type: str = Field(alias="sourceType")
    event_type: str = Field(alias="eventType")
    confidence_score: float = Field(alias="confidenceScore")
    helmet_worn: bool | None = Field(alias="helmetWorn")
    vest_worn: bool | None = Field(alias="vestWorn")
    annotated_image_url: str = Field(alias="annotatedImageUrl")
    detections: list[DetectionSummary]
    count: int
