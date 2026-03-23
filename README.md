# Launch Strategy AI (CrewAI)

A learning-first, production-shaped multi-agent system for product launch strategy.

## What it does

Given a product brief, this app generates:

1. Category Trends Report
2. Competitor Analysis Report
3. Consumer Insights Report
4. Regulatory and Channel Report
5. Final Go-to-Market Strategy

## Stack

- CrewAI
- OpenAI API
- Tavily
- Requests + BeautifulSoup
- FastAPI
- Streamlit

## Setup

### 1) Create and activate a virtual environment

#### macOS / Linux
```bash
python -m venv .venv
source .venv/bin/activate
```

#### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Create your environment file

```bash
cp .env.example .env
```

Populate:
- `OPENAI_API_KEY`
- `TAVILY_API_KEY`

## Run the API

```bash
uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
```

## Run the UI

In a separate terminal:

```bash
streamlit run ui/streamlit_app.py
```

## Health Check

```bash
curl http://localhost:8000/health
```
