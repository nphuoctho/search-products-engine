FROM ghcr.io/astral-sh/uv:0.11.6-python3.12-trixie AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
	uv sync --frozen --no-dev --no-install-project

FROM python:3.12-slim-trixie AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	INDEX_SOURCE_PATH=data/products.csv \
	INDEX_SNAPSHOT_PATH=/app/persistent/index_snapshot.pkl \
	PATH="/app/.venv/bin:$PATH"

RUN groupadd --system --gid 10001 app \
	&& useradd --system --uid 10001 --gid app --no-create-home \
	--home /nonexistent --shell /usr/sbin/nologin app

RUN mkdir -p /app/persistent \
	&& chown -R app:app /app/persistent

COPY --from=builder /app/.venv /app/.venv
COPY --chown=app:app app ./appj
COPY --chown=app:app scripts ./scripts
COPY --chown=app:app data ./data

EXPOSE 8000

USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
