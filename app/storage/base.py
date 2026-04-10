from abc import ABC, abstractmethod

from app.core.inverted_index import InvertedIndex


class BaseStore(ABC):
    @abstractmethod
    def save(self, index: InvertedIndex, metadata: dict[str, dict]) -> None: ...

    @abstractmethod
    def load(self) -> tuple[InvertedIndex, dict[str, dict]] | None:
        """None nếu chưa có snapshot."""
        ...

    @abstractmethod
    def exists(self) -> bool: ...
