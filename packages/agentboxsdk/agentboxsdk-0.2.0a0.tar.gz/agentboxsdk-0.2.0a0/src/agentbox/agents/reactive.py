import re
import asyncio
from typing import Sequence
from agentbox.agents.base import Agent
from agentbox.models.chat import ChatMessage
from agentbox.tools import get_tool
from agentbox.box import Box

_CODE_RE = re.compile(r"```python\s+(.*?)\s+```", re.S)
_SEARCH_RE = re.compile(r"^search\s*:\s*(.+)", re.I | re.S)


class ReactiveAgent(Agent):
    async def a_act(self, messages: Sequence[ChatMessage]) -> str:
        last_msg = messages[-1].content.strip()

        # Python code block
        m = _CODE_RE.search(last_msg)
        if m := _CODE_RE.search(last_msg):
            code = m.group(1).strip()
            PyTool = get_tool("python")
            return await PyTool().a_run(expr=code)

        # 2️⃣ search: query
        if m := _SEARCH_RE.match(last_msg):
            query = m.group(1).strip()
            Search = get_tool("search")
            return await Search().a_run(query=query)

        # 3️⃣ fallback → LLM
        box = Box(engine="ollama", model="llama3.1:8b")
        return await asyncio.to_thread(box.ask, last_msg)
