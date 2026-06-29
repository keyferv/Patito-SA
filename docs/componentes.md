# Componentes del proyecto

Este documento explica qué hace cada parte importante del repositorio.

## Estructura principal

| Ruta | Responsabilidad |
|------|-----------------|
| `app/` | Código principal de la aplicación. |
| `data/` | Documentos base usados por RAG. |
| `docs/` | Documentación técnica y operativa. |
| `examples/` | Preguntas de prueba manual. |
| `outputs/` | Salidas locales generadas, como tickets. |
| `tests/` | Pruebas automatizadas. |
| `vectorstores/` | Índices Chroma generados localmente. |
| `.env.example` | Plantilla de configuración. |
| `requirements.txt` | Dependencias Python. |

## app/config.py

Centraliza rutas, variables de entorno y definición de bases de conocimiento.

Define:

- `BASE_DIR`, `DATA_DIR`, `VECTORSTORE_DIR`, `OUTPUTS_DIR`.
- `TICKET_REGISTRY_PATH`.
- `INSUFFICIENT_INFO_MESSAGE`.
- `Settings`, con modelos Gemini y parámetros RAG.
- `KNOWLEDGE_BASES`, con un documento e índice por agente.

## app/streamlit_app.py

Es la entrada visual del sistema.

Responsabilidades:

- Configurar la página de Streamlit.
- Mantener historial de conversación en `st.session_state`.
- Enviar preguntas al orquestador.
- Mostrar respuesta, agentes participantes y fuentes.
- Guardar un ticket pendiente hasta que el usuario confirme.

## app/orchestrator/router.py

Decide qué agente debe responder.

Responsabilidades:

- Detectar intención usando palabras clave.
- Ejecutar uno o varios agentes según la pregunta.
- Ejecutar el agente de acción cuando hay intención de ticket.
- Consolidar respuestas, fuentes, advertencias y borradores de ticket.

## app/agents/base_rag_agent.py

Contiene la lógica común de los agentes RAG.

Responsabilidades:

- Cargar el retriever de Chroma.
- Recuperar documentos relevantes.
- Construir contexto para el LLM.
- Invocar Gemini con temperatura cero.
- Convertir respuestas estructuradas del modelo a texto plano.
- Devolver `AgentResponse` con respuesta y fuentes.

## Agentes por dominio

| Archivo | Dominio | Documento usado |
|---------|---------|-----------------|
| `app/agents/infra_agent.py` | Infraestructura y servicios | `data/catalogo_servicios.txt` |
| `app/agents/security_agent.py` | Seguridad y accesos | `data/politica_seguridad.txt` |
| `app/agents/incident_agent.py` | Incidentes y SLA | `data/gestion_incidentes_sla.txt` |

Estos archivos son delgados. Solo instancian `RagAgent` con la base de conocimiento correcta.

## app/agents/action_agent.py

Maneja tickets.

Responsabilidades:

- Detectar si el ticket es de software o incidente.
- Extraer datos con patrones simples.
- Validar campos obligatorios.
- Preparar un borrador si los datos están completos.
- Registrar el ticket confirmado en archivo local.
- Exponer una `StructuredTool` opcional para integración LangChain.

## app/rag/build_indexes.py

Genera los índices vectoriales.

Responsabilidades:

- Leer cada documento en `data/`.
- Dividir texto en chunks.
- Crear embeddings con Gemini.
- Persistir cada colección en `vectorstores/`.
- Reemplazar índices anteriores cuando se regeneran.

## app/rag/vectorstores.py

Carga embeddings, Chroma y retrievers.

Responsabilidades:

- Crear `GoogleGenerativeAIEmbeddings`.
- Validar que exista el índice vectorial.
- Cargar la colección Chroma correcta.
- Devolver un retriever con `RETRIEVER_K`.

## app/schemas

Define modelos Pydantic para mantener contratos claros.

| Archivo | Modelos |
|---------|---------|
| `request.py` | `UserRequest` |
| `response.py` | `SourceChunk`, `AgentResponse`, `OrchestratorResponse` |
| `ticket.py` | `TicketDraft`, `TicketResult`, `TicketType` |

## app/utils

Contiene utilidades pequeñas.

| Archivo | Responsabilidad |
|---------|-----------------|
| `source_formatter.py` | Convierte documentos recuperados en fuentes visibles. |
| `ticket_writer.py` | Evita duplicados y escribe tickets en archivo local. |
