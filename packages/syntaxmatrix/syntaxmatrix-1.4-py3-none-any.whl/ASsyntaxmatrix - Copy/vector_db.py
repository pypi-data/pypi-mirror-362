import sqlite3
import uuid
import json
import numpy as np
from typing import List, Optional, Union

from .db import DB_PATH

def _init_embeddings_table():
    """
    Create the embeddings table with an extra column for chunk_text.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS embeddings (
            id TEXT PRIMARY KEY,
            vector BLOB NOT NULL,
            metadata TEXT,
            chunk_text TEXT
        )
        """
    )
    conn.commit()
    conn.close()

# Initialize on import
_init_embeddings_table()


def insert_embedding(
    vector: Union[List[float], np.ndarray],
    id: Optional[str] = None,
    metadata: Optional[dict] = None,
    chunk_text: Optional[str] = None
) -> str:
    """
    Serialize and insert an embedding vector with optional metadata.
    Returns the assigned record id.
    """
    # Ensure numpy array
    arr = np.array(vector, dtype=np.float32)
    blob = arr.tobytes()

    rec_id = id or str(uuid.uuid4())
    meta_json = json.dumps(metadata) if metadata is not None else None

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO embeddings (id, vector, metadata, chunk_text) VALUES (?, ?, ?, ?)",
        (rec_id, blob, meta_json, chunk_text)
    )
    conn.commit()
    conn.close()

    return rec_id


def query_embeddings(
    query_vector: Union[List[float], np.ndarray],
    top_k: int = 5
) -> List[dict]:
    """
    Retrieve the top_k most similar embeddings (cosine similarity) to the query_vector.
    Returns a list of dicts: {'id', 'score', 'metadata'}.
    """
    # Normalize query
    q_arr = np.array(query_vector, dtype=np.float32)
    q_norm = np.linalg.norm(q_arr)
    if q_norm == 0:
        raise ValueError("Query was not detected!")
    q_arr = q_arr / q_norm

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, vector, metadata, chunk_text FROM embeddings")
    rows = cursor.fetchall()
    conn.close()

    results = []
    for rec_id, blob, meta_json, chunk_text in rows:
        stored = np.frombuffer(blob, dtype=np.float32)
        norm = np.linalg.norm(stored)
        if norm == 0:
            continue
        stored_normed = stored / norm
        score = float(np.dot(q_arr, stored_normed))
        metadata = json.loads(meta_json) if meta_json else {}
        results.append({"id": rec_id, "score": score, "metadata": metadata, "chunk_text": chunk_text})

    # Sort by descending similarity
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


def delete_embeddings_for_file(file_name: str) -> None:
    """
    Remove all stored embeddings whose metadata.file_name == file_name.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "DELETE FROM embeddings WHERE json_extract(metadata, '$.file_name') = ?",
        (file_name,)
    )
    conn.commit()
    conn.close()
