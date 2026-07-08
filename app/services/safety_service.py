from fastapi import HTTPException, UploadFile, status

from app.models.yolo_detector import yolo_detector
from app.schemas.safety import DetectionItem, DetectionResponse, DetectionSummary


PERSON_LABELS = {"person"}
HELMET_LABELS = {"helmet", "hardhat", "hard-hat", "safety-helmet"}
NO_HELMET_LABELS = {"no-helmet", "nohelmet", "no-hardhat", "no-hard-hat"}
VEST_LABELS = {"vest", "safety-vest", "reflective-vest"}
NO_VEST_LABELS = {"no-vest", "novest", "no-safety-vest", "no-reflective-vest"}
SHOES_LABELS = {"shoes", "shoe", "boots", "boot", "safety-shoes", "safety-boots"}


class SafetyService:
    async def detect(self, file: UploadFile) -> DetectionResponse:
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image file is required",
            )

        try:
            detection_result = await yolo_detector.detect(file)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc

        detections = detection_result.detections
        helmet_worn = self._is_equipment_worn(detections, HELMET_LABELS, NO_HELMET_LABELS)
        vest_worn = self._is_equipment_worn(detections, VEST_LABELS, NO_VEST_LABELS)
        event_type = self._build_event_type(detections, helmet_worn, vest_worn)
        confidence_score = max((detection.confidence for detection in detections), default=0.0)

        return DetectionResponse(
            source_type="CCTV",
            event_type=event_type,
            confidence_score=confidence_score,
            helmet_worn=helmet_worn,
            vest_worn=vest_worn,
            annotated_image_url=detection_result.annotated_image_url,
            detections=[
                DetectionSummary(label=detection.label, confidence=detection.confidence)
                for detection in detections
            ],
            count=len(detections),
        )

    def _has_label(self, detections: list[DetectionItem], labels: set[str]) -> bool:
        return any(self._normalize_label(detection.label) in labels for detection in detections)

    def _is_equipment_worn(
        self,
        detections: list[DetectionItem],
        worn_labels: set[str],
        not_worn_labels: set[str],
    ) -> bool | None:
        if self._has_label(detections, not_worn_labels):
            return False
        if self._has_label(detections, worn_labels):
            return True
        return None

    def _build_event_type(
        self,
        detections: list[DetectionItem],
        helmet_worn: bool | None,
        vest_worn: bool | None,
    ) -> str:
        has_person_or_equipment = any(
            self._normalize_label(detection.label)
            in PERSON_LABELS | HELMET_LABELS | NO_HELMET_LABELS | VEST_LABELS | NO_VEST_LABELS
            for detection in detections
        )
        if not has_person_or_equipment:
            return "PPE_NOT_DETECTED"

        violation_events = []
        if helmet_worn is False:
            violation_events.append("NO_HELMET")
        if vest_worn is False:
            violation_events.append("NO_SAFETY_VEST")

        if len(violation_events) > 1:
            return "MULTIPLE_SAFETY_VIOLATIONS"
        if len(violation_events) == 1:
            return violation_events[0]

        not_detected_events = []
        if helmet_worn is None:
            not_detected_events.append("HELMET_NOT_DETECTED")
        if vest_worn is None:
            not_detected_events.append("SAFETY_VEST_NOT_DETECTED")

        if len(not_detected_events) > 1:
            return "PPE_NOT_DETECTED"
        if len(not_detected_events) == 1:
            return not_detected_events[0]

        return "NORMAL"

    def _normalize_label(self, label: str) -> str:
        return label.strip().lower().replace("_", "-")


safety_service = SafetyService()

