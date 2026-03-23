import json

import requests
import streamlit as st

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Launch Strategy AI", layout="wide")
st.title("Multi-Agent Product Launch Strategy")
st.caption("CrewAI + OpenAI + Tavily + FastAPI + Streamlit")

with st.form("launch_form"):
    product_name = st.text_input("Product Name", value="VoltEdge")
    category = st.text_input("Category", value="Energy Drink")
    geography = st.text_input("Geography", value="United States")

    product_brief = st.text_area(
        "Product Brief",
        value=(
            "A zero-sugar energy drink with moderate caffeine, electrolytes, "
            "B-vitamins, and a no-crash positioning. The product should appeal "
            "to health-conscious young professionals and active Gen Z consumers."
        ),
        height=180,
    )

    business_goal = st.text_area(
        "Business Goal",
        value="Build a differentiated go-to-market strategy for a crowded energy drink market.",
        height=100,
    )

    constraints = st.text_area(
        "Constraints (one per line)",
        value=(
            "Avoid overpromising health claims\n"
            "Must feel premium but accessible\n"
            "Need e-commerce and retail fit"
        ),
        height=100,
    )

    competitor_urls = st.text_area(
        "Competitor URLs (one per line)",
        value=(
            "https://www.redbull.com/us-en/energydrink\n"
            "https://www.monsterenergy.com/en-us/\n"
            "https://www.celsius.com/"
        ),
        height=120,
    )

    additional_context = st.text_area(
        "Additional Context",
        value="The company wants a launch-ready recommendation, not a generic brainstorm.",
        height=80,
    )

    submitted = st.form_submit_button("Run Strategy")

if submitted:
    payload = {
        "product_name": product_name,
        "category": category,
        "geography": geography,
        "product_brief": product_brief,
        "business_goal": business_goal,
        "constraints": [x.strip() for x in constraints.splitlines() if x.strip()],
        "competitor_urls": [x.strip() for x in competitor_urls.splitlines() if x.strip()],
        "additional_context": additional_context,
    }

    with st.spinner("Running multi-agent strategy workflow..."):
        response = requests.post(
            f"{API_BASE}/api/v1/launch-strategy/run",
            json=payload,
            timeout=600,
        )

    if response.status_code != 200:
        st.error(f"Request failed: {response.text}")
    else:
        data = response.json()
        st.success(f"Run complete. Run ID: {data['run_id']}")

        st.subheader("Final Go-to-Market Strategy")
        st.markdown(data["strategy_markdown"])

        with st.expander("Category Trends Report"):
            st.markdown(data["category_trends_markdown"])

        with st.expander("Competitor Analysis Report"):
            st.markdown(data["competitor_analysis_markdown"])

        with st.expander("Consumer Insights Report"):
            st.markdown(data["consumer_insights_markdown"])

        with st.expander("Regulatory and Channel Report"):
            st.markdown(data["regulatory_channel_markdown"])

        with st.expander("Artifacts"):
            st.json(data["artifacts"])

        with st.expander("Raw JSON"):
            st.code(json.dumps(data, indent=2), language="json")
