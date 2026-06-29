# Flujo RAG

El flujo RAG permite responder usando documentos internos en lugar de conocimiento general del modelo.

## Documentos fuente

| Agente | Archivo fuente | Índice generado |
|--------|----------------|-----------------|
| Infraestructura | `data/catalogo_servicios.txt` | `vectorstores/infraestructura` |
| Seguridad | `data/politica_seguridad.txt` | `vectorstores/seguridad` |
| Incidentes | `data/gestion_incidentes_sla.txt` | `vectorstores/incidentes` |

## Generación de índices

Comando:

```powershell
python -m app.rag.build_indexes
```

Qué ocurre internamente:

1. Se valida `GOOGLE_API_KEY`.
2. Se crea el modelo de embeddings configurado.
3. Se lee cada archivo de `data/`.
4. El texto se divide en chunks con overlap.
5. Cada chunk recibe metadata de fuente, agente e identificador.
6. Se elimina el índice anterior del dominio.
7. Se crea una colección Chroma nueva.

## Consulta RAG

Cuando un usuario pregunta:

1. El orquestador identifica el dominio.
2. El agente carga su retriever.
3. Chroma recupera los chunks más relevantes.
4. El agente arma un prompt con la pregunta y el contexto.
5. Gemini responde usando ese contexto.
6. La interfaz muestra respuesta y fuentes.

## Parámetros importantes

| Variable | Uso |
|----------|-----|
| `GEMINI_EMBEDDING_MODEL` | Modelo usado para crear embeddings. |
| `GEMINI_LLM_MODEL` | Modelo usado para generar respuestas. |
| `CHUNK_SIZE` | Tamaño máximo aproximado de cada chunk. |
| `CHUNK_OVERLAP` | Solapamiento entre chunks. |
| `RETRIEVER_K` | Cantidad de chunks recuperados por consulta. |

## Cuándo regenerar índices

Regenerá índices cuando:

- Cambie cualquier archivo dentro de `data/`.
- Cambie `GEMINI_EMBEDDING_MODEL`.
- Se borre o corrompa una carpeta dentro de `vectorstores/`.

## Regla de respuesta insuficiente

Si no hay información suficiente, el sistema debe responder exactamente:

```text
No encontré información suficiente en la base documental proporcionada.
```

Esta regla evita inventar respuestas fuera de los documentos.
