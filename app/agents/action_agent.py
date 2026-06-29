from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from app.config import TICKET_REGISTRY_PATH
from app.schemas.ticket import TicketDraft, TicketResult
from app.utils.ticket_writer import write_ticket

try:
    from langchain_core.tools import StructuredTool
except ModuleNotFoundError:  # Allows unit tests to run before dependencies are installed.
    StructuredTool = None

SOFTWARE_FIELDS = {
    "software": "software",
    "version": "versión",
    "motivo": "motivo",
    "approver": "jefe que aprueba",
}
INCIDENT_FIELDS = {
    "system_affected": "sistema afectado",
    "description": "descripción",
    "priority": "prioridad",
}


def _strip_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def _norm(text: str) -> str:
    text = _strip_accents(text).lower()
    return re.sub(r"\s+", " ", text).strip()


def _capture(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return None
    value = match.group(1).strip(" .,:;\n\t")
    return value or None


def detect_ticket_type(question: str) -> str:
    q = _norm(question)
    if any(word in q for word in ["incidente", "caida", "falla", "error", "facturacion", "prioridad"]):
        return "incidente"
    return "software"


def _extract_software_data(question: str) -> dict[str, str]:
    data: dict[str, str] = {}
    software = _capture(r"(?:instalar|instalaci[oó]n de|software)\s+([^,.;]+)", question)
    version = _capture(r"versi[oó]n\s*:?\s*([^,.;]+)", question)
    motivo = _capture(r"motivo\s*:?\s*([^,.;]+)", question)
    approver = _capture(r"(?:aprobado por|aprueba|jefe que aprueba)\s+(?:el\s+)?([^,.;]+)", question)

    if software:
        data["software"] = software
    if version:
        data["version"] = version
    if motivo:
        data["motivo"] = motivo
    if approver:
        data["approver"] = approver
    return data


def _extract_incident_data(question: str) -> dict[str, str]:
    data: dict[str, str] = {}
    system = _capture(r"(?:sistema afectado|sistema de|ca[ií]da del sistema de)\s*:?\s*([^,.;]+)", question)
    description = _capture(r"descripci[oó]n\s*:?\s*([^,.;]+)", question)
    priority = _capture(r"prioridad\s*:?\s*([^,.;]+)", question)

    if system:
        data["system_affected"] = f"sistema de {system}" if not _norm(system).startswith("sistema") else system
    if description:
        data["description"] = description
    if priority:
        data["priority"] = priority
    return data


def _signature(ticket_type: str, data: dict[str, str]) -> str:
    normalized_pairs = [f"{key}={_norm(value)}" for key, value in sorted(data.items())]
    return f"{ticket_type}|" + "|".join(normalized_pairs)


def create_ticket_draft(question: str) -> TicketDraft:
    ticket_type = detect_ticket_type(question)
    required = INCIDENT_FIELDS if ticket_type == "incidente" else SOFTWARE_FIELDS
    data = _extract_incident_data(question) if ticket_type == "incidente" else _extract_software_data(question)
    missing = [label for key, label in required.items() if not data.get(key)]

    if missing:
        return TicketDraft(
            ticket_type=ticket_type,
            data=data,
            missing_fields=missing,
            requires_confirmation=False,
            message="No se registró el ticket. Faltan datos obligatorios: " + ", ".join(missing) + ".",
        )

    signature = _signature(ticket_type, data)
    return TicketDraft(
        ticket_type=ticket_type,
        data=data,
        missing_fields=[],
        requires_confirmation=True,
        message="Datos completos. Confirma para registrar el ticket en outputs/registro_tickets.txt.",
        signature=signature,
    )


def confirm_ticket(draft: TicketDraft, output_path: Path = TICKET_REGISTRY_PATH) -> TicketResult:
    return write_ticket(draft, output_path=output_path)


def register_ticket_from_fields(ticket_type: str, data: dict[str, str], signature: str) -> TicketResult:
    draft = TicketDraft(
        ticket_type=ticket_type,
        data=data,
        missing_fields=[],
        requires_confirmation=True,
        message="Registro confirmado.",
        signature=signature,
    )
    return confirm_ticket(draft)


def build_register_ticket_tool():
    if StructuredTool is None:
        raise RuntimeError("Instala las dependencias de LangChain para construir la tool de registro.")
    return StructuredTool.from_function(
        func=register_ticket_from_fields,
        name="registrar_ticket_patito",
        description="Registra un ticket validado y confirmado en outputs/registro_tickets.txt.",
    )
