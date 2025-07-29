import asyncio
import os
from openai import AsyncOpenAI
from typing import AsyncIterator, Sequence

from agentbox.engine.abc import EngineAdapter
from agentbox.models.chat import ChatMessage


# TODO: Add checks for proper model name and API key
class OpenAIEngine(EngineAdapter):
    def __init__(self, model: str | None = None, api_key: str | None = None):
        self.model = model or "gpt-4o-mini"
        self.client = AsyncOpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    async def a_generate(self, messages: Sequence[ChatMessage]) -> str:
        resp = await self.client.chat.completions.create(
            model=self.model,
            messages=[m.model_dump(exclude_none=True) for m in messages],
        )
        return resp.choices[0].message.content

    async def a_stream(self, messages: list[ChatMessage]) -> AsyncIterator[str]:
        for char in "pong":
            yield char
            await asyncio.sleep(0.01)
