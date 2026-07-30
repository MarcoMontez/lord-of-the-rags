# lord-of-the-rags
The one Rag to Chunk them all

# Setup up

# Architecture


# Choices
Dataset
Claude Code
Draw.io and Mermaid
PostGres with Vector
Qwen3 + Ollama for query rewriting

# Development

Each service lives in its own folder under `services/`, with its own `Dockerfile`, `pyproject.toml`, and `uv.lock` — dependencies don't leak between services:

- `services/ingestion/` — document parsing (Ubuntu 26.04, `tesseract-ocr`/`poppler-utils` for `unstructured` hi_res parsing)
- `services/retrieval/` — RAG retrieval (scaffolded, no logic yet)

There's also a `db` service (`pgvector/pgvector:pg17`) providing Postgres with the `pgvector` extension, with data persisted in the `pgdata` volume. Its credentials/port come from `.env` (copy `.env.example` to `.env` to get started).

An `embeddings` service (`text-embeddings-inference`) serves `BAAI/bge-small-en-v1.5` on port 8080, and a `query-rewriter` service serves `qwen3:1.7b-q8_0` (Q8_0 GGUF) via Ollama on port 11434 for rewriting RAG queries. Unlike every other service, `query-rewriter` requires an NVIDIA GPU with the `nvidia` container runtime installed on the host — it reserves the GPU via `docker-compose.yml`'s `deploy.resources.reservations.devices`.

Both `ingestion` and `retrieval` run in Docker so you don't need any of those system packages installed on the host.

```
cp .env.example .env
docker compose up --build
```

Then open http://localhost:8888 for ingestion's Jupyter Lab, and http://localhost:8889 for retrieval's (no login token on either). Each service's folder is bind-mounted at `/workspace` in its container, so edits on the host are reflected live.

To get a shell into a running container (e.g. to run scripts, `uv add` a package, or poke around) without stopping Jupyter:

```
docker compose exec ingestion bash
docker compose exec retrieval bash
```

