# Architecture Overview

HypoForge is a multi-agent AI system. Each agent has one job. They run one after another in a pipeline. A shared data object (called HypothesisState) is passed between them.

## How Data Flows

```
Research Goal + Data (CSV/Parquet)
        |
        v
[1] Literature Scout  -->  Searches arXiv for papers
        |
        v
[2] Data Analyst  -->  Analyzes data, builds causal graph
        |
        v
[3] Hypothesis Generator  -->  Creates candidate hypotheses
        |
        v
[4] Critic  -->  Checks each hypothesis for flaws
        |
        v
[5] Evolver  -->  Scores and ranks hypotheses
        |
        v
[6] Simulator  -->  Runs ML counterfactual predictions
        |
        v
[7] Experiment Designer  -->  Creates experiment protocols
        |
        v
[8] Meta-Reviewer  -->  Writes final report
        |
        v
Results (hypotheses, graph, simulations, report)
```

## Two Ways to Run

### 1. REST API (Recommended)

Start the FastAPI server:

```bash
uvicorn src.api.main:app --reload --port 8000
```

The API exposes all pipeline features through HTTP endpoints. A frontend (React, curl, or any HTTP client) can call these endpoints.

### 2. React Frontend

```bash
cd frontend && npm run dev
```

Vite + React + shadcn/ui frontend. Calls the REST API at `/api`. In development, Vite proxies `/api` to `localhost:8000`.

## Project Structure

```
src/
  agents/            AI agents (one Python file per agent)
  api/               FastAPI REST API (routes, main)
  causal/            Causal discovery algorithms (PC algorithm)
  simulation/        ML surrogate models and counterfactual engine
  ui/                Streamlit dashboard (old UI)
  data_engine.py     CSV/Parquet loading and summary
  orchestrator.py    Runs all 8 agents in sequence
  rag_index.py       Semantic search index using Chroma
  state.py           Pydantic data models shared between agents
docs/                Documentation
examples/            Pre-built example scripts
```

## Tech Stack

| Part | What We Use |
|------|-------------|
| Agent pipeline | Python functions with shared Pydantic state |
| Literature search | arXiv free API + Chroma vector database |
| Causal discovery | PC algorithm (tests if variables are independent, finds direction of edges) |
| ML model | scikit-learn RandomForest, bootstrap for confidence intervals |
| REST API | FastAPI with automatic Swagger docs |
| State management | Pydantic v2 (validates all data) |
