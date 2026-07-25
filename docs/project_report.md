# HypoForge: Open-Source Multi-Agent AI Co-Scientist

## Project Overview

HypoForge is an open-source multi-agent AI co-scientist that automatically generates, ranks, critiques, evolves, and simulates novel scientific hypotheses from a research question and optional dataset. It runs entirely locally with no external API keys, democratizing AI-assisted scientific discovery.

## Problem Being Solved

Researchers face a lengthy bottleneck: reviewing literature, analyzing data, identifying causal relationships, generating testable hypotheses, designing experiments, and producing reports. This process is manual, slow, and prone to cognitive bias. HypoForge automates the entire hypothesis lifecycle, letting scientists focus on creative interpretation and experimental execution.

## Proposed Solution

A pipeline of 8 specialized AI agents that work sequentially:

1. **Literature Scout** — Searches arXiv for papers relevant to the research question using semantic embeddings (sentence-transformers) and stores them in a Chroma vector index for RAG retrieval.
2. **Data Analyst** — Loads CSV/Parquet data, generates an EDA summary (missingness, correlations, distributions), and runs causal discovery to build a directed acyclic graph (DAG).
3. **Hypothesis Generator** — Creates candidate hypotheses from three sources: data patterns (anomalies/clusters), causal DAG paths, and gaps in the literature.
4. **Critic** — Stress-tests every hypothesis for empirical plausibility, causal fallacies, testability, and ethical concerns.
5. **Evolver** — Scores hypotheses on novelty, causal rigor, testability, and impact. Performs genetic crossover and mutation to evolve stronger candidates.
6. **Simulator** — Trains a RandomForest surrogate model on the data and runs counterfactual predictions (do(X=x)) with bootstrap 95% confidence intervals.
7. **Experiment Designer** — Converts top hypotheses into formal experiment protocols: variables, confounders, statistical tests, sample size estimates, and step-by-step procedures.
8. **Meta-Reviewer** — Synthesizes everything into a final research report with citations, causal graph, simulation results, protocols, and safety warnings.

## Innovation and Uniqueness

- **No external LLM APIs required** — Unlike most AI research tools, HypoForge uses only free open-source models (sentence-transformers for embeddings, scikit-learn for ML). No OpenAI, Anthropic, or other paid services needed.
- **Full hypothesis lifecycle** — Not just idea generation. HypoForge covers literature search, causal discovery, critique, evolution, ML simulation, experiment design, and peer-review-level reporting in one pipeline.
- **Custom causal discovery engine** — Implements a PC algorithm with conditional independence testing, v-structure detection, Meek rules, and confounder/mediator identification — no reliance on external causal libraries.
- **Multi-agent architecture** — 8 specialized agents with distinct roles, not a single monolithic prompt. Each agent has a narrow, well-defined task.

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.12 |
| UI Framework | Streamlit (dashboard), FastAPI (REST API) |
| ML / AI | scikit-learn (RandomForest), sentence-transformers (embeddings), scipy (hypothesis testing) |
| Causal Discovery | Custom PC algorithm implementation (networkx) |
| Vector Store | ChromaDB (semantic paper index) |
| Data | pandas, numpy |
| Literature | arXiv API (via requests + XML parsing) |
| Visualization | pyvis, matplotlib, networkx |
| Deployment | Streamlit Community Cloud |

## Architecture

```
Research Question + Data
        |
Literature Scout ---- arXiv API + RAG Index
Data Analyst ---- EDA + PC Causal Discovery
Hypothesis Generator ---- Data + Graph + Literature
Critic ---- Plausibility + Safety Checks
Evolver ---- Multi-Criteria Ranking + Genetic Operators
Simulator ---- RandomForest Counterfactuals (do(X=x))
Experiment Designer ---- Formal Protocol Generation
Meta-Reviewer ---- Final Report Synthesis
        |
Ranked Hypotheses + Causal Graph + Simulations + Protocols + Report
```

## Domain Examples

1. **Urban Microclimate**: "How does urban green space affect local air temperature and air quality?" Uses synthetic urban data with variables: temperature, green_space, traffic_density, surface_albedo, PM2.5.
2. **Environmental Health**: "How does long-term exposure to air pollution and noise affect sleep quality?" Uses synthetic health data with variables: sleep_quality, AQI, noise_level, physical_activity.
3. **Biodiversity & Climate**: "How do temperature and precipitation changes affect species diversity?" Uses synthetic ecological data with variables: species_richness, temperature, precipitation, habitat_fragmentation.

## Results and Validation

- **26 automated tests** covering all agents, pipeline orchestration, data engine, causal discovery, and simulation — all passing.
- Pipeline generates **10+ ranked hypotheses** per run with multi-dimensional scores (novelty, causal rigor, testability, impact).
- Causal graphs identify **confounders and mediators** automatically from data.
- ML surrogate simulator produces **counterfactual predictions with 95% confidence intervals**.
- Experiment protocols include **sample size estimates and statistical test recommendations**.

## How to Run

```bash
pip install -r requirements.txt
streamlit run src/ui/app.py
```

Then open the browser, enter a research question, upload data (optional), and click "Run Pipeline".

## Deployment

- **Streamlit Community Cloud**: Connected to GitHub repo, auto-deploys from `main` branch.
- **API mode**: FastAPI backend available at `/api` endpoints for headless integration.

## Repository

https://github.com/Amitk003/HypoForge

## License

Open source.
