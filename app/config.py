import os
from functools import lru_cache

from pydantic import BaseModel


def _parse_csv_env(value: str, default: list[str]) -> list[str]:
    """Parse comma-separated env var into a clean list."""
    if not value.strip():
        return default
    items = [item.strip() for item in value.split(",") if item.strip()]
    return items or default


def _parse_bool_env(value: str, default: bool) -> bool:
    """Parse common string booleans from env vars."""
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default


class Settings(BaseModel):
    index_source_path: str = "data/products.csv"
    index_snapshot_path: str = "data/index_snapshot.pkl"
    api_prefix: str = "/api/v1"
    cors_allow_origins: list[str] = ["*"]
    cors_allow_methods: list[str] = ["GET"]
    cors_allow_headers: list[str] = ["*"]
    cors_allow_credentials: bool = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings from environment with defaults."""
    return Settings(
        index_source_path=os.getenv("INDEX_SOURCE_PATH", "data/products.csv"),
        index_snapshot_path=os.getenv("INDEX_SNAPSHOT_PATH", "data/index_snapshot.pkl"),
        api_prefix=os.getenv("API_PREFIX", "/api/v1"),
        cors_allow_origins=_parse_csv_env(
            os.getenv("CORS_ALLOW_ORIGINS", "*"), ["*"]
        ),
        cors_allow_methods=_parse_csv_env(
            os.getenv("CORS_ALLOW_METHODS", "GET"), ["GET"]
        ),
        cors_allow_headers=_parse_csv_env(
            os.getenv("CORS_ALLOW_HEADERS", "*"), ["*"]
        ),
        cors_allow_credentials=_parse_bool_env(
            os.getenv("CORS_ALLOW_CREDENTIALS", "false"), False
        ),
    )
