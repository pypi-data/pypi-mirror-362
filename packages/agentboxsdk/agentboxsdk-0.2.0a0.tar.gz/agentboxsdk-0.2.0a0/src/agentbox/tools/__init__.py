from __future__ import annotations

from importlib import import_module

from agentbox.tools.abc import Tool, ToolMeta
from agentbox.tools.registry import (
    get as get_tool,
    register as register_tool,
    register as _register,
)

__all__ = ["tool", "get_tool", "register_tool", "Tool", "ToolMeta"]


# ──────────────────────────────────────────────────────
def tool(cls: type[Tool]) -> type[Tool]:
    """Class decorator that registers the tool with the global registry."""
    _register(cls)
    return cls


# Auto-load built-in tools (side-effect registration)
import_module("agentbox.tools.python_tool")
import_module("agentbox.tools.search_tool")
