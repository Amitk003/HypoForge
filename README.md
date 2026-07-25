# HypoForge: Your AI Co-Scientist

HypoForge is an open-source multi-agent AI system that helps researchers and citizen scientists generate, test, and rank new scientific hypotheses using public data and research literature.

## What It Does

Give HypoForge a research question and optional data. It does the rest:

1.  **Searches** scientific literature for relevant findings
2.  **Analyzes** your data for patterns and causal relationships
3.  **Generates** novel hypothesis candidates
4.  **Debates** them for flaws, novelty, and testability
5.  **Simulates** what would happen if you ran the experiment
6.  **Designs** a concrete experiment protocol
7.  **Ranks** everything so you know which ideas to pursue first

## Why HypoForge?

Most AI tools just search and summarize. HypoForge goes further. It closes the full loop from data to testable experiment design. It works on any domain - urban climate, biodiversity, health, agriculture - and uses only open tools.

## Quick Start

```bash
pip install -r requirements.txt
streamlit run src/ui/app.py
```

## Project Structure

```
src/
  agents/         - AI agents (scout, generator, critic, evolver, etc.)
  causal/         - Causal discovery algorithms
  simulation/     - ML surrogate models and counterfactual engine
  ui/             - Streamlit dashboard
docs/             - Documentation
data/             - Sample datasets
examples/         - Domain-specific example notebooks
```

## How It Works Under the Hood

The system uses a structured multi-agent pipeline. Each agent has a specific job and passes its results to the next stage. All communication happens through a shared state object. The key stages are:

-   **Literature Scout**: Converts your question into search queries, fetches papers from open APIs, and builds a search index.
-   **Data Analyst**: Loads your data, runs basic analysis, and builds a causal graph showing how variables relate.
-   **Hypothesis Generator**: Creates candidate hypotheses by combining data patterns, causal links, and literature findings.
-   **Critic**: Tests each hypothesis for logical flaws, causal mistakes, and practical feasibility.
-   **Evolver**: Ranks hypotheses and combines the best ones to make even stronger candidates.
-   **Simulator**: Trains a quick ML model on your data and predicts what happens under different scenarios.
-   **Experiment Designer**: Produces a step-by-step research protocol with sample size and success metrics.
-   **Meta-Reviewer**: Compiles everything into a final report with citations and risk warnings.

## Requirements

-   Python 3.10+
-   See `requirements.txt` for full list

## License

MIT
