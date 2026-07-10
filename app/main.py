from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.router import api_router
from app.core.config import settings
from app.schemas.common import ApiResponse, ErrorResponse

app = FastAPI(title=settings.app_name)

settings.upload_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

app.include_router(api_router, prefix="/api/v1")


def error_response(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(ApiResponse(success=False, data=None, message=message)),
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    message = exc.detail if isinstance(exc.detail, str) else "Request failed"
    return error_response(exc.status_code, message)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return error_response(status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid request")


@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")


@app.get(
    "/health",
    response_model=ApiResponse[dict],
    responses={500: {"model": ErrorResponse, "description": "Internal server error"}},
)
def health_check() -> ApiResponse[dict]:
    return ApiResponse(success=True, data={"status": "ok"}, message="AI server is running")

