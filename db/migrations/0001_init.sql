CREATE EXTENSION IF NOT EXISTS vector;

CREATE TYPE ingestion_status AS ENUM ('pending', 'processing', 'succeeded', 'failed');

CREATE TABLE documents (
    id              uuid PRIMARY KEY,
    filename        text NOT NULL,
    file_location   text,
    filetype        text,
    last_modified   timestamptz,
    metadata        jsonb NOT NULL DEFAULT '{}',
    status          ingestion_status NOT NULL DEFAULT 'pending',
    created_at      timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE chunks (
    id            uuid PRIMARY KEY,
    document_id   uuid NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    element_id    text,
    chunk_index   integer NOT NULL,
    type          text NOT NULL,
    text          text NOT NULL,
    page_number   integer,
    metadata      jsonb NOT NULL DEFAULT '{}',
    status        ingestion_status NOT NULL DEFAULT 'pending',
    created_at    timestamptz NOT NULL DEFAULT now(),
    UNIQUE (document_id, chunk_index)
);

CREATE TABLE vector_embeddings (
    id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    chunk_id    uuid NOT NULL REFERENCES chunks(id) ON DELETE CASCADE,
    embedding   vector(384) NOT NULL,
    model_name  text NOT NULL DEFAULT 'BAAI/bge-small-en-v1.5',
    status      ingestion_status NOT NULL DEFAULT 'pending',
    created_at  timestamptz NOT NULL DEFAULT now(),
    UNIQUE (chunk_id, model_name)
);

CREATE TABLE ingestion_logs (
    id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id   uuid REFERENCES documents(id) ON DELETE CASCADE,
    chunk_id      uuid REFERENCES chunks(id) ON DELETE CASCADE,
    embedding_id  uuid REFERENCES vector_embeddings(id) ON DELETE CASCADE,
    stage         text NOT NULL,
    status        ingestion_status NOT NULL,
    error_message text,
    created_at    timestamptz NOT NULL DEFAULT now(),
    CHECK (num_nonnulls(document_id, chunk_id, embedding_id) = 1)
);

CREATE INDEX ON chunks (document_id);
CREATE INDEX ON vector_embeddings (chunk_id);
CREATE INDEX ON vector_embeddings USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON ingestion_logs (document_id);
CREATE INDEX ON ingestion_logs (chunk_id);
CREATE INDEX ON ingestion_logs (embedding_id);
