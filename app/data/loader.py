from collections.abc import Iterator
from pathlib import Path

import pandas as pd

from app.data.cleaner import clean_row
from app.data.schema_mapper import map_row_to_document
from app.models.document import Document


def load_products_csv(path: str | Path) -> Iterator[Document]:
    df = pd.read_csv(path, dtype=str).fillna("")
    columns = list(df.columns)

    for row_values in df.itertuples(index=False, name=None):
        raw_row = dict(zip(columns, row_values))
        cleaned_row = clean_row(raw_row)

        doc = map_row_to_document(cleaned_row)
        # Keep display name unchanged in API responses while indexing cleaned text.
        doc.metadata["name"] = raw_row.get("web_name", raw_row.get("name", ""))

        yield doc
