from pydantic import BaseModel, Field

from app.models.document import SearchResult


class SearchResponse(BaseModel):
    query: str
    total: int
    items: list[SearchResult]


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Machine-readable error type")
    message: str = Field(..., description="Human-readable error message")
    path: str = Field(..., description="Request path that produced the error")
    details: list[str] | None = Field(
        default=None, description="Optional validation details"
    )
