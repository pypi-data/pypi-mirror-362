from typing import Dict, Type
from agentbox.tools.abc import Tool

_registry: Dict[str, Type[Tool]] = {}


def register(tool_cls: Type[Tool]) -> None:
    _registry[tool_cls.meta.name] = tool_cls


def get(name: str) -> Type[Tool]:
    return _registry[name]
