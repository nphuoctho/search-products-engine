import re
import unicodedata

from bs4 import BeautifulSoup

_TEXT_FIELDS = ["name", "web_name", "description", "usage", "dosage", "specification"]


def strip_html(html: str) -> str:
    """Remove HTML tags and scripts."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return soup.get_text(separator=" ", strip=True)


def normalize_unicode(text: str) -> str:
    """Normalize unicode to NFC form."""
    return unicodedata.normalize("NFC", text)


def remove_special_chars(text: str) -> str:
    """Remove special characters, keep only word chars and spaces."""
    return re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)


def normalize_spacing(text: str) -> str:
    """Collapse whitespace and fix punctuation spacing."""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"([,.;:!?])([^\s])", r"\1 \2", text)
    return text.strip()


def normalize_number_token(token: str) -> str:
    """Chuẩn hóa format số, không xóa."""
    token = re.sub(r"(\d)[.,](\d{3})(?!\d)", r"\1\2", token)  # 1.000 / 1,000 → 1000
    return token.lower()


def clean_text(raw_text: str) -> str:
    """Strip HTML, normalize unicode, collapse whitespace."""
    if not raw_text or not raw_text.strip():
        return ""

    text = strip_html(raw_text)
    text = normalize_unicode(text)
    text = remove_special_chars(text)
    text = normalize_spacing(text)
    return text.lower()


def clean_row(row: dict) -> dict:
    """Return dict with cleaned text fields."""
    return {**row, **{field: clean_text(row.get(field, "")) for field in _TEXT_FIELDS}}
