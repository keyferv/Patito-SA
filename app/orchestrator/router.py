from __future__ import annotations

from app.agents.action_agent import create_ticket_draft
from app.config import INSUFFICIENT_INFO_MESSAGE
from app.schemas.response import AgentResponse, OrchestratorResponse, SourceChunk

INFRA_KEYWORDS = [
    "software",
    "instalar",
    "instalación",
    "equipo",
    "laptop",
    "hardware",
    "catálogo",
    "servicio",
    "disponibilidad",
    "solicitud",
    "figma",
    "licencia",
]
SECURITY_KEYWORDS = [
    "contraseña",
    "contraseñas",
    "acceso",
    "accesos",
    "vpn",
    "credencial",
    "credenciales",
    "permiso",
    "permisos",
    "mfa",
    "sensible",
    "base de datos",
    "información confidencial",
]
INCIDENT_KEYWORDS = [
    "incidente",
    "falla",
    "fallo",
    "caída",
    "caido",
    "caído",
    "error",
    "prioridad",
    "sla",
    "escalamiento",
    "reporto",
    "reportar",
    "facturación",
    "p1",
    "p2",
    "p3",
    "p4",
]
ACTION_KEYWORDS = ["crear ticket", "crea un ticket", "registrar", "abrir caso", "reportar incidente", "registro"]


def _contains_any(question: str, keywords: list[str]) -> bool:
    normalized = question.lower()
    return any(keyword in normalized for keyword in keywords)


def route_intents(question: str) -> list[str]:
    selected: list[str] = []
    if _contains_any(question, INFRA_KEYWORDS):
        selected.append("infraestructura")
    if _contains_any(question, SECURITY_KEYWORDS):
        selected.append("seguridad")
    if _contains_any(question, INCIDENT_KEYWORDS):
        selected.append("incidentes")
    if _contains_any(question, ACTION_KEYWORDS):
        selected.append("accion")

    if (
        "accion" in selected
        and "incidentes" not in selected
        and _contains_any(question, ["caída", "falla", "incidente", "facturación"])
    ):
        selected.insert(0, "incidentes")
    if (
        "accion" in selected
        and "infraestructura" not in selected
        and _contains_any(question, ["software", "instalar", "figma"])
    ):
        selected.insert(0, "infraestructura")

    return selected


def _run_rag_agent(intent: str, question: str) -> AgentResponse:
    if intent == "infraestructura":
        from app.agents.infra_agent import answer_infrastructure

        return answer_infrastructure(question)
    if intent == "seguridad":
        from app.agents.security_agent import answer_security

        return answer_security(question)
    if intent == "incidentes":
        from app.agents.incident_agent import answer_incident

        return answer_incident(question)
    raise ValueError(f"Intento RAG no soportado: {intent}")


def answer_question(question: str) -> OrchestratorResponse:
    intents = route_intents(question)
    if not intents:
        return OrchestratorResponse(answer=INSUFFICIENT_INFO_MESSAGE)

    agents: list[str] = []
    sources: list[SourceChunk] = []
    warnings: list[str] = []
    answer_parts: list[str] = []
    ticket_draft = None

    for intent in intents:
        if intent == "accion":
            draft = create_ticket_draft(question)
            ticket_draft = draft
            agents.append("Agente de Acción / Registro de tickets")
            answer_parts.append(draft.message)
            continue

        response = _run_rag_agent(intent, question)
        agents.append(response.agent)
        sources.extend(response.sources)
        if response.warning:
            warnings.append(response.warning)
        if response.has_sufficient_info:
            answer_parts.append(response.answer)

    final_answer = (
        "\n\n".join(dict.fromkeys(part.strip() for part in answer_parts if part.strip()))
        if answer_parts
        else INSUFFICIENT_INFO_MESSAGE
    )

    return OrchestratorResponse(
        answer=final_answer,
        agents=list(dict.fromkeys(agents)),
        sources=sources,
        warnings=warnings,
        ticket_draft=ticket_draft,
    )
