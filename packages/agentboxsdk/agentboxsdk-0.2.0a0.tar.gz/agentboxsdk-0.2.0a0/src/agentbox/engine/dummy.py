import asyncio
from typing import AsyncIterator
from agentbox.engine.abc import EngineAdapter
from agentbox.models.chat import ChatMessage


class DummyEngineAdapter(EngineAdapter):
    def __init__(self, model: str | None = None):  # Add constructor
        self.model = model  # Store model even if not used

    async def a_generate(self, messages: list[ChatMessage]) -> str:
        return "pong"

    async def a_stream(self, messages: list[ChatMessage]) -> AsyncIterator[str]:
        for char in "pong":
            yield char
            await asyncio.sleep(0.01)
