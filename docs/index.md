# Documentación de PatitoDesk IA

Documentación técnica y operativa del prototipo. Cada archivo cubre un tema específico para que se pueda consultar por separado.

| Documento | Contenido |
|-----------|-----------|
| [proyecto.md](proyecto.md) | Objetivo, alcance y límites del sistema. |
| [arquitectura.md](arquitectura.md) | Arquitectura, capas y flujos principales. |
| [componentes.md](componentes.md) | Qué hace cada carpeta y módulo importante. |
| [flujo-rag.md](flujo-rag.md) | Generación de índices y flujo de respuesta documental. |
| [flujo-tickets.md](flujo-tickets.md) | Validación, confirmación y registro de tickets. |
| [configuracion-y-datos.md](configuracion-y-datos.md) | Variables de entorno, datos fuente y archivos generados. |
| [pruebas-y-validacion.md](pruebas-y-validacion.md) | Pruebas automatizadas y validación manual. |
| [instalacion-y-uso.md](instalacion-y-uso.md) | Instalación completa, ejecución y problemas comunes. |

PatitoDesk IA es un prototipo académico de mesa de ayuda para TI. Usa Streamlit como interfaz, LangChain como capa de integración, Gemini como modelo LLM y de embeddings, Chroma como vector store local, y un orquestador que decide qué agente debe responder cada consulta.
