from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Sequence, AsyncIterator, Iterator

from agentbox.models.chat import ChatMessage
import asyncio


class EngineAdapter(ABC):
    # ─────────────── generic completion ─────────────── #
    @abstractmethod
    async def a_generate(self, messages: Sequence[ChatMessage]) -> str: ...

    def generate(self, messages: Sequence[ChatMessage]) -> str:
        return asyncio.run(self.a_generate(messages))

    # ────────────────── streaming mode ───────────────── #
    @abstractmethod
    async def a_stream(self, messages: Sequence[ChatMessage]) -> AsyncIterator[str]:
        """Override for true streaming; default falls back to one big chunk."""
        yield await self.a_generate(messages)

    def stream(self, messages: Sequence[ChatMessage]) -> Iterator[str]:
        """Sync wrapper over the async generator."""
        async_gen = self.a_stream(messages)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            while True:
                try:
                    chunk = loop.run_until_complete(async_gen.__anext__())
                except StopAsyncIteration:
                    break
                yield chunk
        finally:
            loop.run_until_complete(async_gen.aclose())
            loop.close()
