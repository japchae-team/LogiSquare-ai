import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "LogiSquare AI"
    yolo_model_path: str = os.getenv("YOLO_MODEL_PATH", "models/safety_yolo11.pt")
    yolo_confidence: float = float(os.getenv("YOLO_CONFIDENCE", "0.25"))


settings = Settings()

