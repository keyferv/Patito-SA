from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import INSUFFICIENT_INFO_MESSAGE, Settings, settings
from app.rag.prompts import RAG_AGENT_SYSTEM_PROMPT
from app.rag.vectorstores import load_retriever
from app.schemas.response import AgentResponse
from app.utils.source_formatter import document_to_source


def _message_content_to_text(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text", "")))
            else:
                parts.append(str(item))
        return "\n".join(part for part in parts if part)
    return str(content)


class RagAgent:
    def __init__(self, agent_key: str, display_name: str, config: Settings = settings) -> None:
        self.agent_key = agent_key
        self.display_name = display_name
        self.config = config

    def answer(self, question: str) -> AgentResponse:
        try:
            retriever = load_retriever(self.agent_key, self.config)
            documents = retriever.invoke(question)
            sources = [
                document_to_source(self.display_name, doc, idx)
                for idx, doc in enumerate(documents, start=1)
            ]
            if not documents:
                return AgentResponse(agent=self.display_name, answer=INSUFFICIENT_INFO_MESSAGE)

            context = "\n\n".join(
                f"Fuente: {source.source} | Chunk: {source.chunk_id}\n{source.content}"
                for source in sources
            )
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", RAG_AGENT_SYSTEM_PROMPT),
                    (
                        "human",
                        "Pregunta del usuario:\n{question}\n\nContexto recuperado:\n{context}\n\nRespuesta:",
                    ),
                ]
            )
            llm = ChatGoogleGenerativeAI(
                model=self.config.gemini_llm_model,
                temperature=0,
                convert_system_message_to_human=True,
            )
            chain = prompt | llm
            result = chain.invoke({"question": question, "context": context})
            answer = _message_content_to_text(getattr(result, "content", result)).strip()
            answer = answer or INSUFFICIENT_INFO_MESSAGE
            return AgentResponse(agent=self.display_name, answer=answer, sources=sources)
        except Exception as exc:
            return AgentResponse(
                agent=self.display_name,
                answer=INSUFFICIENT_INFO_MESSAGE,
                warning=f"No se pudo consultar {self.display_name}: {exc}",
            )
