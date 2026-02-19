from __future__ import annotations

import argparse
from pathlib import Path

from pypdf import PdfReader

from src.assistant.config import settings
from src.assistant.rag.store import RagStore


def chunk_text(text: str, chunk_size_words: int = 500) -> list[str]:
    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    for idx in range(0, len(words), chunk_size_words):
        chunks.append(" ".join(words[idx : idx + chunk_size_words]))
    return chunks


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md", ".log"}:
        return path.read_text(encoding="utf-8", errors="ignore")
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    return ""


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest docs into local RAG store")
    parser.add_argument("docs_path", type=Path, help="File or directory to ingest")
    parser.add_argument("--source", default="local_docs", help="Source label")
    parser.add_argument("--chunk-size", type=int, default=500, help="Chunk size in words")
    args = parser.parse_args()

    store = RagStore(settings.rag_data_dir, settings.embedding_model)

    candidates: list[Path]
    if args.docs_path.is_dir():
        candidates = [p for p in args.docs_path.rglob("*") if p.is_file()]
    else:
        candidates = [args.docs_path]

    total_chunks = 0
    for file_path in candidates:
        text = extract_text(file_path)
        if not text.strip():
            continue
        chunks = chunk_text(text, chunk_size_words=args.chunk_size)
        added = store.add_chunks(source=f"{args.source}:{file_path.name}", chunks=chunks)
        total_chunks += added
        print(f"Ingested {added} chunks from {file_path}")

    print(f"Done. Total chunks added: {total_chunks}")


if __name__ == "__main__":
    main()
