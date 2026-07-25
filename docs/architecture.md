# Architecture Overview

HypoForge is built as a pipeline of specialized agents. Each agent does one job and passes the result to the next agent.

## How Data Flows

1.  User enters a research goal and optional data file
2.  Literature Scout and Data Analyst run in parallel
3.  Their outputs feed into the Hypothesis Generator
4.  Generator produces multiple hypothesis candidates
5.  Critic tests each candidate for problems
6.  Evolver ranks and combines the best ones
7.  Simulator runs what-if predictions for top hypotheses
8.  Experiment Designer creates a protocol for each
9.  Meta-Reviewer produces the final output

## State Management

All agents share a common state object called `HypothesisState`. This contains:

-   All hypothesis candidates with their scores
-   Causal graphs discovered from data
-   Simulation results
-   Experiment protocols
-   Full debate logs

## Technology Choices

-   **Orchestration**: LangGraph for agent coordination
-   **State**: Pydantic models for type safety
-   **Search**: arXiv API + vector search (Chroma/FAISS)
-   **Causal**: PC algorithm via causal-learn
-   **Simulation**: XGBoost with bootstrap confidence intervals
-   **UI**: Streamlit with PyVis for graphs
-   **LLM**: Defaults to open models, can use OpenAI as upgrade
