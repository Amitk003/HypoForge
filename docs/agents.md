# Agent Guide

HypoForge has 8 AI agents. Each agent has one job. They run in sequence and pass results to the next agent.

## Literature Scout

Turns your research question into search queries. Fetches papers from arXiv (free research paper database). Stores paper summaries so other agents can use them.

## Data Analyst

Loads your CSV or Parquet data. Builds a summary (row count, column types, missing values, correlations). Runs causal discovery to find how variables affect each other. Produces a cause-effect graph.

## Hypothesis Generator

Creates hypotheses using three sources:
- Patterns it finds in your data
- Paths in the causal graph
- Gaps in the research papers found by the Literature Scout

Each hypothesis includes a main claim and a proposed mechanism (how the cause leads to the effect).

## Critic

Checks every hypothesis for problems:
- Is it backed by evidence?
- Does it mix up correlation with causation?
- Can it actually be tested?
- Are there any ethical concerns?

Returns a list of issues found for each hypothesis.

## Evolver

Scores hypotheses on 4 things:
- Novelty: how new or surprising
- Causal rigor: how strong is the cause-effect evidence
- Testability: how easy to test
- Impact: how important if proven true

Can also combine two good hypotheses (crossover) or adjust weak parts (mutation) to create stronger candidates.

## Simulator

Trains a RandomForest model on your data. For each top hypothesis, it simulates: "What happens if we change variable X to value Y?" Reports the predicted effect with a 95% confidence interval.

## Experiment Designer

Turns a hypothesis into a formal experiment plan:
- What to measure (independent and dependent variables)
- What to control for (confounders)
- What statistical test to use
- How many samples needed
- Step-by-step procedure

## Meta-Reviewer

Takes everything from all previous agents and writes a final report. Includes citations, causal graph summary, simulation results, experiment protocols, and safety warnings.
