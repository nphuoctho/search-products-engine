from pydantic import BaseModel

from app.models.document import SearchResult


class SearchResponse(BaseModel):
    query: str
    total: int
    items: list[SearchResult]
