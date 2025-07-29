from agentbox.tools import tool
from agentbox.tools.abc import Tool, ToolMeta
import math

SAFE_GLOBALS = {"__builtins__": {}}
SAFE_GLOBALS["math"] = math


@tool
class PythonTool(Tool):
    meta = ToolMeta(
        name="python",
        description="Execute a safe Python expression. Usage: {'expr': '2 + 2'}",
    )

    async def a_run(self, expr: str) -> str:
        try:
            result = eval(expr, SAFE_GLOBALS, {})
            return str(result)
        except Exception as exc:
            return f"Error: {exc}"
