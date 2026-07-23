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

The dev environment (Ubuntu 26.04, `tesseract-ocr`/`poppler-utils` for `unstructured` hi_res parsing, project deps via `uv`) runs in Docker so you don't need those system packages installed on the host.

```
docker compose up --build -d
```

Then open http://localhost:8888 for Jupyter Lab (no login token). The repo is bind-mounted at `/workspace` in the container, so edits on the host are reflected live.

To get a shell into the running container (e.g. to run scripts, `uv add` a package, or poke around) without stopping Jupyter:

```
docker compose exec ingestion bash
```

