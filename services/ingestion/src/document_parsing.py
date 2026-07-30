import hashlib
import uuid
from datetime import datetime
from pathlib import Path

import pandas as pd
import psycopg
from psycopg.types.json import Jsonb
from unstructured.documents.elements import Element
from unstructured.partition.auto import partition
from unstructured.staging.base import elements_to_json


def file_path_to_uuid(file_path: str | Path) -> uuid.UUID:
    digest = hashlib.sha256(Path(file_path).read_bytes()).digest()
    return uuid.UUID(bytes=digest[:16], version=5)


def parse_document(
    file_path: str | Path, strategy="hi_res", infer_table_structure=True
) -> list[Element]:
    return partition(
        filename=str(file_path),
        strategy=strategy,
        infer_table_structure=infer_table_structure,
    )


def save_parsed_elements_local(
    folder_path: str | Path, elements: list[list[Element]]
) -> None:
    folder_path = Path(folder_path)
    folder_path.mkdir(parents=True, exist_ok=True)
    for document_elements in elements:
        filename = Path(document_elements[0].metadata.filename).stem
        elements_to_json(
            document_elements, filename=str(folder_path / f"{filename}.json")
        )


def elements_to_dataframe(elements: list[list[Element]]) -> pd.DataFrame:
    rows = []
    for document_elements in elements:
        metadata = document_elements[0].to_dict()["metadata"]
        file_location = (
            str(Path(metadata["file_directory"]) / metadata["filename"])
            if metadata.get("file_directory")
            else metadata["filename"]
        )
        last_modified = (
            datetime.fromisoformat(metadata["last_modified"])
            if metadata.get("last_modified")
            else None
        )
        rows.append(
            {
                "id": file_path_to_uuid(file_location),
                "filename": metadata["filename"],
                "file_location": file_location,
                "filetype": metadata.get("filetype"),
                "last_modified": last_modified,
                "metadata": {
                    "languages": metadata.get("languages"),
                    "element_count": len(document_elements),
                },
                "status": "succeeded",
            }
        )

    return pd.DataFrame(rows)


def save_parsed_elements(
    conn: psycopg.Connection, elements: list[list[Element]]
) -> pd.DataFrame:
    df = elements_to_dataframe(elements)

    with conn.cursor() as cur:
        for row in df.itertuples(index=False):
            cur.execute(
                """
                INSERT INTO documents
                    (id, filename, file_location, filetype, last_modified, metadata, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    row.id,
                    row.filename,
                    row.file_location,
                    row.filetype,
                    row.last_modified,
                    Jsonb(row.metadata),
                    row.status,
                ),
            )
    conn.commit()

    return df


def chunks_to_dataframe(chunks: list[list[Element]]) -> pd.DataFrame:
    rows = []
    for document_chunks in chunks:
        metadata = document_chunks[0].to_dict()["metadata"]
        file_location = (
            str(Path(metadata["file_directory"]) / metadata["filename"])
            if metadata.get("file_directory")
            else metadata["filename"]
        )
        document_id = file_path_to_uuid(file_location)

        for chunk_index, chunk in enumerate(document_chunks):
            chunk_dict = chunk.to_dict()
            chunk_metadata = chunk_dict["metadata"]
            element_id = chunk_dict["element_id"]
            try:
                chunk_id = uuid.UUID(hex=element_id)
            except ValueError:
                chunk_id = uuid.uuid4()

            rows.append(
                {
                    "id": chunk_id,
                    "document_id": document_id,
                    "element_id": element_id,
                    "chunk_index": chunk_index,
                    "type": chunk_dict["type"],
                    "text": chunk_dict["text"],
                    "page_number": chunk_metadata.get("page_number"),
                    "metadata": {
                        "languages": chunk_metadata.get("languages"),
                    },
                    "status": "succeeded",
                }
            )

    return pd.DataFrame(rows)


def save_chunks(conn: psycopg.Connection, chunks: list[list[Element]]) -> pd.DataFrame:
    df = chunks_to_dataframe(chunks)

    with conn.cursor() as cur:
        for row in df.itertuples(index=False):
            cur.execute(
                """
                INSERT INTO chunks
                    (id, document_id, element_id, chunk_index, type, text, page_number, metadata, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    row.id,
                    row.document_id,
                    row.element_id,
                    row.chunk_index,
                    row.type,
                    row.text,
                    row.page_number,
                    Jsonb(row.metadata),
                    row.status,
                ),
            )
    conn.commit()

    return df
