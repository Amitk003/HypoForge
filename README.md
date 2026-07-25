# HypoForge: Your AI Co-Scientist

HypoForge is an open-source multi-agent AI system that generates, debates, ranks, simulates, and designs experiments for novel scientific hypotheses. Give it a research question and optional data -- it does the rest.

## What It Does

1.  **Searches** scientific literature (arXiv + semantic RAG search)
2.  **Analyzes** your data and discovers causal relationships (PC algorithm)
3.  **Generates** novel hypothesis candidates
4.  **Debates** them for plausibility, causal fallacies, and feasibility
5.  **Evolves** the best ones through genetic crossover and mutation
6.  **Simulates** counterfactual outcomes with confidence intervals
7.  **Designs** concrete experiment protocols with sample size estimates
8.  **Ranks** everything so you know which ideas to pursue first

## Why HypoForge?

Most AI tools search and summarize. HypoForge closes the full loop from raw data to testable experiment design. It works on any domain -- urban climate, biodiversity, health, agriculture -- using only open tools and models.

## Quick Start

```bash
pip install -r requirements.txt
streamlit run src/ui/app.py
```

## Project Structure

```
src/
  agents/             8 specialized AI agents
  causal/             PC algorithm + confounder/mediator detection
  simulation/         ML surrogate models + counterfactual engine
  ui/                 Streamlit dashboard (5 tabs)
  rag_index.py        Chroma vector index for semantic paper search
  orchestrator.py     Pipeline that sequences all agents
  state.py            Shared Pydantic state passed between agents
docs/                 Documentation
examples/             Pre-built domain examples to run
data/                 Sample datasets and uploads
```

## How Each Agent Works

| Agent | What it does |
|---|---|
| **Literature Scout** | Converts your question into search queries, fetches papers from arXiv, embeds them into a Chroma vector index, and returns semantically ranked results |
| **Data Analyst** | Loads your CSV/Parquet, runs EDA, and discovers a causal DAG using the PC algorithm (partial correlation + conditional independence tests + v-structure orientation + Meek rule propagation). Identifies confounders and mediators |
| **Hypothesis Generator** | Creates 5-10 candidate hypotheses from data anomalies, causal graph paths, and literature gaps |
| **Critic** | Stress-tests each hypothesis for empirical plausibility, causal fallacies, and practical feasibility |
| **Evolver** | Ranks by composite score (novelty, causal rigor, testability, impact). Applies genetic crossover and mutation to create stronger combined candidates |
| **Simulator** | Trains a RandomForest surrogate on your data. Runs counterfactual predictions (do(X=x)) with bootstrap 95% confidence intervals |
| **Experiment Designer** | Translates top hypotheses into formal protocols with IVs, DVs, confounders, statistical test, sample size, and step-by-step procedure |
| **Meta-Reviewer** | Compiles all findings, citations, DAG diagrams, simulation results, and safety warnings into a synthesis report |

## Interactive Dashboard (Streamlit)

The dashboard has 5 tabs:

-   **Research Setup** -- Enter goal, upload data, run pipeline, see summary metrics
-   **Agent Debate** -- Chat-style log of generator, critic, and evolver discussions
-   **Ranked Hypotheses** -- Expandable cards with scores, evidence, critique, safety flags
-   **Causal Graph & Simulator** -- Interactive PyVis causal graph with live counterfactual slider. Adjust intervention values and see predicted outcomes update in real time
-   **Report & Export** -- Full meta-review report with Markdown download

## Running the Examples

```bash
# Urban climate -- green space, temperature, PM2.5
python examples/urban_climate.py

# Biodiversity -- species richness, temperature, precipitation
python examples/biodiversity_climate.py

# Environmental health -- sleep quality, AQI, noise
python examples/health_environment.py
```

## Running Tests

```bash
python test_pipeline.py
```

## Requirements

-   Python 3.10+
-   See `requirements.txt` for full list

## License

MIT
