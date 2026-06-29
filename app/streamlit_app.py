from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.agents.action_agent import confirm_ticket
from app.config import INSUFFICIENT_INFO_MESSAGE
from app.orchestrator.router import answer_question
from app.schemas.ticket import TicketDraft

st.set_page_config(page_title="PatitoDesk IA", page_icon="🦆")

st.title("PatitoDesk IA")
st.write(
    "Prototipo académico de mesa de ayuda IA para TI con agentes especializados, RAG, Gemini y LangChain."
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_ticket" not in st.session_state:
    st.session_state.pending_ticket = None

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Escribe tu consulta para PatitoDesk IA...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Consultando agentes..."):
            response = answer_question(question)

        st.markdown(response.answer)
        st.session_state.messages.append({"role": "assistant", "content": response.answer})

        if response.agents:
            st.subheader("Agentes participantes")
            for agent in response.agents:
                st.write(f"- {agent}")

        if response.sources:
            st.subheader("Fuentes utilizadas")
            for source in response.sources:
                with st.expander(f"{source.agent} · {source.source} · chunk {source.chunk_id}"):
                    st.write(source.content)

        if response.warnings:
            st.subheader("Advertencias")
            for warning in response.warnings:
                st.warning(warning)

        if response.ticket_draft:
            draft: TicketDraft = response.ticket_draft
            if draft.missing_fields:
                st.error(draft.message)
                st.session_state.pending_ticket = None
            elif draft.requires_confirmation:
                st.info(draft.message)
                st.json(draft.data)
                st.session_state.pending_ticket = draft.model_dump()

if st.session_state.pending_ticket:
    st.divider()
    st.subheader("Confirmación de ticket pendiente")
    pending = TicketDraft.model_validate(st.session_state.pending_ticket)
    st.json(pending.data)
    if st.button("Confirmar y registrar ticket"):
        result = confirm_ticket(pending)
        if result.success:
            st.success(result.message)
            st.session_state.pending_ticket = None
        else:
            st.error(result.message)
