from pathlib import Path

from unstructured.documents.elements import Element
from unstructured.partition.auto import partition


def parse_document(file_path: str | Path , strategy="hi_res", infer_table_structure=True)-> list[Element]:
    return partition(filename=str(file_path), 
                     strategy=strategy,
                     infer_table_structure=infer_table_structure)
