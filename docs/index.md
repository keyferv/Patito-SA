# Documentación de PatitoDesk IA

Esta carpeta organiza la documentación del proyecto en archivos pequeños. La idea es que una persona pueda entender el sistema sin leer todo el código primero.

## Lectura recomendada

1. `proyecto.md`: qué problema resuelve el proyecto y qué alcance tiene.
2. `arquitectura.md`: cómo se conectan la interfaz, el orquestador, los agentes, RAG y los tickets.
3. `componentes.md`: qué hace cada carpeta y archivo importante.
4. `flujo-rag.md`: cómo se generan índices y cómo se responden preguntas con documentos.
5. `flujo-tickets.md`: cómo funciona el registro de tickets.
6. `configuracion-y-datos.md`: variables de entorno, documentos base y archivos generados.
7. `pruebas-y-validacion.md`: cómo validar que el proyecto funciona.
8. `instalacion-y-uso.md`: comandos para instalar y ejecutar el proyecto.

## Resumen rápido

PatitoDesk IA es un prototipo académico de mesa de ayuda para TI. Usa Streamlit como interfaz, LangChain como capa de integración, Gemini como modelo LLM y de embeddings, Chroma como vector store local, y un orquestador que decide qué agente debe responder cada consulta.
