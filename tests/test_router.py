from app.config import INSUFFICIENT_INFO_MESSAGE
from app.orchestrator.router import answer_question, route_intents
from app.agents.base_rag_agent import _message_content_to_text


def test_routes_software_to_infrastructure():
    assert route_intents("¿Qué debo hacer para solicitar la instalación de Figma?") == [
        "infraestructura"
    ]


def test_routes_vpn_to_security():
    assert route_intents("Necesito acceso por VPN y permisos temporales") == ["seguridad"]


def test_routes_billing_outage_to_incidents():
    assert "incidentes" in route_intents("El sistema de facturación está caído, ¿qué prioridad tiene?")


def test_routes_mixed_question_to_multiple_agents():
    intents = route_intents("Facturación está caída y necesito acceso temporal a base de datos")
    assert "incidentes" in intents
    assert "seguridad" in intents


def test_routes_ticket_to_action_and_domain_agent():
    intents = route_intents("Crea un ticket para instalar Figma")
    assert "accion" in intents
    assert "infraestructura" in intents


def test_normalizes_structured_llm_text_content():
    content = [{"type": "text", "text": "Respuesta limpia", "extras": {"signature": "abc"}}]

    assert _message_content_to_text(content) == "Respuesta limpia"


def test_out_of_scope_question_returns_clean_insufficient_response():
    response = answer_question("¿Cuál es la política para comprar almuerzos de empleados?")

    assert response.answer == INSUFFICIENT_INFO_MESSAGE
    assert response.warnings == []
    assert response.agents == []
