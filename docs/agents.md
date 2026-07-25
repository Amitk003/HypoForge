# Agent Guide

## Literature Scout

Turns the research goal into search queries. Fetches papers from arXiv and other open sources. Builds a search index so other agents can look up relevant findings.

## Data Analyst

Loads your dataset. Builds summary statistics and finds correlations. Runs causal discovery to figure out how variables influence each other. Produces a directed graph of causal relationships.

## Hypothesis Generator

Creates 5-10 hypothesis candidates. It looks at unusual patterns in the data, paths in the causal graph, and gaps in the literature. Each hypothesis includes a core claim and a proposed mechanism.

## Critic

Stress-tests every hypothesis. Checks three things:
-   Is it plausible based on existing research?
-   Does it confuse correlation with causation?
-   Is it practically testable and ethical?

Returns scores and written critiques for each candidate.

## Evolver

Ranks hypotheses using a weighted score: novelty, causal strength, testability, and potential impact. Applies genetic operations - combines good parts of two hypotheses, or mutates a weak part into something stronger.

## Simulator

Trains a quick ML model (XGBoost) on the available data. For each top hypothesis, it simulates what happens when you change the key variable. Reports the predicted effect with confidence intervals.

## Experiment Designer

Turns a hypothesis into a concrete experiment. Specifies what variables to measure, what to control for, what statistical test to use, and how many samples you need. Outputs a step-by-step protocol.

## Meta-Reviewer

Compiles everything into a final document. Includes all citations, the causal graph, simulation plots, the protocol, and safety warnings. Produces a summary suitable for sharing with collaborators.
