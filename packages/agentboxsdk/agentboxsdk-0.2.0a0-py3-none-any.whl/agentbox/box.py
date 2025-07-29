from typing import AsyncIterator, Iterator
from agentbox.engine.registry import get_adapter
from agentbox.models.chat import ChatMessage
from agentbox.settings import Settings
from agentbox.agents.base import Agent


class Box:
    def __init__(self, *, engine: str, model: str):
        self.engine = engine
        self.model = model
        self._adapter = get_adapter(engine)(model=model if model != "na" else None)

    def ask(self, prompt: str) -> str:
        messages = [ChatMessage(role="user", content=prompt)]
        return self._adapter.generate(messages)

    async def async_ask(self, prompt: str) -> str:
        messages = [ChatMessage(role="user", content=prompt)]
        return await self._adapter.a_generate(messages)

    # ───────────── streaming variants ───────────── #
    def stream(self, prompt: str) -> Iterator[str]:
        messages = [ChatMessage(role="user", content=prompt)]
        return self._adapter.stream(messages)

    async def astream(self, prompt: str) -> AsyncIterator[str]:
        messages = [ChatMessage(role="user", content=prompt)]
        async for chunk in self._adapter.a_stream(messages):
            yield chunk

    @classmethod
    def from_settings(cls, settings: Settings | None = None) -> "Box":
        """Create a Box from settings."""
        setting = settings or Settings.load()
        return cls(engine=setting.engine, model=setting.model)

    def run_agent(self, agent: Agent, prompt: str) -> str:
        """Pass prompt to agent; agent may call tools/LLM/etc."""
        messages = [ChatMessage(role="user", content=prompt)]
        return agent.act(messages)
