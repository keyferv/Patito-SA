from __future__ import annotations

from langchain_core.documents import Document

from app.schemas.response import SourceChunk


def document_to_source(agent_name: str, document: Document, index: int) -> SourceChunk:
    metadata = document.metadata or {}
    source = str(metadata.get("source", "documento_desconocido"))
    chunk_id = str(metadata.get("chunk_id", metadata.get("chunk_index", index)))
    content = " ".join(document.page_content.split())
    return SourceChunk(
        agent=agent_name,
        source=source,
        chunk_id=chunk_id,
        content=content[:900],
    )
