from __future__ import annotations

from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

from app.crews.launch_strategy_crew import LaunchStrategyCrew
from app.schemas import LaunchRequest, LaunchResponse
from app.services.ingestion import ingest_inputs
from app.services.storage import create_run_id, save_run


class LaunchStrategyState(BaseModel):
    run_id: str = ""
    request: LaunchRequest | None = None
    ingested_context: str = ""
    category_trends_markdown: str = ""
    competitor_analysis_markdown: str = ""
    consumer_insights_markdown: str = ""
    regulatory_channel_markdown: str = ""
    strategy_markdown: str = ""


class LaunchStrategyFlow(Flow[LaunchStrategyState]):
    @start()
    def ingest(self):
        assert self.state.request is not None
        request = self.state.request
        self.state.run_id = create_run_id()

        docs = ingest_inputs(request)

        assembled = []
        for doc in docs:
            assembled.append(
                f"TITLE: {doc.title}\n"
                f"SOURCE_TYPE: {doc.source_type}\n"
                f"SOURCE_URL: {doc.source_url or 'N/A'}\n"
                f"CONTENT:\n{doc.content}\n"
                f"{'-' * 80}"
            )

        self.state.ingested_context = "\n".join(assembled)
        return docs

    @listen(ingest)
    def run_crew(self, ingested_docs):
        assert self.state.request is not None

        crew = LaunchStrategyCrew().crew()
        result = crew.kickoff(
            inputs={
                "product_name": self.state.request.product_name,
                "category": self.state.request.category,
                "geography": self.state.request.geography,
                "business_goal": self.state.request.business_goal,
                "product_brief": self.state.request.product_brief,
                "constraints": ", ".join(self.state.request.constraints) or "None",
                "additional_context": self.state.request.additional_context or "None",
                "ingested_context": self.state.ingested_context or "None",
            }
        )

        task_outputs = getattr(result, "tasks_output", []) or []

        if len(task_outputs) >= 1:
            self.state.category_trends_markdown = getattr(task_outputs[0], "raw", str(task_outputs[0]))
        if len(task_outputs) >= 2:
            self.state.competitor_analysis_markdown = getattr(task_outputs[1], "raw", str(task_outputs[1]))
        if len(task_outputs) >= 3:
            self.state.consumer_insights_markdown = getattr(task_outputs[2], "raw", str(task_outputs[2]))
        if len(task_outputs) >= 4:
            self.state.regulatory_channel_markdown = getattr(task_outputs[3], "raw", str(task_outputs[3]))
        if len(task_outputs) >= 5:
            self.state.strategy_markdown = getattr(task_outputs[4], "raw", str(task_outputs[4]))
        else:
            self.state.strategy_markdown = getattr(result, "raw", str(result))

        return ingested_docs

    @listen(run_crew)
    def persist(self, ingested_docs):
        assert self.state.request is not None

        artifacts = save_run(
            run_id=self.state.run_id,
            request=self.state.request,
            ingested_docs=ingested_docs,
            category_trends_markdown=self.state.category_trends_markdown,
            competitor_analysis_markdown=self.state.competitor_analysis_markdown,
            consumer_insights_markdown=self.state.consumer_insights_markdown,
            regulatory_channel_markdown=self.state.regulatory_channel_markdown,
            strategy_markdown=self.state.strategy_markdown,
        )

        return LaunchResponse(
            run_id=self.state.run_id,
            product_name=self.state.request.product_name,
            category=self.state.request.category,
            geography=self.state.request.geography,
            category_trends_markdown=self.state.category_trends_markdown,
            competitor_analysis_markdown=self.state.competitor_analysis_markdown,
            consumer_insights_markdown=self.state.consumer_insights_markdown,
            regulatory_channel_markdown=self.state.regulatory_channel_markdown,
            strategy_markdown=self.state.strategy_markdown,
            artifacts=artifacts,
        )
