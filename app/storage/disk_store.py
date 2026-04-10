import pickle
from pathlib import Path

from app.core.inverted_index import InvertedIndex
from app.storage.base import BaseStore


class DiskStore(BaseStore):
    """
    Persist index + metadata ra file .pkl.
    Dùng pickle vì InvertedIndex chứa defaultdict và dataclass —
    JSON không serialize được trực tiếp.
    """

    def __init__(self, path: str | Path = "data/index_snapshot.pkl") -> None:
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, index: InvertedIndex, metadata: dict[str, dict]) -> None:
        payload = {"index": index, "metadata": metadata}
        with self._path.open("wb") as f:
            pickle.dump(payload, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self) -> tuple[InvertedIndex, dict[str, dict]] | None:
        if not self.exists():
            return None
        with self._path.open("rb") as f:
            payload = pickle.load(f)
        return payload["index"], payload["metadata"]

    def exists(self) -> bool:
        return self._path.exists()
