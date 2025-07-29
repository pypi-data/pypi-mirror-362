import httpx
import asyncio
from typing import Sequence, AsyncIterator
from agentbox.engine.abc import EngineAdapter
from agentbox.models.chat import ChatMessage


class OllamaEngine(EngineAdapter):
    def __init__(self, host: str = "http://localhost:11434", model: str | None = None):
        self.host = host.rstrip("/")
        self.model = model or "llama3.1:8b"

    async def a_generate(self, messages: Sequence[ChatMessage]) -> str:
        url = f"{self.host}/api/chat"
        payload = {
            "model": self.model,
            "messages": [m.model_dump(exclude_none=True) for m in messages],
            "stream": False,
        }
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            return r.json()["message"]["content"]

    async def a_stream(self, messages: list[ChatMessage]) -> AsyncIterator[str]:
        for char in "pong":
            yield char
            await asyncio.sleep(0.01)
