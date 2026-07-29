# lord-of-the-rags
The one Rag to Chunk them all

# Setup up

# Architecture


# Choices
Dataset
Claude Code
Draw.io and Mermaid
PostGres with Vector

# Development

Each service lives in its own folder under `services/`, with its own `Dockerfile`, `pyproject.toml`, and `uv.lock` — dependencies don't leak between services:

- `services/ingestion/` — document parsing (Ubuntu 26.04, `tesseract-ocr`/`poppler-utils` for `unstructured` hi_res parsing)
- `services/retrieval/` — RAG retrieval (scaffolded, no logic yet)

Both run in Docker so you don't need any of those system packages installed on the host.

```
docker compose up --build
```

Then open http://localhost:8888 for ingestion's Jupyter Lab, and http://localhost:8889 for retrieval's (no login token on either). Each service's folder is bind-mounted at `/workspace` in its container, so edits on the host are reflected live.

To get a shell into a running container (e.g. to run scripts, `uv add` a package, or poke around) without stopping Jupyter:

```
docker compose exec ingestion bash
docker compose exec retrieval bash
```

