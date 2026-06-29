# Configuración y datos

El proyecto depende de variables de entorno, documentos base y archivos generados localmente.

## Variables de entorno

El archivo `.env.example` muestra la configuración esperada:

```env
GOOGLE_API_KEY=tu_api_key_aqui
GEMINI_LLM_MODEL=gemini-3.1-flash-lite
GEMINI_EMBEDDING_MODEL=gemini-embedding-2
CHUNK_SIZE=800
CHUNK_OVERLAP=120
RETRIEVER_K=3
```

## Variables principales

| Variable | Obligatoria | Descripción |
|----------|-------------|-------------|
| `GOOGLE_API_KEY` | Sí | API key de Google AI Studio. |
| `GEMINI_LLM_MODEL` | No | Modelo usado para redactar respuestas. |
| `GEMINI_EMBEDDING_MODEL` | No | Modelo usado para embeddings. |
| `CHUNK_SIZE` | No | Tamaño de cada chunk documental. |
| `CHUNK_OVERLAP` | No | Solapamiento entre chunks. |
| `RETRIEVER_K` | No | Cantidad de chunks recuperados. |

## Archivos de datos

| Archivo | Uso |
|---------|-----|
| `data/catalogo_servicios.txt` | Base del agente de infraestructura. |
| `data/politica_seguridad.txt` | Base del agente de seguridad. |
| `data/gestion_incidentes_sla.txt` | Base del agente de incidentes. |

## Archivos generados

| Ruta | Se sube a Git | Motivo |
|------|---------------|--------|
| `vectorstores/` | No, salvo `.gitkeep` | Contiene índices Chroma regenerables. |
| `outputs/registro_tickets.txt` | No | Puede contener datos internos de tickets. |
| `.env` | No | Contiene credenciales. |
| `.venv/` | No | Entorno local de Python. |

## Reglas de seguridad

- No subir `.env`.
- No pegar API keys en documentación, issues o commits.
- No subir tickets reales generados localmente.
- No subir vectorstores generados; se regeneran con un comando.

## Comando para regenerar datos derivados

```powershell
python -m app.rag.build_indexes
```

Con uv:

```powershell
uv run python -m app.rag.build_indexes
```
