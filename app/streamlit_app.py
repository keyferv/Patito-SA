from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.agents.action_agent import confirm_ticket
from app.orchestrator.router import answer_question
from app.schemas.ticket import TicketDraft

st.set_page_config(page_title="PatitoDesk IA")


def init_session_state() -> None:
    defaults = {
        "messages": [],
        "pending_ticket": None,
        "chat_sessions": [],
        "active_chat_id": None,
        "chat_counter": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def build_chat_title(messages: list[dict[str, str]]) -> str:
    for message in messages:
        if message.get("role") == "user":
            title = message.get("content", "").strip()
            return f"{title[:45]}..." if len(title) > 45 else title
    return "Chat sin título"


def save_current_chat() -> None:
    if not st.session_state.messages:
        return

    if st.session_state.active_chat_id is None:
        st.session_state.chat_counter += 1
        st.session_state.active_chat_id = f"chat-{st.session_state.chat_counter}"

    chat_data = {
        "id": st.session_state.active_chat_id,
        "title": build_chat_title(st.session_state.messages),
        "messages": [
            {"role": message["role"], "content": message["content"]}
            for message in st.session_state.messages
        ],
    }

    st.session_state.chat_sessions = [
        chat
        for chat in st.session_state.chat_sessions
        if chat["id"] != st.session_state.active_chat_id
    ]
    st.session_state.chat_sessions.insert(0, chat_data)


def load_chat(chat_id: str) -> None:
    for chat in st.session_state.chat_sessions:
        if chat["id"] == chat_id:
            st.session_state.messages = [
                {"role": message["role"], "content": message["content"]}
                for message in chat["messages"]
            ]
            st.session_state.active_chat_id = chat_id
            st.session_state.pending_ticket = None
            return


def start_new_chat() -> None:
    save_current_chat()
    st.session_state.messages = []
    st.session_state.pending_ticket = None
    st.session_state.active_chat_id = None


def clear_history() -> None:
    st.session_state.messages = []
    st.session_state.pending_ticket = None
    st.session_state.chat_sessions = []
    st.session_state.active_chat_id = None


def render_sidebar() -> None:
    with st.sidebar:
        st.title("PatitoDesk IA")
        st.caption("Mesa de ayuda inteligente")

        if st.button("Nuevo chat", use_container_width=True):
            start_new_chat()
            st.rerun()

        if st.button("Limpiar historial", use_container_width=True):
            clear_history()
            st.rerun()

        st.divider()
        st.subheader("Chats recientes")

        if not st.session_state.chat_sessions:
            st.caption("No hay chats recientes.")
            return

        for chat in st.session_state.chat_sessions[:10]:
            if st.button(chat["title"], key=f"recent-{chat['id']}", use_container_width=True):
                load_chat(chat["id"])
                st.rerun()


def render_messages() -> None:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def render_agent_details(response) -> None:
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


def handle_ticket_draft(draft: TicketDraft) -> None:
    if draft.missing_fields:
        st.error(draft.message)
        st.session_state.pending_ticket = None
        return

    if draft.requires_confirmation:
        st.info(draft.message)
        st.json(draft.data)
        st.session_state.pending_ticket = draft.model_dump()


def handle_question(question: str) -> None:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Consultando agentes..."):
            response = answer_question(question)

        st.markdown(response.answer)
        st.session_state.messages.append({"role": "assistant", "content": response.answer})
        save_current_chat()

        render_agent_details(response)
        if response.ticket_draft:
            handle_ticket_draft(response.ticket_draft)


def render_ticket_confirmation() -> None:
    if not st.session_state.pending_ticket:
        return

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


def main() -> None:
    init_session_state()
    render_sidebar()

    st.title("PatitoDesk IA")
    st.write(
        "Prototipo académico de mesa de ayuda IA para TI con agentes especializados, RAG, Gemini y LangChain."
    )

    render_messages()

    question = st.chat_input("Escribe tu consulta para PatitoDesk IA...")
    if question:
        handle_question(question)

    render_ticket_confirmation()


main()
