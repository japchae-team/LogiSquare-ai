from pydantic import BaseModel


class DetectionItem(BaseModel):
    label: str
    confidence: float
    bbox: list[float]


class DetectionResponse(BaseModel):
    detections: list[DetectionItem]
    count: int

