# Proyecto PatitoDesk IA

PatitoDesk IA es un prototipo académico de mesa de ayuda inteligente para el área de Tecnología de Patito S.A. El sistema responde consultas internas usando documentos controlados y permite preparar tickets locales cuando la solicitud cumple datos mínimos.

## Problema que resuelve

El área de TI necesita atender preguntas repetitivas sobre servicios, accesos e incidentes sin depender siempre de una persona. También necesita registrar solicitudes básicas de forma consistente.

El proyecto reduce ese trabajo mediante:

- Respuestas basadas en documentos internos.
- Separación de conocimiento por tema.
- Enrutamiento automático hacia agentes especializados.
- Validación mínima antes de registrar tickets.

## Alcance funcional

| Área | Qué cubre |
|------|-----------|
| Infraestructura y servicios | Catálogo de servicios, solicitudes de software, hardware y licencias. |
| Seguridad y accesos | Contraseñas, VPN, credenciales, permisos, MFA y acceso a información sensible. |
| Incidentes y SLA | Fallas, prioridades, escalamiento y tiempos de atención. |
| Tickets | Borradores de tickets de software o incidentes con confirmación antes de guardar. |

## Fuera de alcance

El prototipo no implementa:

- Autenticación de usuarios.
- Integración con un sistema real de tickets.
- Control real de permisos.
- Base de datos externa.
- Monitoreo de costos o trazabilidad productiva.
- Evaluación automática avanzada de calidad RAG.

## Decisión principal

El sistema usa tres bases vectoriales separadas, una por dominio. Esto evita mezclar políticas, servicios e incidentes en una sola búsqueda. Es más simple de explicar, revisar y depurar.

## Resultado esperado

Al ejecutar la aplicación, el usuario puede escribir una consulta en Streamlit. El sistema identifica el tema, consulta el agente adecuado, responde con base documental y muestra las fuentes usadas.
