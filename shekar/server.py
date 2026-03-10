#!/usr/bin/env python3
"""
Shekar NLP - Web UI Server

Serves the static UI and exposes REST API endpoints for:
  POST /api/normalizer    — text normalization
  POST /api/tokenizer     — word tokenization
  POST /api/stemmer       — stemming (word → stem pairs)
  POST /api/ner           — named-entity recognition
  POST /api/pos           — part-of-speech tagging
  POST /api/spellchecker  — spell checking / correction
"""

import json
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
STATIC_DIR = DATA_DIR / "statics"
HOST = "localhost"


_normalizer = None
_word_tokenizer = None
_stemmer = None
_ner = None
_pos = None
_spell_checker = None


def get_normalizer():
    global _normalizer
    if _normalizer is None:
        from shekar import Normalizer

        _normalizer = Normalizer()
    return _normalizer


def get_word_tokenizer():
    global _word_tokenizer
    if _word_tokenizer is None:
        from shekar import WordTokenizer

        _word_tokenizer = WordTokenizer()
    return _word_tokenizer


def get_stemmer():
    global _stemmer
    if _stemmer is None:
        from shekar import Stemmer

        _stemmer = Stemmer()
    return _stemmer


def get_ner():
    global _ner
    if _ner is None:
        from shekar import NER

        _ner = NER()
    return _ner


def get_pos():
    global _pos
    if _pos is None:
        from shekar import POSTagger

        _pos = POSTagger()
    return _pos


def get_spell_checker():
    global _spell_checker
    if _spell_checker is None:
        from shekar import SpellChecker

        _spell_checker = SpellChecker()
    return _spell_checker


class ShekarHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/" or path == "/index.html":
            self._serve_file(STATIC_DIR / "index.html", "text/html; charset=utf-8")
        else:
            # Try statics/ first, then fall back to data/ (e.g. for fonts/)
            candidate = STATIC_DIR / path.lstrip("/")
            if not candidate.is_file():
                candidate = DATA_DIR / path.lstrip("/")
            if candidate.is_file():
                mime = self._mime(candidate.suffix)
                self._serve_file(candidate, mime)
            else:
                self._send_json({"error": "Not found"}, status=404)

    def do_POST(self):
        routes = {
            "/api/normalizer": self._handle_normalize,
            "/api/tokenizer": self._handle_tokenize,
            "/api/stemmer": self._handle_stem,
            "/api/ner": self._handle_ner,
            "/api/pos": self._handle_pos,
            "/api/spellchecker": self._handle_spellcheck,
        }
        handler = routes.get(self.path)
        if handler is None:
            self._send_json({"error": "Not found"}, status=404)
            return

        body = self._read_json()
        if body is None:
            return
        text = body.get("text", "").strip()
        if not text:
            self._send_json({"error": "متن ورودی خالی است."}, status=400)
            return

        try:
            handler(text)
        except Exception as exc:
            self._send_json({"error": str(exc)}, status=500)

    def _handle_normalize(self, text: str):
        t0 = time.perf_counter()
        result = get_normalizer().normalize(text)
        elapsed = time.perf_counter() - t0
        self._send_json({"result": result, "elapsed_ms": round(elapsed * 1000, 1)})

    def _handle_tokenize(self, text: str):
        t0 = time.perf_counter()
        tokens = list(get_word_tokenizer()(text))
        elapsed = time.perf_counter() - t0
        self._send_json(
            {
                "tokens": tokens,
                "count": len(tokens),
                "elapsed_ms": round(elapsed * 1000, 1),
            }
        )

    def _handle_stem(self, text: str):
        t0 = time.perf_counter()
        stemmer = get_stemmer()
        words = list(get_word_tokenizer()(text))
        stems = [[w, stemmer(w)] for w in words]
        elapsed = time.perf_counter() - t0
        self._send_json({"stems": stems, "elapsed_ms": round(elapsed * 1000, 1)})

    def _handle_ner(self, text: str):
        t0 = time.perf_counter()
        entities = get_ner().transform(text)
        elapsed = time.perf_counter() - t0
        self._send_json(
            {
                "entities": [list(e) for e in entities],
                "elapsed_ms": round(elapsed * 1000, 1),
            }
        )

    def _handle_pos(self, text: str):
        t0 = time.perf_counter()
        tags = get_pos().transform(text)
        elapsed = time.perf_counter() - t0
        self._send_json(
            {"tags": [list(t) for t in tags], "elapsed_ms": round(elapsed * 1000, 1)}
        )

    def _handle_spellcheck(self, text: str):
        t0 = time.perf_counter()
        checker = get_spell_checker()
        corrected = checker.correct(text)
        elapsed = time.perf_counter() - t0
        self._send_json(
            {"corrected": corrected, "elapsed_ms": round(elapsed * 1000, 1)}
        )

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            self._send_json({"error": "Empty request body"}, status=400)
            return None
        raw = self.rfile.read(length)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON"}, status=400)
            return None

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _serve_file(self, path: Path, mime: str):
        try:
            data = path.read_bytes()
        except FileNotFoundError:
            self._send_json({"error": "File not found"}, status=404)
            return
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):  # noqa: N802
        print(f"  {self.address_string()} — {fmt % args}")

    @staticmethod
    def _mime(suffix: str) -> str:
        return {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".json": "application/json; charset=utf-8",
            ".png": "image/png",
            ".svg": "image/svg+xml",
            ".ico": "image/x-icon",
            ".ttf": "font/ttf",
            ".woff": "font/woff",
            ".woff2": "font/woff2",
        }.get(suffix.lower(), "application/octet-stream")


def serve(port: int = 8080):
    if not STATIC_DIR.is_dir():
        print(f"[error] Static directory not found: {STATIC_DIR}", file=sys.stderr)
        sys.exit(1)

    server = HTTPServer((HOST, port), ShekarHandler)
    url = f"http://{HOST}:{port}"
    print(f"Shekar NLP UI  →  {url}")
    print("Press Ctrl+C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":  # pragma: no cover
    serve()
