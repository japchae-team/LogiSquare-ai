import os
from dataclasses import dataclass


def _get_bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str = "LogiSquare AI"
    yolo_model_path: str = os.getenv("YOLO_MODEL_PATH", "models/safety_yolo11.pt")
    yolo_confidence: float = float(os.getenv("YOLO_CONFIDENCE", "0.25"))
    backend_callback_enabled: bool = _get_bool_env("BACKEND_CALLBACK_ENABLED", False)
    backend_base_url: str = os.getenv("BACKEND_BASE_URL", "https://logisquare.p-e.kr").rstrip("/")
    backend_request_timeout: float = float(os.getenv("BACKEND_REQUEST_TIMEOUT", "5.0"))

    @property
    def backend_ai_cctv_event_url(self) -> str:
        if not self.backend_base_url:
            return ""
        return f"{self.backend_base_url}/api/safety/events/ai-cctv"


settings = Settings()

