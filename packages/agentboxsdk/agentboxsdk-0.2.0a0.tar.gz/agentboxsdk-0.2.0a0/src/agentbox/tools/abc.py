from abc import ABC, abstractmethod
from pydantic import BaseModel


class ToolMeta(BaseModel, frozen=True):
    name: str
    description: str


class Tool(ABC):
    meta: ToolMeta

    @abstractmethod
    async def a_run(self, **kwargs) -> str: ...
    def run(self, **kwargs) -> str:
        import asyncio

        return asyncio.run(self.a_run(**kwargs))
