from app.agents.base_rag_agent import RagAgent
from app.config import KNOWLEDGE_BASES
from app.schemas.response import AgentResponse


def answer_incident(question: str) -> AgentResponse:
    spec = KNOWLEDGE_BASES["incidentes"]
    return RagAgent(spec.agent_key, spec.display_name).answer(question)
