from .box import Box
from agentbox.tools import tool
from importlib.metadata import version, PackageNotFoundError

__all__ = ["Box", "tool"]

try:
    __version__: str = version("agentboxsdk")
except PackageNotFoundError:
    __version__ = "0.0.0.dev0"
