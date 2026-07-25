# Contributing to HypoForge

## How to Add a New Agent

1.  Create a new file in `src/agents/`
2.  Define a class that takes `HypothesisState` and returns an updated `HypothesisState`
3.  Add the agent to the pipeline in the orchestrator
4.  Write the corresponding documentation

## How to Add a New Causal Method

1.  Add your algorithm in `src/causal/`
2.  The method should take a pandas DataFrame and return a networkx DiGraph
3.  Register it in the causal discovery factory function

## How to Add a New Domain Vertical

1.  Create a folder in `examples/`
2.  Add a script that downloads sample data and runs the pipeline
3.  Document what the example shows

## Code Style

-   Use type hints everywhere
-   Keep functions small and focused on one thing
-   Write docstrings for public functions
-   Test with the test_pipeline.py script
