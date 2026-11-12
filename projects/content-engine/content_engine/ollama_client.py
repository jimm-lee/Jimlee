"""Minimal Ollama chat client that asks for JSON matching a schema."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Protocol

DEFAULT_HOST = "http://127.0.0.1:11434"
DEFAULT_MODEL = "llama3.2:3b"
REQUEST_TIMEOUT_S = 900


class OllamaError(RuntimeError):
    """Raised when Ollama is unreachable or returns something unusable."""


class JsonModel(Protocol):
    """Anything that can answer a prompt with JSON (the real client or a test fake)."""

    def ask_json(self, system: str, prompt: str, schema: dict[str, Any]) -> Any: ...


class OllamaClient:
    def __init__(
        self, model: str = DEFAULT_MODEL, host: str = DEFAULT_HOST, temperature: float = 0.8
    ) -> None:
        self.model = model
        self.host = host.rstrip("/")
        self.temperature = temperature

    def ask_json(self, system: str, prompt: str, schema: dict[str, Any]) -> Any:
        """Send one chat turn and return the reply parsed as JSON.

        Ollama's structured outputs constrain the reply to `schema`, which keeps
        small local models from drifting into prose.
        """
        body = {
            "model": self.model,
            "stream": False,
            "format": schema,
            "options": {"temperature": self.temperature},
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        }
        request = urllib.request.Request(
            f"{self.host}/api/chat",
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_S) as response:
                payload = json.load(response)
        except urllib.error.URLError as exc:
            raise OllamaError(
                f"Could not reach Ollama at {self.host} ({exc}). Is `ollama serve` running?"
            ) from exc
        content = payload.get("message", {}).get("content", "")
        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            raise OllamaError(f"Model returned invalid JSON: {content[:200]!r}") from exc
