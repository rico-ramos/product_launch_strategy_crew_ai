from typing import Optional, Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from tavily import TavilyClient

from app.config import get_settings


class TavilySearchInput(BaseModel):
    query: str = Field(..., description="The search query to execute.")
    max_results: int = Field(default=5, ge=1, le=10)
    topic: Optional[str] = Field(
        default="general",
        description="Search topic. Common values are 'general' or 'news'.",
    )


class TavilySearchTool(BaseTool):
    name: str = "Tavily Search Tool"
    description: str = (
        "Search the web for current market information, competitor analysis, "
        "consumer trends, pricing, and market intelligence."
    )
    args_schema: Type[BaseModel] = TavilySearchInput

    def _run(self, query: str, max_results: int = 5, topic: str = "general") -> str:
        settings = get_settings()
        client = TavilyClient(api_key=settings.tavily_api_key)

        response = client.search(
            query=query,
            max_results=max_results,
            topic=topic,
            include_answer=False,
            include_raw_content=False,
        )

        results = response.get("results", [])
        if not results:
            return "No search results found."

        lines = []
        for idx, item in enumerate(results, start=1):
            title = item.get("title", "Untitled")
            url = item.get("url", "")
            content = item.get("content", "")
            lines.append(
                f"{idx}. TITLE: {title}\n"
                f"URL: {url}\n"
                f"SNIPPET: {content}\n"
            )

        return "\n".join(lines)
