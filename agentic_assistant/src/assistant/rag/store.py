from __future__ import annotations

import json
import importlib
import sqlite3
import uuid
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from sentence_transformers import SentenceTransformer


class RagStore:
    def __init__(self, data_dir: Path, embedding_model: str) -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.index_path = self.data_dir / "vectors.bin"
        self.meta_path = self.data_dir / "index_meta.json"
        self.sqlite_path = self.data_dir / "chunks.sqlite3"

        self.embedder = SentenceTransformer(embedding_model)
        dimension = self.embedder.get_sentence_embedding_dimension()
        if dimension is None:
            raise RuntimeError("Embedding model did not provide output dimension")
        self.dimension = int(dimension)

        self.index: Any = None
        self._ensure_sqlite()
        self._load_or_create_index()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.sqlite_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_sqlite(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS chunks (
                    id TEXT PRIMARY KEY,
                    source TEXT NOT NULL,
                    chunk_index INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def _load_or_create_index(self) -> None:
        try:
            hnswlib = importlib.import_module("hnswlib")
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "hnswlib is not installed in the active Python environment. "
                "Install dependencies from requirements.txt before using RAG."
            ) from exc

        self.index = hnswlib.Index(space="cosine", dim=self.dimension)

        if self.index_path.exists() and self.meta_path.exists():
            with self.meta_path.open("r", encoding="utf-8") as handle:
                meta = json.load(handle)

            max_elements = max(meta.get("max_elements", 10000), 10000)
            self.index.load_index(str(self.index_path), max_elements=max_elements)
            self.index.set_ef(100)
            return

        self.index.init_index(max_elements=10000, ef_construction=100, M=16)
        self.index.set_ef(100)

    def _save_meta(self) -> None:
        if self.index is None:
            return
        meta = {
            "max_elements": max(self.index.get_max_elements(), 10000),
            "current_count": self.index.get_current_count(),
            "dimension": self.dimension,
        }
        with self.meta_path.open("w", encoding="utf-8") as handle:
            json.dump(meta, handle, indent=2)

    def add_chunks(self, source: str, chunks: Iterable[str]) -> int:
        chunk_list = [chunk.strip() for chunk in chunks if chunk.strip()]
        if not chunk_list:
            return 0

        embeddings = self.embedder.encode(chunk_list, convert_to_numpy=True).astype(np.float32)

        if self.index is None:
            raise RuntimeError("Vector index is not initialized")

        existing_count = self.index.get_current_count()
        required = existing_count + len(chunk_list)
        if required > self.index.get_max_elements():
            self.index.resize_index(max(required * 2, 10000))

        labels = np.arange(existing_count, required)
        self.index.add_items(embeddings, labels)

        rows: list[tuple[str, str, int, str]] = []
        for chunk_idx, content in enumerate(chunk_list):
            rows.append((str(uuid.uuid4()), source, chunk_idx, content))

        with self._connect() as conn:
            conn.executemany(
                "INSERT INTO chunks (id, source, chunk_index, content) VALUES (?, ?, ?, ?)",
                rows,
            )
            conn.commit()

        self.index.save_index(str(self.index_path))
        self._save_meta()
        return len(chunk_list)

    def query(self, text: str, top_k: int = 3) -> list[dict]:
        if self.index is None or self.index.get_current_count() == 0:
            return []

        vector = self.embedder.encode([text], convert_to_numpy=True).astype(np.float32)
        labels, distances = self.index.knn_query(vector, k=min(top_k, self.index.get_current_count()))
        label_list = labels[0].tolist()
        score_list = distances[0].tolist()

        with self._connect() as conn:
            db_rows = conn.execute(
                "SELECT source, chunk_index, content FROM chunks ORDER BY rowid"
            ).fetchall()

        results: list[dict] = []
        for label, score in zip(label_list, score_list):
            if 0 <= label < len(db_rows):
                row = db_rows[label]
                results.append(
                    {
                        "source": row["source"],
                        "chunk_index": row["chunk_index"],
                        "content": row["content"],
                        "distance": float(score),
                    }
                )
        return results
