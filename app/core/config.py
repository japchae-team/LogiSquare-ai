import os
from dataclasses import dataclass
from pathlib import Path


def _get_bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str = "LogiSquare AI"
    ai_server_base_url: str = os.getenv("AI_SERVER_BASE_URL", "http://165.246.170.53:8000").rstrip("/")
    yolo_model_path: str = os.getenv("YOLO_MODEL_PATH", "models/ppe-helmet-vest-best.pt")
    yolo_confidence: float = float(os.getenv("YOLO_CONFIDENCE", "0.25"))
    backend_callback_enabled: bool = _get_bool_env("BACKEND_CALLBACK_ENABLED", False)
    backend_base_url: str = os.getenv("BACKEND_BASE_URL", "https://logisquare.p-e.kr").rstrip("/")
    backend_request_timeout: float = float(os.getenv("BACKEND_REQUEST_TIMEOUT", "15.0"))

    @property
    def upload_dir(self) -> Path:
        return Path(__file__).resolve().parents[2] / "uploads"

    @property
    def backend_ai_cctv_event_url(self) -> str:
        if not self.backend_base_url:
            return ""
        return f"{self.backend_base_url}/api/safety/events/ai-cctv"


settings = Settings()

