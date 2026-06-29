from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from app.config import TICKET_REGISTRY_PATH
from app.schemas.ticket import TicketDraft, TicketResult


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def ticket_exists(signature: str, output_path: Path = TICKET_REGISTRY_PATH) -> bool:
    return bool(signature) and f"signature: {signature}" in _read_text(output_path)


def write_ticket(draft: TicketDraft, output_path: Path = TICKET_REGISTRY_PATH) -> TicketResult:
    if not draft.is_complete or not draft.signature:
        return TicketResult(
            success=False,
            message="No se puede registrar el ticket porque faltan datos obligatorios o confirmación.",
            ticket_type=draft.ticket_type,
            data=draft.data,
        )

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if ticket_exists(draft.signature, output_path):
            return TicketResult(
                success=False,
                message="No se registró el ticket porque parece ser un duplicado.",
                ticket_type=draft.ticket_type,
                data=draft.data,
            )

        ticket_id = f"PAT-{datetime.now():%Y%m%d%H%M%S}-{uuid4().hex[:6].upper()}"
        payload = {
            "id": ticket_id,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "ticket_type": draft.ticket_type,
            "status": "registrado",
            "data": draft.data,
        }
        with output_path.open("a", encoding="utf-8") as file:
            file.write("---\n")
            file.write(f"id: {payload['id']}\n")
            file.write(f"created_at: {payload['created_at']}\n")
            file.write(f"ticket_type: {payload['ticket_type']}\n")
            file.write("status: registrado\n")
            file.write(f"signature: {draft.signature}\n")
            file.write("data: ")
            file.write(json.dumps(payload["data"], ensure_ascii=False, sort_keys=True))
            file.write("\n")

        return TicketResult(
            success=True,
            message=f"Ticket {ticket_id} registrado correctamente.",
            ticket_id=ticket_id,
            ticket_type=draft.ticket_type,
            data=draft.data,
        )
    except OSError as exc:
        return TicketResult(
            success=False,
            message=f"Error de escritura al registrar el ticket: {exc}",
            ticket_type=draft.ticket_type,
            data=draft.data,
        )
