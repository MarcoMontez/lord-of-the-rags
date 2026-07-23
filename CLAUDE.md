# Project Preferences

## Commits
- Use Conventional Commits format: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, etc.
- Do not add a `Co-Authored-By` trailer.

## Package manager
- Use `uv` for everything: `uv add <pkg>`, `uv sync`, `uv run <script>`. Do not use bare `pip` or `python` to manage deps/run scripts.

## Testing
- Use `pytest` with a `tests/` directory mirroring the source layout.

## Code style
- Format and lint with `ruff` (`ruff format`, `ruff check`).
- Type hints required on function signatures.
- No comments/docstrings unless explaining a non-obvious WHY (hidden constraint, workaround, subtle invariant) — never restate WHAT the code does.
