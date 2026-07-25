# FAQ

## What is HypoForge?

HypoForge is an open-source multi-agent AI system that helps researchers generate, test, and rank new scientific hypotheses. It searches literature, analyzes data, discovers causal relationships, runs simulations, and designs experiments.

## Do I need to know how to code?

Basic command line skills help (installing packages, running scripts). The dashboard is a graphical interface -- no coding needed to use it. If you want to modify agents or add features, you will need Python.

## Do I need a GPU?

No. Everything runs on CPU. The sentence-transformers model used for semantic search works fine on CPU (about 80MB download).

## Do I need an internet connection?

For arXiv paper lookups, yes. For everything else (data analysis, causal discovery, simulation, dashboard), no.

## What kind of data should I upload?

CSV or Parquet files with numeric columns. At least 50 rows and 5 columns for best results. Column names should describe the variable (e.g., "temperature", "green_space", "pm25"), not generic names like "col1", "col2".

## What happens if I have no data?

The system still works. It searches literature and generates hypotheses based on the research goal alone. But you will not get causal graphs, simulations, or detailed experiment protocols.

## How is this different from ChatGPT or Gemini?

ChatGPT searches and summarizes. HypoForge goes further:
- It discovers causal relationships (not just correlations)
- It runs simulations to predict experiment outcomes
- It generates formal experiment protocols with sample sizes
- It uses multiple specialized agents that critique and improve each other's work

## What is the PC algorithm?

The PC algorithm (Peter-Clark) is a constraint-based causal discovery method. It starts with all variables connected, then removes edges when statistical tests show two variables are independent given a set of other variables. It identifies v-structures (colliders) to determine causal direction.

## Can I add my own agent?

Yes. Create a new file in `src/agents/`, define a function that takes and returns `HypothesisState`, and add it to the pipeline in `src/orchestrator.py`. See the contributing guide in `docs/contributing.md`.

## How are hypotheses scored?

Each hypothesis gets four scores (0-1):

- **Novelty**: How new or unexpected the idea is
- **Causal Rigor**: How well the causal mechanism is supported
- **Testability**: How easy it is to test experimentally
- **Impact**: Potential importance if confirmed

The composite score is the average of all four, minus a penalty for critique notes.

## What is the RAG vector index?

When papers are fetched from arXiv, they are embedded into a Chroma vector database using sentence-transformers. This allows semantic search -- finding papers by meaning, not just keyword matching. The index persists across sessions in the `chroma_db/` folder.

## Is this for real science or just demonstrations?

It is designed for real hypothesis generation. The causal discovery and simulation components use established methods (PC algorithm, RandomForest counterfactuals, bootstrap confidence intervals). However, outputs should be reviewed by domain experts before planning actual experiments.
