# API Guide

HypoForge provides a REST API built with FastAPI. You can use it to run the pipeline and get results from any programming language or tool.

## Start the Server

```bash
uvicorn src.api.main:app --reload --port 8000
```

Open `http://localhost:8000/docs` in your browser. You will see the Swagger UI where you can test all endpoints.

## Available Endpoints

### Health Check

```
GET /api/health
```

Returns `{"status": "ok"}`. Use this to check if the server is running.

### Run Pipeline

```
POST /api/pipeline
```

Starts the multi-agent pipeline. This is the main endpoint.

**Request Body (form data):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| research_goal | string | Yes | Your research question |
| file | file | No | CSV or Parquet data file |
| alpha | number | No | Significance level for causal discovery (default: 0.05) |
| max_hypotheses | integer | No | Maximum number of hypotheses to generate (default: 10) |

**Response:**

```json
{
  "run_id": "abc-123-def",
  "pipeline_stage": "complete",
  "hypothesis_count": 5,
  "simulation_count": 3,
  "protocol_count": 3,
  "error_count": 0,
  "errors": [],
  "timings": {
    "literature_scout": 1.2,
    "data_analysis": 2.5,
    ...
  }
}
```

Use the `run_id` to get results from the other endpoints.

### Get Pipeline Status

```
GET /api/runs/{run_id}
```

Returns the current status and summary counts for a pipeline run.

### Get Hypotheses

```
GET /api/runs/{run_id}/hypotheses
```

Returns a list of ranked hypotheses with scores:

| Field | Description |
|-------|-------------|
| title | Short name for the hypothesis |
| core_statement | The main claim |
| proposed_mechanism | How the cause-effect works |
| novelty_score | How new or surprising (0 to 1) |
| causal_rigor_score | How strong is the causal evidence (0 to 1) |
| testability_score | How easy to test (0 to 1) |
| impact_score | Potential impact if true (0 to 1) |
| critique_notes | List of weaknesses found by the Critic agent |
| safety_flags | List of ethical concerns |
| supporting_evidence | Evidence from literature or data |

### Get Causal Graph

```
GET /api/runs/{run_id}/causal-graph
```

Returns the discovered cause-effect relationships:

```json
{
  "nodes": ["temperature", "green_space", "traffic"],
  "edges": [
    {"source": "green_space", "target": "temperature", "weight": 0.8}
  ],
  "confounders": ["traffic"],
  "mediators": []
}
```

### Run Counterfactual Simulation

```
POST /api/runs/{run_id}/simulate
```

Simulate what happens if you change a variable. Send as form data:

| Field | Type | Description |
|-------|------|-------------|
| target_variable | string | The variable you want to predict |
| intervention_variable | string | The variable you want to change |
| intervention_value | number | The new value for the intervention |

**Response:**

```json
{
  "target_variable": "temperature",
  "intervention_variable": "green_space",
  "intervention_value": 96.0,
  "baseline_outcome": 25.3,
  "predicted_outcome": 24.9,
  "delta": -0.4,
  "ci_lower": -0.8,
  "ci_upper": -0.1
}
```

- `delta`: Change from baseline to predicted (negative means decrease)
- `ci_lower` and `ci_upper`: 95% confidence interval for the change

### Get Report

```
GET /api/runs/{run_id}/report
```

Returns the full meta-review report in Markdown format, plus summary stats.

## Using with curl

```bash
# Run pipeline
curl -X POST http://localhost:8000/api/pipeline \
  -F "research_goal=How does green space affect temperature?" \
  -F "file=@data/sample.csv"

# Get hypotheses (replace run_id with actual value)
curl http://localhost:8000/api/runs/YOUR_RUN_ID/hypotheses

# Run simulation
curl -X POST http://localhost:8000/api/runs/YOUR_RUN_ID/simulate \
  -F "target_variable=temperature" \
  -F "intervention_variable=green_space" \
  -F "intervention_value=96.0"
```

## Using with Python

```python
import requests

# Run pipeline
resp = requests.post("http://localhost:8000/api/pipeline", data={
    "research_goal": "How does green space affect temperature?"
})
run_id = resp.json()["run_id"]

# Get hypotheses
hypotheses = requests.get(f"http://localhost:8000/api/runs/{run_id}/hypotheses").json()
for h in hypotheses:
    print(f"{h['title']}: {h['novelty_score']}")
```
