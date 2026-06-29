from pathlib import Path

from app.agents.action_agent import confirm_ticket, create_ticket_draft


def test_software_ticket_missing_fields_does_not_require_confirmation():
    draft = create_ticket_draft("Crea un ticket para instalar Figma")

    assert draft.ticket_type == "software"
    assert not draft.requires_confirmation
    assert "versión" in draft.missing_fields
    assert "motivo" in draft.missing_fields
    assert "jefe que aprueba" in draft.missing_fields


def test_incident_ticket_complete_generates_pending_draft():
    draft = create_ticket_draft(
        "Crea un ticket por caída del sistema de facturación, descripción: no permite emitir facturas, prioridad alta."
    )

    assert draft.ticket_type == "incidente"
    assert draft.requires_confirmation
    assert draft.missing_fields == []
    assert draft.signature


def test_confirm_ticket_writes_file(tmp_path: Path):
    draft = create_ticket_draft(
        "Crea un ticket para instalar Figma, versión más reciente, motivo diseño de piezas, aprobado por el jefe de Marketing."
    )
    output_path = tmp_path / "registro_tickets.txt"

    result = confirm_ticket(draft, output_path=output_path)

    assert result.success
    content = output_path.read_text(encoding="utf-8")
    assert "ticket_type: software" in content
    assert "Figma" in content


def test_duplicate_ticket_is_rejected(tmp_path: Path):
    draft = create_ticket_draft(
        "Crea un ticket para instalar Figma, versión más reciente, motivo diseño de piezas, aprobado por el jefe de Marketing."
    )
    output_path = tmp_path / "registro_tickets.txt"

    first = confirm_ticket(draft, output_path=output_path)
    second = confirm_ticket(draft, output_path=output_path)

    assert first.success
    assert not second.success
    assert "duplicado" in second.message.lower()
