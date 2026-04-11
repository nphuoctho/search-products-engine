import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes.search import router as search_router
from app.config import get_settings
from app.models.search import ErrorResponse

settings = get_settings()

app = FastAPI(title="Search Engine API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)
app.include_router(search_router, prefix=settings.api_prefix)


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    message = exc.detail if isinstance(exc.detail, str) else "Request failed."
    payload = ErrorResponse(error="http_error", message=message, path=request.url.path)
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


@app.exception_handler(RequestValidationError)
def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    details = [err.get("msg", "Invalid value") for err in exc.errors()]
    payload = ErrorResponse(
        error="validation_error",
        message="Invalid request parameters.",
        path=request.url.path,
        details=details,
    )
    return JSONResponse(status_code=422, content=payload.model_dump())


@app.exception_handler(Exception)
def generic_exception_handler(request: Request, _: Exception) -> JSONResponse:
    payload = ErrorResponse(
        error="internal_server_error",
        message="Unexpected server error.",
        path=request.url.path,
    )
    return JSONResponse(status_code=500, content=payload.model_dump())


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {
        "message": "Search API is running. Open /docs for API docs.",
        "search_endpoint": f"{settings.api_prefix}/search",
    }


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
