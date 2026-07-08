from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

import cv2
import numpy as np
from fastapi import UploadFile
from ultralytics import YOLO

from app.core.config import settings
from app.schemas.safety import DetectionItem


ANNOTATED_IMAGE_DIR = Path("uploads/safety-events")
ANNOTATED_IMAGE_URL_PREFIX = "/uploads/safety-events"


@dataclass(frozen=True)
class DetectionResult:
    detections: list[DetectionItem]
    annotated_image_url: str


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

    async def detect(self, file: UploadFile) -> DetectionResult:
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
        sorted_detections = sorted(detections, key=lambda detection: (detection.bbox[1], detection.bbox[0]))
        annotated_image_url = self._save_annotated_image(image, sorted_detections)
        return DetectionResult(detections=sorted_detections, annotated_image_url=annotated_image_url)

    def _save_annotated_image(self, image: np.ndarray, detections: list[DetectionItem]) -> str:
        ANNOTATED_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

        annotated_image = image.copy()
        for detection in detections:
            x1, y1, x2, y2 = (int(value) for value in detection.bbox)
            color = self._label_color(detection.label)
            label_text = f"{detection.label} {detection.confidence:.2f}"

            cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, 2)
            text_size, _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            text_width, text_height = text_size
            text_y = max(y1 - 8, text_height + 8)
            cv2.rectangle(
                annotated_image,
                (x1, text_y - text_height - 8),
                (x1 + text_width + 8, text_y + 4),
                color,
                -1,
            )
            cv2.putText(
                annotated_image,
                label_text,
                (x1 + 4, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

        file_name = f"{uuid4().hex}.jpg"
        output_path = ANNOTATED_IMAGE_DIR / file_name
        cv2.imwrite(str(output_path), annotated_image)
        return f"{ANNOTATED_IMAGE_URL_PREFIX}/{file_name}"

    def _label_color(self, label: str) -> tuple[int, int, int]:
        normalized_label = label.strip().lower().replace("_", "-")
        if normalized_label in {"no-helmet", "no-safety-vest", "no-vest", "novest", "nohelmet"}:
            return (0, 0, 255)
        if normalized_label in {"helmet", "safety-vest", "vest"}:
            return (0, 180, 0)
        return (255, 140, 0)


yolo_detector = YoloDetector()

