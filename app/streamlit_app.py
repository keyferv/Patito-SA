from __future__ import annotations

import sys
from pathlib import Path
from html import escape

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

###
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_ticket" not in st.session_state:
    st.session_state.pending_ticket = None
if "chat_questions" not in st.session_state:
    st.session_state.chat_questions = []
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []
if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = None
if "chat_counter" not in st.session_state:
    st.session_state.chat_counter = 0


def build_chat_title(messages):
    for message in messages:
        if message["role"] == "user":
            title = message["content"].strip()
            return title[:45] + "..." if len(title) > 45 else title
    return "Chat sin título"


def save_current_chat():
    if not st.session_state.messages:
        return

    if st.session_state.active_chat_id is None:
        st.session_state.chat_counter += 1
        st.session_state.active_chat_id = f"chat-{st.session_state.chat_counter}"

    chat_data = {
        "id": st.session_state.active_chat_id,
        "title": build_chat_title(st.session_state.messages),
        "messages": [
            {"role": msg["role"], "content": msg["content"]}
            for msg in st.session_state.messages
        ],
    }

    st.session_state.chat_sessions = [
        chat for chat in st.session_state.chat_sessions
        if chat["id"] != st.session_state.active_chat_id
    ]

    st.session_state.chat_sessions.insert(0, chat_data)


def load_chat(chat_id):
    for chat in st.session_state.chat_sessions:
        if chat["id"] == chat_id:
            st.session_state.messages = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in chat["messages"]
            ]
            st.session_state.active_chat_id = chat_id
            st.session_state.pending_ticket = None
            break

# Historial de chat - JACHO

    st.header("💬 Historial de chat")

    total_mensajes = len(st.session_state.messages)
    st.caption(f"Mensajes en esta sesión: {total_mensajes}")

    if st.session_state.messages:
        for index, message in enumerate(st.session_state.messages, start=1):
            role = "Usuario" if message["role"] == "user" else "PatitoDesk IA"
            st.markdown(f"**{index}. {role}:**")
            st.write(message["content"])
            st.divider()
    else:
        st.info("Aún no hay mensajes en el historial.")

    if st.button("🧹 Limpiar historial"):
        st.session_state.messages = []
        st.session_state.pending_ticket = None
        st.rerun()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Escribe tu consulta para PatitoDesk IA...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.chat_questions.append(question)
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Consultando agentes..."):
            response = answer_question(question)

        st.markdown(response.answer)
        st.session_state.messages.append({"role": "assistant", "content": response.answer})
        save_current_chat()

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


