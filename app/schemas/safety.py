from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DetectionItem(BaseModel):
    label: str
    confidence: float
    bbox: list[float]


class DetectionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    camera_id: int | None = Field(default=None, alias="cameraId")
    storage_location_id: int | None = Field(default=None, alias="storageLocationId")
    worker_id: int | None = Field(default=None, alias="workerId")
    source_type: str = Field(alias="sourceType")
    event_type: str = Field(alias="eventType")
    confidence_score: float = Field(alias="confidenceScore")
    helmet_worn: bool = Field(alias="helmetWorn")
    vest_worn: bool = Field(alias="vestWorn")
    shoes_worn: bool | None = Field(default=None, alias="shoesWorn")
    annotated_image_url: str = Field(alias="annotatedImageUrl")
    occurred_at: datetime | None = Field(default=None, alias="occurredAt")
    detections: list[DetectionItem]
    count: int
