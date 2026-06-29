# Arquitectura de PatitoDesk IA

La arquitectura está organizada en capas simples: interfaz, orquestación, agentes, recuperación documental, configuración y persistencia local.

## Vista general

```mermaid
flowchart TD
    U[Usuario] --> UI[Streamlit]
    UI --> O[Orquestador]
    O --> IA[Agente Infraestructura]
    O --> SA[Agente Seguridad]
    O --> GA[Agente Incidentes]
    O --> TA[Agente Acción]
    IA --> IR[Retriever infraestructura]
    SA --> SR[Retriever seguridad]
    GA --> GR[Retriever incidentes]
    IR --> IV[(Chroma infraestructura)]
    SR --> SV[(Chroma seguridad)]
    GR --> GV[(Chroma incidentes)]
    TA --> OUT[outputs/registro_tickets.txt]
```

## Capas

| Capa | Responsabilidad | Archivos principales |
|------|-----------------|----------------------|
| Interfaz | Recibe preguntas, muestra respuestas, fuentes y confirmación de tickets. | `app/streamlit_app.py` |
| Orquestación | Detecta intención y decide qué agentes ejecutar. | `app/orchestrator/router.py` |
| Agentes RAG | Consultan documentos por dominio y generan respuestas. | `app/agents/base_rag_agent.py`, `app/agents/*_agent.py` |
| Acción | Valida datos y prepara o registra tickets. | `app/agents/action_agent.py` |
| RAG | Crea embeddings, carga Chroma y expone retrievers. | `app/rag/build_indexes.py`, `app/rag/vectorstores.py` |
| Modelos de datos | Define respuestas, fuentes y tickets. | `app/schemas/*.py` |
| Configuración | Centraliza rutas, variables y bases de conocimiento. | `app/config.py` |
| Persistencia local | Guarda índices y tickets generados. | `vectorstores/`, `outputs/` |

## Flujo de una pregunta

```mermaid
sequenceDiagram
    participant User as Usuario
    participant UI as Streamlit
    participant Router as Orquestador
    participant Agent as Agente RAG
    participant Chroma as Chroma
    participant Gemini as Gemini

    User->>UI: Escribe pregunta
    UI->>Router: answer_question(pregunta)
    Router->>Router: route_intents(pregunta)
    Router->>Agent: Ejecuta agente seleccionado
    Agent->>Chroma: Recupera chunks relevantes
    Agent->>Gemini: Genera respuesta con contexto
    Gemini-->>Agent: Respuesta
    Agent-->>Router: AgentResponse
    Router-->>UI: OrchestratorResponse
    UI-->>User: Muestra respuesta, agentes y fuentes
```

## Flujo de un ticket

```mermaid
sequenceDiagram
    participant User as Usuario
    participant UI as Streamlit
    participant Router as Orquestador
    participant Action as Agente Acción
    participant File as Registro local

    User->>UI: Solicita crear o registrar ticket
    UI->>Router: answer_question(pregunta)
    Router->>Action: create_ticket_draft(pregunta)
    Action->>Action: Detecta tipo y campos faltantes
    Action-->>UI: Borrador de ticket
    User->>UI: Confirma ticket completo
    UI->>Action: confirm_ticket(borrador)
    Action->>File: Escribe en outputs/registro_tickets.txt
```

## Por qué no hay una sola base vectorial

Separar los índices por agente mejora tres cosas:

- Trazabilidad: cada respuesta indica de qué documento salió la fuente.
- Control: un agente no responde con información de otro dominio.
- Depuración: si falla un tema, se revisa su índice y documento específico.
