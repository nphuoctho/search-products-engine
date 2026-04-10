# Search Engine Baseline

Lightweight Vietnamese product search engine using:
- Inverted Index
- BM25 ranking
- FastAPI endpoints for indexing and search

## Project Structure

```text
search-engine-baseline/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── deps.py
│   │   └── routes/
│   │       ├── index.py
│   │       └── search.py
│   ├── core/
│   │   ├── bm25.py
│   │   ├── inverted_index.py
│   │   ├── preprocessor.py
│   │   └── search_engine.py
│   ├── data/
│   │   ├── cleaner.py
│   │   ├── loader.py
│   │   └── schema_mapper.py
│   ├── models/
│   │   ├── document.py
│   │   ├── index.py
│   │   └── search.py
│   └── storage/
│       ├── base.py
│       ├── disk_store.py
│       └── memory_store.py
├── data/
│   ├── products.csv
│   ├── index_snapshot.pkl
│   └── stopwords/
├── scripts/
│   └── bulk_index.py
├── pyproject.toml
└── README.md
```

## Install

```bash
uv sync
```

## Run API

```bash
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Open:
- Swagger: `http://127.0.0.1:8000/docs`
- Root: `http://127.0.0.1:8000/`

## API Endpoints

### 1) Rebuild index

`POST /index`

Rebuilds inverted index from source CSV and saves snapshot.

Example response:

```json
{
	"indexed_docs": 7631,
	"snapshot": "data/index_snapshot.pkl"
}
```

### 2) Search products

`GET /search?query=<text>&top_k=10`

Example response:

```json
{
	"query": "băng vệ sinh",
	"total": 10,
	"items": [
		{
			"id": "123",
			"score": 5.1821,
			"name": "Băng vệ sinh ...",
			"price": "32000",
			"thumbnail_url": "...",
			"specification": "...",
			"dosage_form": "...",
			"country_of_manufacture": "..."
		}
	]
}
```

## Configuration

Centralized in `app/config.py`:
- `INDEX_SOURCE_PATH` (default: `data/products.csv`)
- `INDEX_SNAPSHOT_PATH` (default: `data/index_snapshot.pkl`)

Set environment variables before running app:

```bash
export INDEX_SOURCE_PATH="data/products.csv"
export INDEX_SNAPSHOT_PATH="data/index_snapshot.pkl"
uv run uvicorn app.main:app --reload
```

## Optional CLI Indexing

You can still build snapshot via script:

```bash
uv run python scripts/bulk_index.py
```
