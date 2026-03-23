from crewai import Agent, Crew, LLM, Process, Task

from app.config import get_settings
from app.tools.tavily_search_tool import TavilySearchTool
from app.tools.webpage_scrape_tool import WebpageScrapeTool


class LaunchStrategyCrew:
    def __init__(self) -> None:
        settings = get_settings()
        self.llm = LLM(model=settings.openai_model_name, temperature=0.2)
        self.search_tool = TavilySearchTool()
        self.scrape_tool = WebpageScrapeTool()

    def market_research_lead(self) -> Agent:
        return Agent(
            role="Market Research Lead",
            goal="Analyze category trends and produce evidence-based market context for the product launch.",
            backstory=(
                "You are a senior CPG market intelligence lead specializing in beverage markets, "
                "trend analysis, category shifts, and launch readiness."
            ),
            llm=self.llm,
            tools=[self.search_tool, self.scrape_tool],
            verbose=True,
            allow_delegation=False,
            max_iter=8,
        )

    def competitor_intelligence_analyst(self) -> Agent:
        return Agent(
            role="Competitor Intelligence Analyst",
            goal="Benchmark competitors, positioning patterns, pricing signals, and whitespace opportunities.",
            backstory=(
                "You specialize in competitive intelligence for beverage brands, including packaging, "
                "claims, pricing, digital presence, and whitespace analysis."
            ),
            llm=self.llm,
            tools=[self.search_tool, self.scrape_tool],
            verbose=True,
            allow_delegation=False,
            max_iter=8,
        )

    def consumer_insights_analyst(self) -> Agent:
        return Agent(
            role="Consumer Insights Analyst",
            goal="Identify target audience needs, behaviors, motivations, objections, and usage occasions.",
            backstory=(
                "You are a consumer researcher focused on Gen Z, Millennials, wellness behaviors, "
                "social influence, and energy-drink purchase drivers."
            ),
            llm=self.llm,
            tools=[self.search_tool],
            verbose=True,
            allow_delegation=False,
            max_iter=8,
        )

    def regulatory_channel_analyst(self) -> Agent:
        return Agent(
            role="Regulatory and Channel Analyst",
            goal="Identify claim risks, regulatory watchouts, and channel implications for launch strategy.",
            backstory=(
                "You analyze compliance-sensitive messaging, caffeine and wellness claim exposure, "
                "and retail/e-commerce channel strategy for CPG brands."
            ),
            llm=self.llm,
            tools=[self.search_tool, self.scrape_tool],
            verbose=True,
            allow_delegation=False,
            max_iter=8,
        )

    def product_strategist(self) -> Agent:
        return Agent(
            role="Product Strategist",
            goal="Convert evidence from prior analysis into a differentiated go-to-market strategy.",
            backstory=(
                "You are a product marketing strategist for consumer brands. You transform research "
                "into positioning, personas, pricing, messaging, and launch plans."
            ),
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=8,
        )

    def crew(self) -> Crew:
        market_lead = self.market_research_lead()
        competitor_analyst = self.competitor_intelligence_analyst()
        consumer_analyst = self.consumer_insights_analyst()
        regulatory_analyst = self.regulatory_channel_analyst()
        strategist = self.product_strategist()

        category_trends_task = Task(
            description="""
Analyze the category context for this launch.

Product: {product_name}
Category: {category}
Geography: {geography}
Business Goal: {business_goal}
Product Brief: {product_brief}
Constraints: {constraints}
Additional Context: {additional_context}

Pre-ingested context:
{ingested_context}

Your responsibilities:
1. Analyze category trends shaping the energy drink market.
2. Identify growth themes and major market shifts.
3. Highlight health-conscious trends such as low sugar, functional ingredients, hydration, focus, or no-crash positioning.
4. Note where evidence is directional versus strongly supported.
5. Keep findings practical for launch strategy.

Output ONLY markdown.

Required structure:
# Category Trends Report
## Executive Summary
## Market Dynamics
## Growth Drivers
## Health and Functional Trends
## Risks and Constraints
## Launch Implications
## Sources
""",
            expected_output="A markdown category trends report.",
            agent=market_lead,
        )

        competitor_analysis_task = Task(
            description="""
Create a competitor intelligence report for this launch.

Focus competitors:
- Red Bull
- Monster
- Celsius
- Rockstar
- Any relevant emerging challenger brands you find

Use the product brief and any ingested competitor URLs.

Your responsibilities:
1. Compare brand positioning and target audience signals.
2. Compare product claims, flavor architecture, packaging signals, and differentiation patterns.
3. Analyze pricing direction where available.
4. Identify whitespace opportunities for a new entrant.
5. Highlight what to emulate versus avoid.

Output ONLY markdown.

Required structure:
# Competitor Analysis Report
## Executive Summary
## Competitor Profiles
## Positioning Patterns
## Pricing Signals
## Claims and Messaging Patterns
## Whitespace Opportunities
## Strategic Takeaways
## Sources
""",
            expected_output="A markdown competitor analysis report.",
            agent=competitor_analyst,
        )

        consumer_insights_task = Task(
            description="""
Create a consumer insights report for the proposed launch.

Use prior task outputs plus tool-based research.

Your responsibilities:
1. Analyze likely buyer segments in the target geography.
2. Focus on Gen Z and Millennials, but note adjacent segments if relevant.
3. Identify motivations, unmet needs, objections, and usage occasions.
4. Distinguish health-conscious buyers from performance-driven buyers where useful.
5. Translate insights into actionable audience implications.

Output ONLY markdown.

Required structure:
# Consumer Insights Report
## Executive Summary
## Core Consumer Segments
## Motivations and Jobs-to-be-Done
## Objections and Purchase Barriers
## Consumption Occasions
## Audience Implications
## Sources
""",
            expected_output="A markdown consumer insights report.",
            agent=consumer_analyst,
        )

        regulatory_channel_task = Task(
            description="""
Create a regulatory and channel strategy report.

Use prior task outputs plus tool-based research.

Your responsibilities:
1. Identify likely regulatory and claim watchouts relevant to energy drinks.
2. Call out caffeine, health/wellness, and functional-ingredient messaging risks at a high level.
3. Compare channel considerations across convenience, grocery, big box, e-commerce, and digital/social channels.
4. Identify channel implications for premium versus accessible pricing.
5. Recommend channel priorities and messaging precautions.

Do not provide legal advice. Provide business-facing strategic guidance.

Output ONLY markdown.

Required structure:
# Regulatory and Channel Report
## Executive Summary
## Claim and Messaging Watchouts
## Caffeine and Wellness Risk Considerations
## Retail Channel Implications
## Digital and E-commerce Implications
## Recommended Channel Priorities
## Sources
""",
            expected_output="A markdown regulatory and channel report.",
            agent=regulatory_analyst,
        )

        strategy_task = Task(
            description="""
Using all prior reports, create the final go-to-market strategy.

Product: {product_name}
Category: {category}
Geography: {geography}
Product Brief: {product_brief}
Business Goal: {business_goal}
Constraints: {constraints}

Your responsibilities:
1. Recommend the best target audience.
2. Create 2-3 practical personas.
3. Define a clear positioning statement.
4. Define a differentiated USP.
5. Create message pillars.
6. Recommend pricing direction.
7. Recommend priority channels and launch motions.
8. Provide launch risks and mitigations.
9. Produce a practical 90-day launch plan.

Output ONLY markdown.

Required structure:
# Go-to-Market Strategy
## Strategic Recommendation
## Target Audience
## Personas
## Positioning Statement
## Unique Selling Proposition
## Message Pillars
## Pricing Recommendation
## Channel and Marketing Strategy
## Launch Risks and Mitigations
## 90-Day Launch Plan
""",
            expected_output="A markdown go-to-market strategy.",
            agent=strategist,
        )

        return Crew(
            agents=[
                market_lead,
                competitor_analyst,
                consumer_analyst,
                regulatory_analyst,
                strategist,
            ],
            tasks=[
                category_trends_task,
                competitor_analysis_task,
                consumer_insights_task,
                regulatory_channel_task,
                strategy_task,
            ],
            process=Process.sequential,
            verbose=True,
            memory=False,
            planning=False,
        )
