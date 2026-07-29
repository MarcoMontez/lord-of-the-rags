from pathlib import Path

from unstructured.documents.elements import Element
from unstructured.partition.auto import partition
from unstructured.staging.base import elements_to_json


def parse_document(
    file_path: str | Path, strategy="hi_res", infer_table_structure=True
) -> list[Element]:
    return partition(
        filename=str(file_path),
        strategy=strategy,
        infer_table_structure=infer_table_structure,
    )


def save_parsed_elements(
    folder_path: str | Path, elements: list[list[Element]]
) -> None:
    folder_path = Path(folder_path)
    folder_path.mkdir(parents=True, exist_ok=True)
    for document_elements in elements:
        filename = Path(document_elements[0].metadata.filename).stem
        elements_to_json(
            document_elements, filename=str(folder_path / f"{filename}.json")
        )
