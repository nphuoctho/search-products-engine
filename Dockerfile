FROM ghcr.io/astral-sh/uv:0.11.6-python3.12-trixie

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY app ./app
COPY scripts ./scripts
COPY data ./seed-data

EXPOSE 8000

CMD ["sh", "-c", "mkdir -p /app/data/stopwords && if [ ! -f /app/data/products.csv ] && [ -f /app/seed-data/products.csv ]; then cp /app/seed-data/products.csv /app/data/products.csv; fi && if [ ! -f /app/data/stopwords/vietnamese-stopwords.txt ] && [ -f /app/seed-data/stopwords/vietnamese-stopwords.txt ]; then cp /app/seed-data/stopwords/vietnamese-stopwords.txt /app/data/stopwords/vietnamese-stopwords.txt; fi && if [ ! -f /app/data/stopwords/vietnamese-stopwords-dash.txt ] && [ -f /app/seed-data/stopwords/vietnamese-stopwords-dash.txt ]; then cp /app/seed-data/stopwords/vietnamese-stopwords-dash.txt /app/data/stopwords/vietnamese-stopwords-dash.txt; fi && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"]