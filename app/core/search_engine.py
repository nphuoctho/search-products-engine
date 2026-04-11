from collections.abc import Iterable

from app.core.bm25 import BM25Scorer
from app.core.inverted_index import InvertedIndex
from app.core.preprocessor import tokenize
from app.models.document import Document, SearchResult
from app.storage.base import BaseStore
from app.storage.disk_store import DiskStore


class SearchEngine:
    def __init__(
        self, store: BaseStore | None, k1: float = 1.5, b: float = 0.75
    ) -> None:
        self._store = store or DiskStore()
        self.k1 = k1
        self.b = b
        self._index: InvertedIndex
        self._metadata: dict[str, dict]
        self._scorer: BM25Scorer
        self._load_or_init()

    def _load_or_init(self) -> None:
        """Load existing snapshot or initialize empty index structures."""
        result = self._store.load()
        if result is not None:
            self._index, self._metadata = result
        else:
            self._index = InvertedIndex()
            self._metadata = {}
        self._scorer = BM25Scorer(self._index, k1=self.k1, b=self.b)

    def _reset_index(self) -> None:
        """Reset in-memory index and metadata for a full rebuild."""
        self._index = InvertedIndex()
        self._metadata = {}
        self._scorer = BM25Scorer(self._index, k1=self.k1, b=self.b)

    def index_document(self, doc: Document) -> None:
        tokens = tokenize(doc.index_text)
        if not tokens:
            return
        self._index.add_documents(doc.id, tokens)
        self._metadata[doc.id] = doc.metadata

    def save(self) -> None:
        """Persist current in-memory index state to the configured store."""
        self._store.save(self._index, self._metadata)

    def rebuild_index(self, docs: Iterable[Document]) -> int:
        """Rebuild index from scratch and return number of indexed documents."""
        self._reset_index()

        indexed_count = 0
        for doc in docs:
            self.index_document(doc)
            if doc.id in self._metadata:
                indexed_count += 1

        return indexed_count

    def search(self, query: str, top_k: int = 10) -> list[SearchResult]:
        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        ranked = self._scorer.search(query_tokens, top_k=top_k)
        results: list[SearchResult] = []
        for doc_id, score in ranked:
            meta = self._metadata.get(doc_id, {})
            results.append(
                SearchResult(
                    id=doc_id,
                    score=round(score, 4),
                    name=meta.get("name", ""),
                    price=meta.get("price", ""),
                    sku=meta.get("sku", ""),
                    thumbnail_url=meta.get("thumbnail_url", ""),
                    specification=meta.get("specification", ""),
                    dosage_form=meta.get("dosage_form", ""),
                    country_of_manufacture=meta.get("country_of_manufacture", ""),
                )
            )

        return results
