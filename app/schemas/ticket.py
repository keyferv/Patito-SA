from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

TicketType = Literal["software", "incidente"]


class TicketDraft(BaseModel):
    ticket_type: TicketType
    data: dict[str, str] = Field(default_factory=dict)
    missing_fields: list[str] = Field(default_factory=list)
    requires_confirmation: bool = False
    message: str
    signature: str | None = None

    @property
    def is_complete(self) -> bool:
        return not self.missing_fields and self.requires_confirmation


class TicketResult(BaseModel):
    success: bool
    message: str
    ticket_id: str | None = None
    ticket_type: TicketType | None = None
    data: dict[str, Any] = Field(default_factory=dict)
