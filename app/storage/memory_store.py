from app.core.inverted_index import InvertedIndex
from app.storage.base import BaseStore


class MemoryStore(BaseStore):
    def __init__(self) -> None:
        self._index: InvertedIndex | None = None
        self._metadata: dict[str, dict] | None = None

    def save(self, index: InvertedIndex, metadata: dict[str, dict]) -> None:
        self._index = index
        self._metadata = metadata

    def load(self) -> tuple[InvertedIndex, dict[str, dict] | None] | None:
        if self._index is None:
            return None
        return self._index, self._metadata

    def exists(self) -> bool:
        return self._index is not None
