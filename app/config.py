import os
from functools import lru_cache

from pydantic import BaseModel


class Settings(BaseModel):
    index_source_path: str = "data/products.csv"
    index_snapshot_path: str = "data/index_snapshot.pkl"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings from environment with defaults."""
    return Settings(
        index_source_path=os.getenv("INDEX_SOURCE_PATH", "data/products.csv"),
        index_snapshot_path=os.getenv("INDEX_SNAPSHOT_PATH", "data/index_snapshot.pkl"),
    )
