from fastapi import APIRouter, HTTPException

from app.api.deps import clear_search_engine_cache
from app.config import get_settings
from app.core.search_engine import SearchEngine
from app.data.loader import load_products_csv
from app.models.index import IndexResponse
from app.storage.disk_store import DiskStore

router = APIRouter(tags=["index"])


@router.post("/index", response_model=IndexResponse)
def rebuild_index() -> IndexResponse:
    """Rebuild inverted index from CSV and persist to snapshot file."""
    try:
        settings = get_settings()
        docs = load_products_csv(settings.index_source_path)
        engine = SearchEngine(store=DiskStore(settings.index_snapshot_path))
        indexed_docs = engine.rebuild_index(docs)
        engine.save()
        clear_search_engine_cache()

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Index build failed due to an internal error.",
        ) from exc

    return IndexResponse(
        indexed_docs=indexed_docs, snapshot=settings.index_snapshot_path
    )
