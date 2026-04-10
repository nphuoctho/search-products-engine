from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Posting:
    doc_id: str
    term_freq: int


class InvertedIndex:
    def __init__(self) -> None:
        self._index: dict[str, list[Posting]] = defaultdict(list)
        self._doc_lengths: dict[str, int] = {}
        self._total_docs: int = 0

    def add_documents(self, doc_id: str, tokens: list[str]) -> None:
        if doc_id in self._doc_lengths:
            raise ValueError(f"doc_id '{doc_id}' already have in index")

        self._doc_lengths[doc_id] = len(tokens)
        self._total_docs += 1

        tf: dict[str, int] = defaultdict(int)
        for token in tokens:
            tf[token] += 1

        for term, freq in tf.items():
            self._index[term].append(Posting(doc_id=doc_id, term_freq=freq))

    def get_postings(self, term: str) -> list[Posting]:
        return self._index.get(term, [])

    def doc_length(self, doc_id: str) -> int:
        return self._doc_lengths.get(doc_id, 0)

    def avg_doc_length(self) -> float:
        if not self._doc_lengths:
            return 0.0
        return sum(self._doc_lengths.values()) / len(self._doc_lengths)

    def total_docs(self) -> int:
        return self._total_docs

    def doc_freq(self, term: str) -> int:
        return len(self._index.get(term, []))
