from __future__ import annotations

import base64
from typing import Optional

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import settings

PROMPT_POR_DEFECTO = (
    "Analiza esta imagen de manera concisa. "
    "Describe qué se observa y menciona si parece estar relacionada con un caso "
    "de soporte de TI (infraestructura, seguridad o incidente). "
    "No afirmes diagnósticos ni hagas OCR si la imagen no es clara."
)


def _imagen_a_data_url(image_bytes: bytes, mime_type: str) -> str:
    """Codifica bytes de imagen como data URL base64."""
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def _construir_mensaje_multimodal(
    image_bytes: bytes, mime_type: str, prompt_text: str
) -> HumanMessage:
    """Construye un HumanMessage multimodal con texto e imagen."""
    data_url = _imagen_a_data_url(image_bytes, mime_type)
    return HumanMessage(
        content=[
            {"type": "text", "text": prompt_text},
            {"type": "image_url", "image_url": data_url},
        ]
    )


def analizar_imagen(
    image_bytes: bytes,
    mime_type: str,
    instruccion: Optional[str] = None,
) -> str:
    """Envía una imagen a Gemini para análisis multimodal.

    Retorna texto plano con el análisis o un mensaje de error.
    """
    if not image_bytes:
        return "Error: no se recibió contenido de imagen."

    prompt_text = instruccion or PROMPT_POR_DEFECTO

    try:
        settings.require_google_api_key()
        llm = ChatGoogleGenerativeAI(
            model=settings.gemini_llm_model,
            temperature=0,
            convert_system_message_to_human=True,
        )
        message = _construir_mensaje_multimodal(image_bytes, mime_type, prompt_text)
        result = llm.invoke([message])
        content = getattr(result, "content", str(result))
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            parts = []
            for part in content:
                if isinstance(part, dict) and part.get("type") == "text":
                    parts.append(str(part.get("text", "")))
                else:
                    parts.append(str(part))
            return "\n".join(p.strip() for p in parts if p.strip())
        return str(content).strip()
    except Exception as exc:
        return f"Error al analizar la imagen: {exc}"
