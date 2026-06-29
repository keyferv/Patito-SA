from __future__ import annotations

import shutil
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import KNOWLEDGE_BASES, Settings, settings
from app.rag.vectorstores import get_embeddings


def _load_document(path: Path, agent_key: str) -> Document:
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo requerido: {path}")
    text = path.read_text(encoding="utf-8")
    return Document(page_content=text, metadata={"source": path.name, "agent": agent_key})


def build_indexes(config: Settings = settings) -> None:
    config.require_google_api_key()
    embeddings = get_embeddings(config)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    for agent_key, spec in KNOWLEDGE_BASES.items():
        print(f"\n[PatitoDesk IA] Generando índice para: {spec.display_name}")
        print(f"  Documento: {spec.data_file}")
        document = _load_document(spec.data_file, agent_key)
        chunks = splitter.split_documents([document])
        for index, chunk in enumerate(chunks, start=1):
            chunk.metadata["chunk_index"] = index
            chunk.metadata["chunk_id"] = f"{agent_key}-{index}"

        if spec.persist_directory.exists():
            shutil.rmtree(spec.persist_directory)
        spec.persist_directory.mkdir(parents=True, exist_ok=True)

        Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name=spec.collection_name,
            persist_directory=str(spec.persist_directory),
        )
        print(f"  Chunks creados: {len(chunks)}")
        print(f"  Persistido en: {spec.persist_directory}")

    print("\n[PatitoDesk IA] Índices generados correctamente.")


if __name__ == "__main__":
    build_indexes()
