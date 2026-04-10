import re
from functools import lru_cache
from pathlib import Path

from underthesea import word_tokenize

from app.data.cleaner import normalize_number_token, normalize_unicode


@lru_cache(maxsize=1)
def _load_stopwords() -> frozenset[str]:
    """Load and cache Vietnamese stopwords from the repository data folder."""
    stopwords_path = Path("data/stopwords/vietnamese-stopwords.txt")

    stopwords = {
        line.strip().lower()
        for line in stopwords_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    }

    return frozenset(stopwords)


def is_valid_token(token: str) -> bool:
    """Check if a token is valid for indexing.

    A token is valid if it has at least 2 characters and contains at least one word character.
    """
    return len(token) >= 2 and bool(re.search(r"\w", token, re.UNICODE))


def tokenize(text: str) -> list[str]:
    if not text:
        return []
    text = normalize_unicode(text)

    stopwords = _load_stopwords()

    tokenized = word_tokenize(text.lower(), format="text")
    raw_tokens = tokenized.split() if isinstance(tokenized, str) else list(tokenized)

    result = []
    for token in raw_tokens:
        token = normalize_number_token(token)
        if is_valid_token(token) and token not in stopwords:
            result.append(token)

    return result
