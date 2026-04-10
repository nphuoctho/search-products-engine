from functools import lru_cache

from app.config import get_settings
from app.core.search_engine import SearchEngine
from app.storage.disk_store import DiskStore


@lru_cache(maxsize=1)
def get_search_engine() -> SearchEngine:
    """Create one shared search engine instance backed by disk snapshot."""
    settings = get_settings()
    store = DiskStore(settings.index_snapshot_path)
    return SearchEngine(store=store)


def clear_search_engine_cache() -> None:
    """Invalidate cached engine so next request reloads latest snapshot."""
    get_search_engine.cache_clear()
