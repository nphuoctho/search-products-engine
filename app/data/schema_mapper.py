from app.models.document import Document

# Fields được đưa vào BM25 — thứ tự ảnh hưởng đến context
_INDEXED_FIELDS = ["name", "web_name", "usage"]

# Fields chỉ lưu để trả về trong SearchResult
_STORED_FIELDS = [
    "sku",
    "price",
    "thumbnail_url",
    "specification",
    "dosage_form",
    "country_of_manufacture",
]


def map_row_to_document(row: dict) -> Document:
    index_text = " ".join(row[f] for f in _INDEXED_FIELDS if row.get(f))

    metadata = {f: row.get(f, "") for f in _STORED_FIELDS}

    return Document(id=row["id"], index_text=index_text, metadata=metadata)
