from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import get_search_engine
from app.core.search_engine import SearchEngine
from app.models.search import ErrorResponse, SearchResponse

router = APIRouter(prefix="/search", tags=["search"])


@router.get(
    "",
    response_model=SearchResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        503: {"model": ErrorResponse, "description": "Search engine unavailable"},
    },
)
def search_products(
    query: str = Query(..., min_length=1),
    top_k: int = Query(10, ge=1, le=100),
    engine: SearchEngine = Depends(get_search_engine),
) -> SearchResponse:
    """Search products and return a consistent object response."""
    try:
        items = engine.search(query=query, top_k=top_k)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Index snapshot not found. Please build index before searching.",
        ) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return SearchResponse(query=query, total=len(items), items=items)
