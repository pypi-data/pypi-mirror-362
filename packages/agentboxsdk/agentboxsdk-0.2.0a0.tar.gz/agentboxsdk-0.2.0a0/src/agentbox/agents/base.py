from abc import ABC, abstractmethod
from typing import Sequence
from agentbox.models.chat import ChatMessage


class Agent(ABC):
    @abstractmethod
    async def a_act(self, messages: Sequence[ChatMessage | dict]) -> str: ...

    def act(self, messages: Sequence[ChatMessage]) -> str:
        msgs = [m if isinstance(m, ChatMessage) else ChatMessage(**m) for m in messages]
        import asyncio

        return asyncio.run(self.a_act(msgs))
