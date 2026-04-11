import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import get_settings
from app.core.search_engine import SearchEngine
from app.data.loader import load_products_csv
from app.storage.disk_store import DiskStore


def main() -> None:
    settings = get_settings()
    store = DiskStore(settings.index_snapshot_path)
    engine = SearchEngine(store=store)

    docs = list(load_products_csv(settings.index_source_path))
    print(f"Indexing {len(docs)} products...")

    for doc in docs:
        engine.index_document(doc)

    engine.save()
    print(f"Done. Snapshot saved to {settings.index_snapshot_path}")


if __name__ == "__main__":
    main()
