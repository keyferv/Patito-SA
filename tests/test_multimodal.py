from __future__ import annotations

from unittest.mock import MagicMock, patch

from langchain_core.messages import HumanMessage

from app.multimodal import (
    _construir_mensaje_multimodal,
    _imagen_a_data_url,
    analizar_imagen,
)


class TestImagenADataURL:
    def test_codifica_bytes_png(self) -> None:
        data_url = _imagen_a_data_url(b"\x89PNG\r\n\x1a\n", "image/png")
        assert data_url.startswith("data:image/png;base64,")
        assert len(data_url) > len("data:image/png;base64,")

    def test_codifica_bytes_jpeg(self) -> None:
        data_url = _imagen_a_data_url(b"\xff\xd8\xff\xe0", "image/jpeg")
        assert data_url.startswith("data:image/jpeg;base64,")

    def test_codifica_bytes_vacios(self) -> None:
        data_url = _imagen_a_data_url(b"", "image/png")
        assert data_url == "data:image/png;base64,"


class TestConstruirMensajeMultimodal:
    def test_construye_human_message_con_texto_e_imagen(self) -> None:
        image_bytes = b"\x89PNG\r\n\x1a\n"
        msg = _construir_mensaje_multimodal(image_bytes, "image/png", "Describe esto.")
        assert isinstance(msg, HumanMessage)
        assert isinstance(msg.content, list)
        assert len(msg.content) == 2
        assert msg.content[0] == {"type": "text", "text": "Describe esto."}
        assert isinstance(msg.content[1], dict)
        assert msg.content[1]["type"] == "image_url"
        assert msg.content[1]["image_url"].startswith("data:image/png;base64,")

    def test_la_imagen_codificada_esta_dentro_del_mensaje(self) -> None:
        image_bytes = b"fake-image-data"
        msg = _construir_mensaje_multimodal(image_bytes, "image/jpeg", "Prompt")
        data_url = msg.content[1]["image_url"]
        assert "ZmFrZS1pbWFnZS1kYXRh" in data_url


class TestAnalizarImagen:
    def test_devuelve_error_si_bytes_estan_vacios(self) -> None:
        result = analizar_imagen(b"", "image/png")
        assert "no se recibió" in result.lower()

    def test_llama_a_gemini_y_retorna_contenido(self) -> None:
        mock_llm = MagicMock()
        mock_result = MagicMock()
        mock_result.content = "En la imagen se observa un monitor con pantalla azul."
        mock_llm.invoke.return_value = mock_result

        with patch("app.multimodal.settings") as mock_settings:
            mock_settings.require_google_api_key = MagicMock()
            mock_settings.gemini_llm_model = "gemini-2.0-flash"
            with patch("app.multimodal.ChatGoogleGenerativeAI", return_value=mock_llm):
                result = analizar_imagen(b"\x89PNG", "image/png")

        assert "monitor" in result
        mock_llm.invoke.assert_called_once()

    def test_usa_instruccion_personalizada_cuando_se_provee(self) -> None:
        mock_llm = MagicMock()
        mock_result = MagicMock()
        mock_result.content = "OK"
        mock_llm.invoke.return_value = mock_result

        with patch("app.multimodal.settings") as mock_settings:
            mock_settings.require_google_api_key = MagicMock()
            mock_settings.gemini_llm_model = "gemini-2.0-flash"
            with patch("app.multimodal.ChatGoogleGenerativeAI", return_value=mock_llm):
                analizar_imagen(b"\x89PNG", "image/png", instruccion="Instrucción custom")

        called_messages = mock_llm.invoke.call_args[0][0]
        assert called_messages[0].content[0]["text"] == "Instrucción custom"

    def test_captura_excepcion_y_retorna_error(self) -> None:
        with patch("app.multimodal.settings") as mock_settings:
            mock_settings.require_google_api_key = MagicMock()
            mock_settings.gemini_llm_model = "gemini-2.0-flash"
            with patch(
                "app.multimodal.ChatGoogleGenerativeAI",
                side_effect=RuntimeError("API caída"),
            ):
                result = analizar_imagen(b"\x89PNG", "image/png")
        assert "Error al analizar" in result
        assert "API caída" in result

    def test_maneja_resultado_sin_contenido_texto(self) -> None:
        mock_llm = MagicMock()
        mock_result = MagicMock(spec=[], content=["parte 1", "parte 2"])
        mock_llm.invoke.return_value = mock_result

        with patch("app.multimodal.settings") as mock_settings:
            mock_settings.require_google_api_key = MagicMock()
            mock_settings.gemini_llm_model = "gemini-2.0-flash"
            with patch("app.multimodal.ChatGoogleGenerativeAI", return_value=mock_llm):
                result = analizar_imagen(b"\x89PNG", "image/png")

        assert "parte 1" in result
        assert "parte 2" in result

    def test_extrae_texto_de_partes_tipo_dict(self) -> None:
        mock_llm = MagicMock()
        mock_result = MagicMock(
            spec=[],
            content=[
                {
                    "type": "text",
                    "text": "La imagen muestra un error 503 en facturación.",
                    "extras": {"signature": "abc"},
                }
            ],
        )
        mock_llm.invoke.return_value = mock_result

        with patch("app.multimodal.settings") as mock_settings:
            mock_settings.require_google_api_key = MagicMock()
            mock_settings.gemini_llm_model = "gemini-2.0-flash"
            with patch("app.multimodal.ChatGoogleGenerativeAI", return_value=mock_llm):
                result = analizar_imagen(b"\x89PNG", "image/png")

        assert result == "La imagen muestra un error 503 en facturación."
        assert "extras" not in result
