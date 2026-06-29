from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.schemas.common import ApiResponse

app = FastAPI(title=settings.app_name)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health", response_model=ApiResponse[dict])
def health_check() -> ApiResponse[dict]:
    return ApiResponse(success=True, data={"status": "ok"}, message="AI server is running")

