from pathlib import Path

from unstructured.documents.elements import Element
from unstructured.partition.auto import partition


def parse_document(file_path: str | Path) -> list[Element]:
    return partition(filename=str(file_path), strategy="hi_res")
