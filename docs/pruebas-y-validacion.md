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
| `tests/test_router.py` | Enrutamiento de preguntas, respuesta fuera de alcance y normalización de contenido del LLM. |
| `tests/test_ticket_validation.py` | Validación de tickets incompletos, completos, confirmación y duplicados. |

## Validación manual recomendada

Usá `examples/preguntas_prueba.md` y probá:

1. Una pregunta de infraestructura.
2. Una pregunta de seguridad.
3. Una pregunta de incidentes.
4. Una pregunta mixta.
5. Una solicitud de ticket incompleta.
6. Una solicitud de ticket completa con confirmación.
7. Una pregunta fuera de alcance.

## Resultado esperado

- Las preguntas dentro del alcance deben responder desde documentos.
- La app debe mostrar fuentes recuperadas.
- Las preguntas fuera de alcance deben usar el mensaje de información insuficiente.
- Los tickets incompletos no deben registrarse.
- Los tickets completos deben esperar confirmación antes de escribirse.

## Advertencia sobre Python

El proyecto recomienda Python 3.11. En Python 3.14 las pruebas pueden pasar, pero algunas dependencias de LangChain o Pydantic pueden mostrar warnings de compatibilidad.
