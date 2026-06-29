from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
VECTORSTORE_DIR = BASE_DIR / "vectorstores"
OUTPUTS_DIR = BASE_DIR / "outputs"
TICKET_REGISTRY_PATH = OUTPUTS_DIR / "registro_tickets.txt"

INSUFFICIENT_INFO_MESSAGE = "No encontré información suficiente en la base documental proporcionada."


@dataclass(frozen=True)
class Settings:
    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
    gemini_llm_model: str = os.getenv("GEMINI_LLM_MODEL", "gemini-2.0-flash")
    gemini_embedding_model: str = os.getenv(
        "GEMINI_EMBEDDING_MODEL", "models/text-embedding-004"
    )
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "800"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "120"))
    retriever_k: int = int(os.getenv("RETRIEVER_K", "3"))

    def require_google_api_key(self) -> str:
        if not self.google_api_key:
            raise RuntimeError(
                "Falta GOOGLE_API_KEY. Copia .env.example a .env y agrega tu API key de Google AI Studio."
            )
        return self.google_api_key


settings = Settings()


@dataclass(frozen=True)
class KnowledgeBaseSpec:
    agent_key: str
    display_name: str
    data_file: Path
    persist_directory: Path
    collection_name: str


KNOWLEDGE_BASES: dict[str, KnowledgeBaseSpec] = {
    "infraestructura": KnowledgeBaseSpec(
        agent_key="infraestructura",
        display_name="Agente de Infraestructura y Servicios",
        data_file=DATA_DIR / "catalogo_servicios.txt",
        persist_directory=VECTORSTORE_DIR / "infraestructura",
        collection_name="patito_infraestructura",
    ),
    "seguridad": KnowledgeBaseSpec(
        agent_key="seguridad",
        display_name="Agente de Seguridad y Accesos",
        data_file=DATA_DIR / "politica_seguridad.txt",
        persist_directory=VECTORSTORE_DIR / "seguridad",
        collection_name="patito_seguridad",
    ),
    "incidentes": KnowledgeBaseSpec(
        agent_key="incidentes",
        display_name="Agente de Gestión de Incidentes",
        data_file=DATA_DIR / "gestion_incidentes_sla.txt",
        persist_directory=VECTORSTORE_DIR / "incidentes",
        collection_name="patito_incidentes",
    ),
}
