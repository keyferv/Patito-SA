from __future__ import annotations

from pydantic import BaseModel, Field

from app.config import INSUFFICIENT_INFO_MESSAGE
from app.schemas.ticket import TicketDraft


class SourceChunk(BaseModel):
    agent: str
    source: str
    chunk_id: str
    content: str


class AgentResponse(BaseModel):
    agent: str
    answer: str
    sources: list[SourceChunk] = Field(default_factory=list)
    warning: str | None = None

    @property
    def has_sufficient_info(self) -> bool:
        return self.answer.strip() != INSUFFICIENT_INFO_MESSAGE


class OrchestratorResponse(BaseModel):
    answer: str
    agents: list[str] = Field(default_factory=list)
    sources: list[SourceChunk] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    ticket_draft: TicketDraft | None = None
