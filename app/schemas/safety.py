from pydantic import BaseModel, ConfigDict, Field


class DetectionItem(BaseModel):
    label: str
    confidence: float
    bbox: list[float]


class DetectionSummary(BaseModel):
    label: str
    confidence: float


class DetectionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    source_type: str = Field(alias="sourceType")
    event_type: str = Field(alias="eventType")
    confidence_score: float = Field(alias="confidenceScore")
    helmet_worn: bool | None = Field(alias="helmetWorn")
    vest_worn: bool | None = Field(alias="vestWorn")
    annotated_image_url: str = Field(alias="annotatedImageUrl")
    detections: list[DetectionSummary]
    count: int
