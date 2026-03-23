from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from app.config import get_settings
from app.schemas import IngestedDocument, LaunchRequest, RunArtifacts, StoredRun


def create_run_id() -> str:
    return uuid4().hex[:12]


def get_run_dir(run_id: str) -> Path:
    settings = get_settings()
    run_dir = Path(settings.storage_dir) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def save_run(
    run_id: str,
    request: LaunchRequest,
    ingested_docs: list[IngestedDocument],
    category_trends_markdown: str,
    competitor_analysis_markdown: str,
    consumer_insights_markdown: str,
    regulatory_channel_markdown: str,
    strategy_markdown: str,
) -> RunArtifacts:
    run_dir = get_run_dir(run_id)

    category_trends_path = run_dir / "01_category_trends.md"
    competitor_analysis_path = run_dir / "02_competitor_analysis.md"
    consumer_insights_path = run_dir / "03_consumer_insights.md"
    regulatory_channel_path = run_dir / "04_regulatory_channel.md"
    strategy_path = run_dir / "05_go_to_market_strategy.md"
    summary_path = run_dir / "run_summary.json"

    category_trends_path.write_text(category_trends_markdown, encoding="utf-8")
    competitor_analysis_path.write_text(competitor_analysis_markdown, encoding="utf-8")
    consumer_insights_path.write_text(consumer_insights_markdown, encoding="utf-8")
    regulatory_channel_path.write_text(regulatory_channel_markdown, encoding="utf-8")
    strategy_path.write_text(strategy_markdown, encoding="utf-8")

    payload = StoredRun(
        request=request,
        ingested_docs=ingested_docs,
        category_trends_markdown=category_trends_markdown,
        competitor_analysis_markdown=competitor_analysis_markdown,
        consumer_insights_markdown=consumer_insights_markdown,
        regulatory_channel_markdown=regulatory_channel_markdown,
        strategy_markdown=strategy_markdown,
        metadata={"run_id": run_id},
    )
    summary_path.write_text(payload.model_dump_json(indent=2), encoding="utf-8")

    return RunArtifacts(
        run_id=run_id,
        category_trends_path=str(category_trends_path),
        competitor_analysis_path=str(competitor_analysis_path),
        consumer_insights_path=str(consumer_insights_path),
        regulatory_channel_path=str(regulatory_channel_path),
        strategy_path=str(strategy_path),
        summary_json_path=str(summary_path),
    )


def load_run(run_id: str) -> dict:
    run_dir = get_run_dir(run_id)
    summary_path = run_dir / "run_summary.json"

    if not summary_path.exists():
        raise FileNotFoundError(f"Run not found: {run_id}")

    return json.loads(summary_path.read_text(encoding="utf-8"))
