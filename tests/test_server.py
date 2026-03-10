import io
import json
from pathlib import Path
from unittest.mock import MagicMock, patch
import shekar.server as server_module
from shekar.server import ShekarHandler


def _make_handler(method: str, path: str, body: bytes | None = None) -> ShekarHandler:
    request = MagicMock()
    request.makefile = MagicMock()

    rfile = io.BytesIO(body or b"")
    wfile = io.BytesIO()

    headers = {
        "Content-Length": str(len(body)) if body else "0",
        "Content-Type": "application/json",
    }

    handler = ShekarHandler.__new__(ShekarHandler)
    handler.rfile = rfile
    handler.wfile = wfile
    handler.path = path
    handler.command = method
    handler.headers = headers
    handler.server = MagicMock()
    handler.client_address = ("127.0.0.1", 12345)
    handler.request_version = "HTTP/1.1"

    handler._status_code = None

    def fake_send_response(code, message=None):
        handler._status_code = code

    handler.send_response = fake_send_response
    handler.send_header = MagicMock()
    handler.end_headers = MagicMock()
    handler.log_message = MagicMock()

    return handler


def _get_response_json(handler: ShekarHandler) -> dict:
    handler.wfile.seek(0)
    return json.loads(handler.wfile.read().decode("utf-8"))


def _post(path: str, payload: dict) -> tuple[int, dict]:
    body = json.dumps(payload).encode("utf-8")
    handler = _make_handler("POST", path, body)
    handler.do_POST()
    return handler._status_code, _get_response_json(handler)


class TestMime:
    def test_html(self):
        assert ShekarHandler._mime(".html") == "text/html; charset=utf-8"

    def test_css(self):
        assert ShekarHandler._mime(".css") == "text/css; charset=utf-8"

    def test_js(self):
        assert ShekarHandler._mime(".js") == "application/javascript; charset=utf-8"

    def test_png(self):
        assert ShekarHandler._mime(".png") == "image/png"

    def test_ttf(self):
        assert ShekarHandler._mime(".ttf") == "font/ttf"

    def test_unknown_falls_back_to_octet_stream(self):
        assert ShekarHandler._mime(".xyz") == "application/octet-stream"

    def test_case_insensitive(self):
        assert ShekarHandler._mime(".HTML") == "text/html; charset=utf-8"
        assert ShekarHandler._mime(".PNG") == "image/png"


class TestPostErrors:
    def test_unknown_route_returns_404(self):
        status, body = _post("/api/unknown", {"text": "سلام"})
        assert status == 404
        assert "error" in body

    def test_empty_text_returns_400(self):
        status, body = _post("/api/normalizer", {"text": "   "})
        assert status == 400
        assert "error" in body

    def test_missing_text_key_returns_400(self):
        status, body = _post("/api/normalizer", {})
        assert status == 400
        assert "error" in body

    def test_empty_body_returns_400(self):
        handler = _make_handler("POST", "/api/normalizer", b"")
        handler.do_POST()
        assert handler._status_code == 400

    def test_invalid_json_returns_400(self):
        handler = _make_handler("POST", "/api/normalizer", b"not json")
        handler.do_POST()
        assert handler._status_code == 400
        body = _get_response_json(handler)
        assert "error" in body


class TestPostNormalizer:
    def test_returns_result_and_elapsed(self):
        mock_normalizer = MagicMock()
        mock_normalizer.normalize.return_value = "سلام دنیا"

        with patch.object(
            server_module, "get_normalizer", return_value=mock_normalizer
        ):
            status, body = _post("/api/normalizer", {"text": "سلام دنیا"})

        assert status == 200
        assert body["result"] == "سلام دنیا"
        assert "elapsed_ms" in body
        mock_normalizer.normalize.assert_called_once_with("سلام دنیا")

    def test_exception_returns_500(self):
        mock_normalizer = MagicMock()
        mock_normalizer.normalize.side_effect = RuntimeError("boom")

        with patch.object(
            server_module, "get_normalizer", return_value=mock_normalizer
        ):
            status, body = _post("/api/normalizer", {"text": "سلام"})

        assert status == 500
        assert "error" in body


