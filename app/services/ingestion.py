from typing import List

import requests
from bs4 import BeautifulSoup

from app.schemas import IngestedDocument, LaunchRequest


def scrape_url(url: str) -> IngestedDocument:
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

    title = soup.title.string.strip() if soup.title and soup.title.string else url

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = " ".join(soup.stripped_strings)

    return IngestedDocument(
        source_type="competitor_url",
        source_url=url,
        title=title,
        content=text[:15000],
    )


def ingest_inputs(request: LaunchRequest) -> List[IngestedDocument]:
    docs: List[IngestedDocument] = []

    docs.append(
        IngestedDocument(
            source_type="user_brief",
            title="User Product Brief",
            content=(
                f"Product Name: {request.product_name}\n"
                f"Category: {request.category}\n"
                f"Geography: {request.geography}\n"
                f"Business Goal: {request.business_goal}\n"
                f"Product Brief: {request.product_brief}\n"
                f"Constraints: {', '.join(request.constraints) if request.constraints else 'None'}\n"
                f"Additional Context: {request.additional_context or 'None'}"
            ),
        )
    )

    for url in request.competitor_urls:
        try:
            docs.append(scrape_url(str(url)))
        except Exception as exc:
            docs.append(
                IngestedDocument(
                    source_type="competitor_url_error",
                    source_url=str(url),
                    title=f"Failed to ingest: {url}",
                    content=f"Error while scraping URL: {exc}",
                )
            )

    return docs
