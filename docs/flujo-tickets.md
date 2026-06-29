# Flujo de tickets

El agente de acción no registra cualquier texto. Primero valida datos obligatorios y luego espera confirmación del usuario.

## Tipos de ticket

| Tipo | Cuándo se detecta |
|------|-------------------|
| Software | Solicitudes de instalación, software, versión, motivo o aprobación. |
| Incidente | Palabras relacionadas con incidente, caída, falla, error, facturación o prioridad. |

## Campos obligatorios

Solicitud de software:

| Campo interno | Campo mostrado |
|---------------|----------------|
| `software` | software |
| `version` | versión |
| `motivo` | motivo |
| `approver` | jefe que aprueba |

Incidente:

| Campo interno | Campo mostrado |
|---------------|----------------|
| `system_affected` | sistema afectado |
| `description` | descripción |
| `priority` | prioridad |

## Flujo completo

1. El usuario pide registrar o crear un ticket.
2. El orquestador activa el agente de acción.
3. El agente detecta tipo de ticket.
4. El agente intenta extraer campos desde el texto.
5. Si faltan datos, devuelve un mensaje con campos faltantes.
6. Si todos los datos están completos, crea un borrador.
7. Streamlit muestra el borrador y espera confirmación.
8. Al confirmar, se escribe el ticket en `outputs/registro_tickets.txt`.

## Control de duplicados

El sistema genera una firma con el tipo de ticket y sus datos normalizados. Esa firma permite evitar registrar dos veces el mismo ticket.

## Persistencia

Los tickets se guardan localmente en:

```text
outputs/registro_tickets.txt
```

Ese archivo está ignorado por Git porque puede contener información operativa interna.

## Limitación importante

La extracción de datos usa patrones simples con expresiones regulares. Es suficiente para el prototipo académico, pero en producción convendría usar extracción estructurada con validación más robusta.
