from typing import Type

import requests
from bs4 import BeautifulSoup
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class WebpageScrapeInput(BaseModel):
    url: str = Field(..., description="Webpage URL to fetch and extract readable text from.")


class WebpageScrapeTool(BaseTool):
    name: str = "Webpage Scrape Tool"
    description: str = "Fetch a webpage and extract readable text content for downstream analysis."
    args_schema: Type[BaseModel] = WebpageScrapeInput

    def _run(self, url: str) -> str:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            )
        }

        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = " ".join(soup.stripped_strings)
        return text[:12000]
