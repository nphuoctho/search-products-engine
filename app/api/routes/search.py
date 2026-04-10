from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.deps import get_search_engine
from app.core.search_engine import SearchEngine
from app.models.search import SearchResponse

router = APIRouter(tags=["search"])


@router.get("/search", response_model=SearchResponse)
def search_products(
    query: str = Query(..., min_length=1),
    top_k: int = Query(10, ge=1, le=100),
    engine: SearchEngine = Depends(get_search_engine),
) -> SearchResponse:
    """Search products and return a consistent object response."""
    try:
        items = engine.search(query=query, top_k=top_k)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Search failed due to an internal error.",
        ) from exc

    return SearchResponse(query=query, total=len(items), items=items)