####
with st.sidebar:
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f2a33 0%, #071820 100%);
        }

        section[data-testid="stSidebar"] * {
            color: #f5fbff;
        }

        div[data-testid="stSidebarContent"] {
            padding-top: 1.6rem;
        }

        .water-card {
            text-align: center;
            padding: 1.7rem 1.2rem;
            border-radius: 1.8rem;
            margin-bottom: 1.6rem;
            background:
                radial-gradient(circle at 25% 15%, rgba(115, 214, 255, 0.45), transparent 35%),
                radial-gradient(circle at 80% 5%, rgba(255, 255, 255, 0.18), transparent 35%),
                linear-gradient(135deg, rgba(57, 153, 184, 0.95), rgba(10, 52, 66, 0.98));
            border: 1px solid rgba(157, 225, 248, 0.42);
            box-shadow: 0 20px 45px rgba(0, 0, 0, 0.28);
        }

        .water-logo {
            width: 4.3rem;
            height: 4.3rem;
            margin: 0 auto 0.9rem auto;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(255, 255, 255, 0.16);
            border: 1px solid rgba(255, 255, 255, 0.30);
            backdrop-filter: blur(8px);
            font-size: 2.25rem;
            line-height: 1;
        }

        .sidebar-title {
            font-size: 1.4rem;
            font-weight: 800;
            letter-spacing: 0.03rem;
            margin-bottom: 0.35rem;
        }

        .sidebar-subtitle {
            font-size: 0.9rem;
            opacity: 0.9;
        }

        .section-label {
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.16rem;
            opacity: 0.72;
            margin: 1.35rem 0 0.7rem 0.25rem;
            font-weight: 800;
        }

        .action-icon {
            width: 2.15rem;
            height: 2.15rem;
            border-radius: 0.75rem;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(255, 255, 255, 0.10);
            border: 1px solid rgba(255, 255, 255, 0.12);
            margin-top: 0.32rem;
        }

        .eq-icon {
            height: 1rem;
            display: flex;
            gap: 0.14rem;
            align-items: center;
        }

        .eq-icon span {
            display: block;
            width: 0.14rem;
            border-radius: 999px;
            background: #f5fbff;
        }

        .eq-icon span:nth-child(1) { height: 0.45rem; }
        .eq-icon span:nth-child(2) { height: 0.75rem; }
        .eq-icon span:nth-child(3) { height: 1rem; }
        .eq-icon span:nth-child(4) { height: 0.75rem; }
        .eq-icon span:nth-child(5) { height: 0.45rem; }

        .trash-icon svg {
            width: 1.05rem;
            height: 1.05rem;
            stroke: #f5fbff;
        }

        section[data-testid="stSidebar"] div.stButton > button {
            width: 100%;
            min-height: 2.85rem;
            border-radius: 1rem;
            padding: 0.72rem 0.9rem;
            background: rgba(255, 255, 255, 0.10);
            border: 1px solid rgba(255, 255, 255, 0.14);
            color: #f5fbff;
            font-weight: 700;
            font-size: 0.95rem;
            transition: 0.18s ease;
        }

        section[data-testid="stSidebar"] div.stButton > button:hover {
            background: rgba(69, 190, 225, 0.32);
            border-color: rgba(128, 226, 255, 0.58);
            color: white;
            transform: translateY(-1px);
        }

        .chat-item {
            padding: 0.85rem 0.95rem;
            border-radius: 1rem;
            margin-bottom: 0.55rem;
            background: rgba(255, 255, 255, 0.08);
            font-size: 0.9rem;
            line-height: 1.35;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .chat-item:hover {
            background: rgba(67, 184, 220, 0.20);
            border-color: rgba(105, 211, 245, 0.38);
        }

        .empty-history {
            padding: 0.9rem 1rem;
            border-radius: 1rem;
            background: rgba(255, 255, 255, 0.08);
            font-size: 0.9rem;
            opacity: 0.86;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="water-card">
            <div class="water-logo">🦆</div>
            <div class="sidebar-title">PatitoDesk IA</div>
            <div class="sidebar-subtitle">Mesa de ayuda inteligente</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-label">Acciones</div>', unsafe_allow_html=True)

    col_icon_new, col_btn_new = st.columns([0.16, 0.84])
    with col_icon_new:
        st.markdown(
            """
            <div class="action-icon">
                <div class="eq-icon">
                    <span></span><span></span><span></span><span></span><span></span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_btn_new:
        if st.button("Nuevo chat", use_container_width=True):
            save_current_chat()
            st.session_state.messages = []
            st.session_state.pending_ticket = None
            st.session_state.active_chat_id = None
            st.rerun()

    col_icon_clear, col_btn_clear = st.columns([0.16, 0.84])
    with col_icon_clear:
        st.markdown(
            """
            <div class="action-icon trash-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 7h16"></path>
                    <path d="M10 11v6"></path>
                    <path d="M14 11v6"></path>
                    <path d="M6 7l1 13h10l1-13"></path>
                    <path d="M9 7V4h6v3"></path>
                </svg>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_btn_clear:
        if st.button("Limpiar historial", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chat_questions = []
            st.session_state.chat_sessions = []
            st.session_state.pending_ticket = None
            st.session_state.active_chat_id = None
            st.rerun()

    st.markdown('<div class="section-label">Recientes</div>', unsafe_allow_html=True)

    if st.session_state.chat_sessions:
       for chat in st.session_state.chat_sessions[:10]:
            if st.button(chat["title"], key=f"recent-{chat['id']}", use_container_width=True):
                load_chat(chat["id"])
                st.rerun()
    else:
        st.markdown(
            '<div class="empty-history">No hay chats recientes.</div>',
            unsafe_allow_html=True,
        )