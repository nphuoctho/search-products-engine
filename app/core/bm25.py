import math

from app.core.inverted_index import InvertedIndex


class BM25Scorer:
    def __init__(self, index: InvertedIndex, k1: float = 1.5, b: float = 0.75) -> None:
        self._index = index
        self.k1 = k1
        self.b = b

    def _idf(self, term: str) -> float:
        N = self._index.total_docs()
        df = self._index.doc_freq(term)
        if df == 0:
            return 0.0
        return math.log((N - df + 0.5) / (df + 0.5) + 1)

    def _tf_norm(self, term_freq: int, doc_id: str) -> float:
        dl = self._index.doc_length(doc_id)  # doc length
        avgdl = self._index.avg_doc_length()  # average doc length
        k1, b = self.k1, self.b

        numerator = term_freq * (k1 + 1)
        denominator = term_freq + k1 * (1 - b + b * (dl / avgdl) if avgdl > 0 else 1)
        return numerator / denominator

    def score(self, query_tokens: list[str], doc_id: str) -> float:
        """Score một doc cụ thể với query đã tokenize."""
        total: float = 0.0
        for term in query_tokens:
            postings = self._index.get_postings(term)
            tf = next((p.term_freq for p in postings if p.doc_id == doc_id), 0)
            if tf == 0:
                continue
            total += self._idf(term) * self._tf_norm(tf, doc_id)
        return total

    def search(
        self, query_tokens: list[str], top_k: int = 10
    ) -> list[tuple[str, float]]:
        """
        Trả về list (doc_id, score) đã sort descending, độ dài top_k.
        Chỉ score các doc có chứa ít nhất 1 query term — bỏ qua doc không liên quan.
        """
        if not query_tokens:
            return []

        # Gom candidate doc_ids từ posting lists — tránh score toàn bộ corpus
        candidate_ids: set[str] = set()
        for term in query_tokens:
            for posting in self._index.get_postings(term):
                candidate_ids.add(posting.doc_id)
        if not candidate_ids:
            return []
        scores = {doc_id: self.score(query_tokens, doc_id) for doc_id in candidate_ids}

        # heapq.nlargest: O(n log k) thay vì O(n log n) của sorted()
        import heapq

        return heapq.nlargest(top_k, scores.items(), key=lambda x: x[1])
