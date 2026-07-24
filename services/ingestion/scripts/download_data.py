"""Download the finance PDF archive and QA parquet file from Salesforce/UniDoc-Bench."""

import shutil
import tarfile
from pathlib import Path

from huggingface_hub import hf_hub_download

REPO_ID = "Salesforce/UniDoc-Bench"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def download_pdfs():
    filename = "finance_pdfs.tar.gz"
    output_dir = DATA_DIR / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)

    archive_path = hf_hub_download(repo_id=REPO_ID, repo_type="dataset", filename=filename)

    with tarfile.open(archive_path) as tar:
        tar.extractall(output_dir)

    print(f"Extracted {filename} to {output_dir}")


def download_parquet():
    filename = "data/finance-00000-of-00001.parquet"
    output_dir = DATA_DIR / "test"
    output_dir.mkdir(parents=True, exist_ok=True)

    parquet_path = hf_hub_download(repo_id=REPO_ID, repo_type="dataset", filename=filename)
    shutil.copy(parquet_path, output_dir / Path(filename).name)

    print(f"Copied {filename} to {output_dir}")


def main():
    download_pdfs()
    download_parquet()


if __name__ == "__main__":
    main()
