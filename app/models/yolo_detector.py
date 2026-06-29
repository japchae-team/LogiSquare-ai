from pathlib import Path
from tempfile import NamedTemporaryFile

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
        suffix = Path(file.filename or "image.jpg").suffix or ".jpg"

        with NamedTemporaryFile(delete=True, suffix=suffix) as temp_file:
            temp_file.write(contents)
            temp_file.flush()

            model = self._load_model()
            results = model.predict(str(temp_file.name), conf=settings.yolo_confidence, verbose=False)

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

