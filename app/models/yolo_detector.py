from pathlib import Path

import cv2
import numpy as np
from fastapi import UploadFile
from ultralytics import YOLO

from app.core.config import settings
from app.schemas.safety import DetectionItem


class YoloDetector:
    def __init__(self) -> None:
        self._model: YOLO | None = None

    def _load_model(self) -> YOLO:
        if self._model is None:
            model_path = Path(settings.yolo_model_path)
            if not model_path.exists():
                raise FileNotFoundError(f"YOLO model file not found: {model_path}")
            self._model = YOLO(str(model_path))
        return self._model

    async def detect(self, file: UploadFile) -> list[DetectionItem]:
        contents = await file.read()
        if not contents:
            raise ValueError("Uploaded image file is empty")

        image = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Uploaded file could not be decoded as an image")

        model = self._load_model()
        results = model.predict(image, conf=settings.yolo_confidence, verbose=False)

        detections: list[DetectionItem] = []
        for result in results:
            names = result.names
            for box in result.boxes:
                class_id = int(box.cls[0].item())
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                detections.append(
                    DetectionItem(
                        label=names[class_id],
                        confidence=float(box.conf[0].item()),
                        bbox=[float(x1), float(y1), float(x2), float(y2)],
                    )
                )
        return detections


yolo_detector = YoloDetector()

