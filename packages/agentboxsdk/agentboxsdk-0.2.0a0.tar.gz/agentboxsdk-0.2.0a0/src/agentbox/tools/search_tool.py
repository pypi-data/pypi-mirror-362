from __future__ import annotations
import httpx
import asyncio
from agentbox.tools import tool
from agentbox.tools.abc import Tool, ToolMeta


@tool
class SearchTool(Tool):
    """Return DuckDuckGo Instant-Answer snippet + url."""

    meta = ToolMeta(
        name="search",
        description="Quick lookup via DuckDuckGo Instant Answer API",
    )

    async def a_run(self, query: str) -> str:
        snippet, url = await self._instant_answer(query)
        if not snippet:  # fallback: ddg scrape
            snippet, url = await asyncio.to_thread(self._scrape_ddg, query)

        if not snippet:
            return "No answer found."

        return f"{snippet}\nSource: {url}" if url else snippet

    # ───────────────────── helpers ───────────────────── #

    async def _instant_answer(self, q: str) -> tuple[str, str]:
        api = "https://api.duckduckgo.com/"
        params = {"q": q, "format": "json", "no_redirect": 1, "no_html": 1}
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(api, params=params)
            r.raise_for_status()
            data = r.json()

        snippet = data.get("AbstractText") or data.get("Answer") or ""
        url = data.get("AbstractURL") or data.get("Redirect") or ""
        return snippet, url

    def _scrape_ddg(self, q: str) -> tuple[str, str]:
        try:
            from ddgs import DDGS
        except ImportError:
            return "", ""

        res = DDGS().text(q, max_results=2)
        if not res:
            return "", ""
        first = res[0]
        return first.get("body", ""), first.get("href", "")
