"""Remove macOS AppleDouble PDF artifacts (e.g. "._file.pdf") from the finance data folder."""

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def main():
    for path in DATA_DIR.rglob("._*.pdf"):
        path.unlink()
        print(f"Removed {path}")


if __name__ == "__main__":
    main()
