# Examples

HypoForge comes with 3 pre-built examples. Each one generates sample data, runs the full pipeline, and saves a report to disk.

## Urban Climate

```bash
python examples/urban_climate.py
```

This creates data about green space, temperature, PM2.5, and traffic in different city areas.

Research question: "How does urban green space affect local air temperature and air quality?"

## Biodiversity and Climate

```bash
python examples/biodiversity_climate.py
```

This creates data about species diversity, temperature, rainfall, and elevation in different locations.

## Environmental Health

```bash
python examples/health_environment.py
```

This creates data about sleep quality, stress, air pollution, noise, and exercise hours.

## Running Without Examples

You can run the pipeline directly from Python:

```python
from src.orchestrator import run_pipeline
from src.state import HypothesisState

state = HypothesisState(research_goal="How does X affect Y?")
result = run_pipeline(state)

for h in result.top_hypotheses:
    print(f"{h.title}: {h.novelty_score}")
```

Or use the API:

```bash
curl -X POST http://localhost:8000/api/pipeline \
  -F "research_goal=How does X affect Y?"
```
