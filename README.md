# python-rag-api

This repository contains a Python implementation of a Retrieval-Augmented Generation (RAG) API.

## Run Locally

1. Run docker compose: `docker compose up -d`
2. Run migrations: `alembic upgrade head`
3. Start the FastAPI server: `fastapi dev src/pdf_analyzer/main.py`

## Fix Code Style

```bash
ruff check src --fix
```