class TestPostTokenizer:
    def test_returns_tokens_and_count(self):
        mock_tokenizer = MagicMock(return_value=["سلام", "دنیا"])

        with patch.object(
            server_module, "get_word_tokenizer", return_value=mock_tokenizer
        ):
            status, body = _post("/api/tokenizer", {"text": "سلام دنیا"})

        assert status == 200
        assert body["tokens"] == ["سلام", "دنیا"]
        assert body["count"] == 2
        assert "elapsed_ms" in body


class TestPostStemmer:
    def test_returns_word_stem_pairs(self):
        mock_tokenizer = MagicMock(return_value=["کتاب‌ها", "خانه"])
        mock_stemmer = MagicMock(side_effect=lambda w: w.split("‌")[0])

        with (
            patch.object(
                server_module, "get_word_tokenizer", return_value=mock_tokenizer
            ),
            patch.object(server_module, "get_stemmer", return_value=mock_stemmer),
        ):
            status, body = _post("/api/stemmer", {"text": "کتاب‌ها خانه"})

        assert status == 200
        assert "stems" in body
        assert "elapsed_ms" in body
        for pair in body["stems"]:
            assert len(pair) == 2


class TestPostNER:
    def test_returns_entities(self):
        mock_ner = MagicMock()
        mock_ner.transform.return_value = [("تهران", "LOC"), ("علی", "PER")]

        with patch.object(server_module, "get_ner", return_value=mock_ner):
            status, body = _post("/api/ner", {"text": "علی در تهران است"})

        assert status == 200
        assert body["entities"] == [["تهران", "LOC"], ["علی", "PER"]]
        assert "elapsed_ms" in body


class TestPostPOS:
    def test_returns_tags(self):
        mock_pos = MagicMock()
        mock_pos.transform.return_value = [("سلام", "INTJ"), ("دنیا", "NOUN")]

        with patch.object(server_module, "get_pos", return_value=mock_pos):
            status, body = _post("/api/pos", {"text": "سلام دنیا"})

        assert status == 200
        assert body["tags"] == [["سلام", "INTJ"], ["دنیا", "NOUN"]]
        assert "elapsed_ms" in body


class TestPostSpellChecker:
    def test_returns_corrected_text(self):
        mock_checker = MagicMock()
        mock_checker.correct.return_value = "کتاب خوب"

        with patch.object(
            server_module, "get_spell_checker", return_value=mock_checker
        ):
            status, body = _post("/api/spellchecker", {"text": "کتاب خوب"})

        assert status == 200
        assert body["corrected"] == "کتاب خوب"
        assert "elapsed_ms" in body


class TestGetRoutes:
    def _get(self, path: str) -> tuple[int, bytes]:
        handler = _make_handler("GET", path)
        handler.do_GET()
        handler.wfile.seek(0)
        return handler._status_code, handler.wfile.read()

    def test_root_serves_index_html(self, tmp_path, monkeypatch):
        static_dir = tmp_path / "statics"
        static_dir.mkdir()
        (static_dir / "index.html").write_text("<html/>", encoding="utf-8")
        monkeypatch.setattr(server_module, "STATIC_DIR", static_dir)

        status, _ = self._get("/")
        assert status == 200

    def test_index_html_path_serves_index_html(self, tmp_path, monkeypatch):
        static_dir = tmp_path / "statics"
        static_dir.mkdir()
        (static_dir / "index.html").write_text("<html/>", encoding="utf-8")
        monkeypatch.setattr(server_module, "STATIC_DIR", static_dir)

        status, _ = self._get("/index.html")
        assert status == 200

    def test_existing_static_file_served(self, tmp_path, monkeypatch):
        static_dir = tmp_path / "statics"
        static_dir.mkdir()
        (static_dir / "styles.css").write_text("body{}", encoding="utf-8")
        monkeypatch.setattr(server_module, "STATIC_DIR", static_dir)
        monkeypatch.setattr(server_module, "DATA_DIR", tmp_path)

        status, _ = self._get("/styles.css")
        assert status == 200

    def test_missing_file_returns_404(self, tmp_path, monkeypatch):
        static_dir = tmp_path / "statics"
        static_dir.mkdir()
        monkeypatch.setattr(server_module, "STATIC_DIR", static_dir)
        monkeypatch.setattr(server_module, "DATA_DIR", tmp_path)

        status, body = self._get("/nonexistent.css")
        assert status == 404
        assert b"error" in body

    def test_data_dir_fallback_for_fonts(self, tmp_path, monkeypatch):
        static_dir = tmp_path / "statics"
        static_dir.mkdir()
        fonts_dir = tmp_path / "fonts"
        fonts_dir.mkdir()
        (fonts_dir / "test.ttf").write_bytes(b"\x00\x01\x02")
        monkeypatch.setattr(server_module, "STATIC_DIR", static_dir)
        monkeypatch.setattr(server_module, "DATA_DIR", tmp_path)

        status, _ = self._get("/fonts/test.ttf")
        assert status == 200


