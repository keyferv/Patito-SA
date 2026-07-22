# Pruebas y validación

Este documento explica cómo validar que el proyecto funciona después de instalarlo o modificarlo.

## Pruebas automatizadas

Comando con pip o entorno activado:

```powershell
pytest -q
```

Comando con uv:

```powershell
uv run pytest -q
```

## Qué cubren las pruebas

| Archivo | Qué valida |
|---------|------------|
| `tests/conftest.py` | Agrega la raíz del proyecto a `sys.path` para que los imports funcionen en cualquier entorno. |
| `tests/test_router.py` | Enrutamiento de preguntas, respuesta fuera de alcance y normalización de contenido del LLM. |
| `tests/test_ticket_validation.py` | Validación de tickets incompletos, completos, confirmación y duplicados. |
| `tests/test_monitoring.py` | Conteo de archivos en directorios, etiquetas de estado, y verificación de salud de bases de conocimiento configuradas. |
| `tests/test_multimodal.py` | Codificación base64 de imágenes, construcción de mensajes multimodales, llamado a Gemini, extracción de texto desde dict, manejo de errores y respuesta con instrucción personalizada. |

## Validación manual recomendada

Usá `examples/preguntas_prueba.md` y probá:

1. Una pregunta de infraestructura.
2. Una pregunta de seguridad.
3. Una pregunta de incidentes.
4. Una pregunta mixta.
5. Una solicitud de ticket incompleta.
6. Una solicitud de ticket completa con confirmación.
7. Una pregunta fuera de alcance.
8. Subir una imagen de prueba (por ejemplo, una captura de pantalla con un error 503) en el expander "Análisis multimodal de imágenes" y verificar que el análisis describe el contenido sin inventar diagnósticos.

## Resultado esperado

- Las preguntas dentro del alcance deben responder desde documentos.
- La app debe mostrar fuentes recuperadas.
- Las preguntas fuera de alcance deben usar el mensaje de información insuficiente.
- Los tickets incompletos no deben registrarse.
- Los tickets completos deben esperar confirmación antes de escribirse.

## Advertencia sobre Python

El proyecto recomienda Python 3.11. En Python 3.14 las pruebas pueden pasar, pero algunas dependencias de LangChain o Pydantic pueden mostrar warnings de compatibilidad.
