from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, HttpUrl


class LaunchRequest(BaseModel):
    product_name: str = Field(..., min_length=2, description="Name of the product")
    category: str = Field(default="Energy Drink")
    geography: str = Field(default="United States")
    product_brief: str = Field(
        ...,
        description="Short product description including ingredients, claims, audience, and desired brand feel.",
    )
    business_goal: str = Field(
        default="Create a differentiated go-to-market strategy for a new energy drink launch."
    )
    constraints: List[str] = Field(default_factory=list)
    competitor_urls: List[HttpUrl] = Field(default_factory=list)
    additional_context: Optional[str] = None


class IngestedDocument(BaseModel):
    source_type: str
    source_url: Optional[str] = None
    title: str
    content: str


class RunArtifacts(BaseModel):
    run_id: str
    category_trends_path: str
    competitor_analysis_path: str
    consumer_insights_path: str
    regulatory_channel_path: str
    strategy_path: str
    summary_json_path: str


class LaunchResponse(BaseModel):
    run_id: str
    product_name: str
    category: str
    geography: str
    category_trends_markdown: str
    competitor_analysis_markdown: str
    consumer_insights_markdown: str
    regulatory_channel_markdown: str
    strategy_markdown: str
    artifacts: RunArtifacts


class StoredRun(BaseModel):
    request: LaunchRequest
    ingested_docs: List[IngestedDocument]
    category_trends_markdown: str
    competitor_analysis_markdown: str
    consumer_insights_markdown: str
    regulatory_channel_markdown: str
    strategy_markdown: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