class TestServeFile:
    def test_file_not_found_returns_404(self):
        handler = _make_handler("GET", "/")
        with patch.object(Path, "read_bytes", side_effect=FileNotFoundError):
            handler._serve_file(Path("/fake/path.html"), "text/html")
        assert handler._status_code == 404
        handler.wfile.seek(0)
        body = json.loads(handler.wfile.read().decode("utf-8"))
        assert "error" in body


class TestLogMessage:
    def test_log_message_prints(self, capsys):
        handler = _make_handler("GET", "/")
        handler.address_string = MagicMock(return_value="127.0.0.1")
        ShekarHandler.log_message(handler, "%s %s", "GET", "/")
        captured = capsys.readouterr()
        assert "127.0.0.1" in captured.out
        assert "GET" in captured.out


class TestServe:
    def test_missing_static_dir_exits(self, tmp_path, monkeypatch):
        import pytest

        monkeypatch.setattr(server_module, "STATIC_DIR", tmp_path / "nonexistent")
        with pytest.raises(SystemExit) as exc_info:
            server_module.serve(port=19999)
        assert exc_info.value.code == 1

    def test_keyboard_interrupt_stops_server(self, tmp_path, monkeypatch):
        static_dir = tmp_path / "statics"
        static_dir.mkdir()
        monkeypatch.setattr(server_module, "STATIC_DIR", static_dir)

        mock_server = MagicMock()
        mock_server.serve_forever.side_effect = KeyboardInterrupt

        with patch("shekar.server.HTTPServer", return_value=mock_server):
            server_module.serve(port=19999)  # Should not raise


class TestLazySingletons:
    def _reset(self):
        server_module._normalizer = None
        server_module._word_tokenizer = None
        server_module._stemmer = None
        server_module._ner = None
        server_module._pos = None
        server_module._spell_checker = None

    def test_get_normalizer_returns_same_instance(self):
        self._reset()
        mock = MagicMock()
        with patch("shekar.Normalizer", return_value=mock):
            a = server_module.get_normalizer()
            b = server_module.get_normalizer()
        assert a is b

    def test_get_word_tokenizer_returns_same_instance(self):
        self._reset()
        mock = MagicMock()
        with patch("shekar.WordTokenizer", return_value=mock):
            a = server_module.get_word_tokenizer()
            b = server_module.get_word_tokenizer()
        assert a is b

    def test_get_stemmer_returns_same_instance(self):
        self._reset()
        mock = MagicMock()
        with patch("shekar.Stemmer", return_value=mock):
            a = server_module.get_stemmer()
            b = server_module.get_stemmer()
        assert a is b

    def test_get_ner_returns_same_instance(self):
        self._reset()
        mock = MagicMock()
        with patch("shekar.NER", return_value=mock):
            a = server_module.get_ner()
            b = server_module.get_ner()
        assert a is b

    def test_get_pos_returns_same_instance(self):
        self._reset()
        mock = MagicMock()
        with patch("shekar.POSTagger", return_value=mock):
            a = server_module.get_pos()
            b = server_module.get_pos()
        assert a is b

    def test_get_spell_checker_returns_same_instance(self):
        self._reset()
        mock = MagicMock()
        with patch("shekar.SpellChecker", return_value=mock):
            a = server_module.get_spell_checker()
            b = server_module.get_spell_checker()
        assert a is b
