from __future__ import annotations

import tempfile
from pathlib import Path

from app.config import KnowledgeBaseSpec
from app.monitoring import KBHealth, _count_files, check_knowledge_bases, status_label


def test_count_files_returns_zero_for_missing_dir() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        assert _count_files(Path(tmp) / "missing") == 0


def test_count_files_nested() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "a.txt").write_text("hello")
        (d / "sub").mkdir()
        (d / "sub" / "b.txt").write_text("world")
        assert _count_files(d) == 2


def test_status_label_true_ok() -> None:
    assert status_label(True) == "OK"


def test_status_label_false_missing() -> None:
    assert status_label(False) == "Falta"


def test_status_label_none_without_index() -> None:
    assert status_label(None) == "Sin índice"


def test_check_all_returns_health_for_configured_entries() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        data_file = root / "knowledge.txt"
        data_file.write_text("content", encoding="utf-8")
        vectorstore = root / "vectorstore"
        vectorstore.mkdir()
        (vectorstore / "chroma.sqlite3").write_text("db", encoding="utf-8")

        results = check_knowledge_bases(
            {
                "test": KnowledgeBaseSpec(
                    agent_key="test",
                    display_name="Test Agent",
                    data_file=data_file,
                    persist_directory=vectorstore,
                    collection_name="test_collection",
                )
            }
        )

    keys = {h.key for h in results}
    assert keys == {"test"}
    for h in results:
        assert isinstance(h, KBHealth)
        assert h.data_file_exists is True
        assert h.data_file_bytes > 0
        assert h.vectorstore_exists is True
        assert h.vectorstore_file_count == 1
        assert h.chroma_db_ok is True
