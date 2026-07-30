import os
import uuid

import pandas as pd
import psycopg
import requests

EMBEDDINGS_URL = os.environ.get("EMBEDDINGS_URL", "http://embeddings")
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"


def chunks_to_vectors(chunks_df: pd.DataFrame, batch_size: int = 32) -> pd.DataFrame:
    embeddings = []
    texts = chunks_df["text"].tolist()
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        response = requests.post(f"{EMBEDDINGS_URL}/embed", json={"inputs": batch})
        response.raise_for_status()
        embeddings.extend(response.json())

    return pd.DataFrame(
        {
            "id": [uuid.uuid4() for _ in range(len(chunks_df))],
            "chunk_id": chunks_df["id"].to_numpy(),
            "embedding": embeddings,
            "model_name": EMBEDDING_MODEL_NAME,
            "status": "succeeded",
        }
    )


def save_vector_embeddings(
    conn: psycopg.Connection, vectors_df: pd.DataFrame
) -> pd.DataFrame:
    with conn.cursor() as cur:
        for row in vectors_df.itertuples(index=False):
            embedding_literal = "[" + ",".join(map(str, row.embedding)) + "]"
            cur.execute(
                """
                INSERT INTO vector_embeddings
                    (id, chunk_id, embedding, model_name, status)
                VALUES (%s, %s, %s::vector, %s, %s)
                """,
                (
                    row.id,
                    row.chunk_id,
                    embedding_literal,
                    row.model_name,
                    row.status,
                ),
            )
    conn.commit()

    return vectors_df
