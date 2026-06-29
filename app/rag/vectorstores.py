from __future__ import annotations

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config import KNOWLEDGE_BASES, Settings, settings


def get_embeddings(config: Settings = settings) -> GoogleGenerativeAIEmbeddings:
    config.require_google_api_key()
    return GoogleGenerativeAIEmbeddings(model=config.gemini_embedding_model)


def load_vectorstore(agent_key: str, config: Settings = settings) -> Chroma:
    if agent_key not in KNOWLEDGE_BASES:
        raise KeyError(f"Base de conocimiento no soportada: {agent_key}")

    spec = KNOWLEDGE_BASES[agent_key]
    if not spec.persist_directory.exists() or not any(spec.persist_directory.iterdir()):
        raise FileNotFoundError(
            f"No existe el índice vectorial para {agent_key}. Ejecuta: python -m app.rag.build_indexes"
        )

    return Chroma(
        collection_name=spec.collection_name,
        persist_directory=str(spec.persist_directory),
        embedding_function=get_embeddings(config),
    )


def load_retriever(agent_key: str, config: Settings = settings):
    vectorstore = load_vectorstore(agent_key, config)
    return vectorstore.as_retriever(search_kwargs={"k": config.retriever_k})
