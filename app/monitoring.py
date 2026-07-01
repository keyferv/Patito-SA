from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from app.config import KNOWLEDGE_BASES, KnowledgeBaseSpec


@dataclass(frozen=True)
class KBHealth:
    key: str
    name: str
    data_file_exists: bool
    data_file_bytes: int
    vectorstore_exists: bool
    vectorstore_file_count: int
    chroma_db_ok: bool | None
    error: str | None = None


def check_knowledge_bases(
    knowledge_bases: Mapping[str, KnowledgeBaseSpec] = KNOWLEDGE_BASES,
) -> list[KBHealth]:
    results: list[KBHealth] = []
    for key, spec in knowledge_bases.items():
        err: str | None = None
        data_ok = spec.data_file.is_file()
        data_bytes = spec.data_file.stat().st_size if data_ok else 0

        vec_dir = spec.persist_directory
        vec_ok = vec_dir.is_dir()
        vec_files = _count_files(vec_dir) if vec_ok else 0

        chroma_ok: bool | None = None
        if vec_ok and vec_files > 0:
            chroma_db = vec_dir / "chroma.sqlite3"
            chroma_ok = chroma_db.is_file() and chroma_db.stat().st_size > 0

        results.append(
            KBHealth(
                key=key,
                name=spec.display_name,
                data_file_exists=data_ok,
                data_file_bytes=data_bytes,
                vectorstore_exists=vec_ok,
                vectorstore_file_count=vec_files,
                chroma_db_ok=chroma_ok,
                error=err,
            )
        )
    return results


def _count_files(directory: Path) -> int:
    try:
        return sum(1 for _ in directory.rglob("*") if _.is_file())
    except OSError:
        return 0


def status_label(value: bool | None) -> str:
    if value is None:
        return "Sin índice"
    return "OK" if value else "Falta"
