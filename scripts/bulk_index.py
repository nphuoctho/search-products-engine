import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.search_engine import SearchEngine
from app.data.loader import load_products_csv
from app.storage.disk_store import DiskStore


def main() -> None:
    store = DiskStore("data/index_snapshot.pkl")
    engine = SearchEngine(store=store)

    docs = list(load_products_csv("data/products.csv"))
    print(f"Indexing {len(docs)} products...")

    for doc in docs:
        engine.index_document(doc)

    engine.save()
    print("Done. Snapshot saved to data/index_snapshot.pkl")


if __name__ == "__main__":
    main()
