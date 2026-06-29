# Instalación y uso de PatitoDesk IA

Esta guía es para levantar el proyecto desde cero sin adivinar comandos.

## Carpeta correcta

Todos los comandos se ejecutan desde:

```text
C:\Users\Usuario\Documents\Patito-SA
```

Si estás en otra carpeta, vas a tener errores de imports, archivos no encontrados o índices vacíos.

## Requisitos

- Python 3.11 recomendado.
- API key de Google AI Studio.
- Archivo `.env` creado desde `.env.example`.
- Dependencias instaladas con pip o uv.
- Índices Chroma generados antes de abrir Streamlit.

## Opción 1: PowerShell con pip

```powershell
cd C:\Users\Usuario\Documents\Patito-SA
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
python -m app.rag.build_indexes
python -m streamlit run app/streamlit_app.py
```

## Opción 2: CMD con pip

```bat
cd /d C:\Users\Usuario\Documents\Patito-SA
python --version
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
notepad .env
python -m app.rag.build_indexes
python -m streamlit run app/streamlit_app.py
```

## Opción 3: PowerShell con uv

Instalar uv:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Crear entorno, instalar y ejecutar:

```powershell
cd C:\Users\Usuario\Documents\Patito-SA
uv venv --python 3.11
.\.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
uv run python -m app.rag.build_indexes
uv run streamlit run app/streamlit_app.py
```

## Opción 4: CMD con uv

Instalar uv:

```bat
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Crear entorno, instalar y ejecutar:

```bat
cd /d C:\Users\Usuario\Documents\Patito-SA
uv venv --python 3.11
.venv\Scripts\activate.bat
uv pip install -r requirements.txt
copy .env.example .env
notepad .env
uv run python -m app.rag.build_indexes
uv run streamlit run app/streamlit_app.py
```

## Configurar .env

El archivo `.env` debe quedar así, cambiando solo la API key:

```env
GOOGLE_API_KEY=tu_api_key_aqui
GEMINI_LLM_MODEL=gemini-3.1-flash-lite
GEMINI_EMBEDDING_MODEL=gemini-embedding-2
CHUNK_SIZE=800
CHUNK_OVERLAP=120
RETRIEVER_K=3
```

No subas `.env` a GitHub ni lo pegues en chats.

## Ejecutar después de instalar

PowerShell:

```powershell
cd C:\Users\Usuario\Documents\Patito-SA
.\.venv\Scripts\Activate.ps1
python -m streamlit run app/streamlit_app.py
```

CMD:

```bat
cd /d C:\Users\Usuario\Documents\Patito-SA
.venv\Scripts\activate.bat
python -m streamlit run app/streamlit_app.py
```

uv sin activar manualmente:

```powershell
cd C:\Users\Usuario\Documents\Patito-SA
uv run streamlit run app/streamlit_app.py
```

## Uso básico

1. Abrí la URL que muestra Streamlit.
2. Preguntá sobre catálogo de servicios, seguridad o incidentes.
3. Revisá las fuentes mostradas por la app.
4. Para tickets, escribí la solicitud con todos los datos requeridos.
5. Confirmá solo cuando la app indique que el ticket está completo.

## Preguntas de prueba

Usá el archivo:

```text
examples/preguntas_prueba.md
```

Casos que conviene probar:

- Una pregunta de infraestructura.
- Una pregunta de seguridad.
- Una pregunta de incidentes.
- Una pregunta mixta de incidentes y seguridad.
- Un ticket incompleto.
- Un ticket completo.
- Una pregunta fuera de alcance.

## Regenerar índices

Regenerá índices si cambia algún archivo en `data/` o si cambia `GEMINI_EMBEDDING_MODEL`.

```powershell
python -m app.rag.build_indexes
```

Con uv:

```powershell
uv run python -m app.rag.build_indexes
```

## Ejecutar pruebas

```powershell
pytest -q
```

Con uv:

```powershell
uv run pytest -q
```

## Problemas comunes

### No module named app

Causa probable: ejecutaste el comando desde una carpeta incorrecta.

Solución:

```powershell
cd C:\Users\Usuario\Documents\Patito-SA
python -m streamlit run app/streamlit_app.py
```

### Falta GOOGLE_API_KEY

Causa probable: no creaste `.env` o no agregaste la API key.

Solución:

```powershell
Copy-Item .env.example .env
notepad .env
```

### No responde con documentos

Causa probable: faltan los índices Chroma.

Solución:

```powershell
python -m app.rag.build_indexes
```

### Cambié documentos y responde lo anterior

Causa probable: los índices quedaron viejos.

Solución: regenerá índices.

```powershell
python -m app.rag.build_indexes
```

### Error con PowerShell al activar entorno

Si PowerShell bloquea scripts, usá CMD con:

```bat
.venv\Scripts\activate.bat
```

O ejecutá con uv sin activar manualmente:

```powershell
uv run streamlit run app/streamlit_app.py
```

## Archivos importantes

```text
README.md                         Resumen principal del proyecto
docs/instalacion-y-uso.md         Esta guía completa
.env.example                      Plantilla de variables de entorno
requirements.txt                  Dependencias Python
app/streamlit_app.py              Interfaz Streamlit
app/rag/build_indexes.py          Generador de índices Chroma
outputs/registro_tickets.txt      Tickets guardados localmente
examples/preguntas_prueba.md      Casos de prueba manual
```
