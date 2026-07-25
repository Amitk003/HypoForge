# Contributing

Want to add new features? Here is how the system is organized.

## Adding a New Agent

1. Create a new file in `src/agents/` (copy an existing agent as a template)
2. The agent function takes a `HypothesisState` object and returns a modified `HypothesisState`
3. Add the function to `STAGE_NAMES` in `src/orchestrator.py` to include it in the pipeline

## Adding a New Causal Discovery Method

1. Create a function in `src/causal/causal_discovery.py`
2. Add it as an option in `build_graph_from_data()`
3. Make sure it returns a `CausalGraphData` object

## Adding a New Frontend

The REST API in `src/api/` exposes all pipeline features. Build any frontend you want that calls these endpoints:

- `POST /api/pipeline` -- run the pipeline
- `GET /api/runs/{id}/hypotheses` -- get ranked hypotheses
- `GET /api/runs/{id}/causal-graph` -- get causal graph data
- `POST /api/runs/{id}/simulate` -- run counterfactual simulation
- `GET /api/runs/{id}/report` -- get full report

## Code Style

- Use Python 3.10+ type hints
- One agent = one file
- Functions take `HypothesisState` and return `HypothesisState`
- No emojis or em dashes in code
- Simple variable names
