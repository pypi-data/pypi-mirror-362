from typing import Type, Dict
from agentbox.engine.abc import EngineAdapter
from agentbox.engine.dummy import DummyEngineAdapter
from agentbox.engine.ollama_engine import OllamaEngine
from agentbox.engine.openai_engine import OpenAIEngine

_registry: Dict[str, Type[EngineAdapter]] = {
    "dummy": DummyEngineAdapter,
    "ollama": OllamaEngine,
    "openai": OpenAIEngine,
}


def get_adapter(name: str) -> Type[EngineAdapter]:
    try:
        return _registry[name]
    except KeyError as exc:
        raise ValueError(f"Unknown engine: {name}") from exc
