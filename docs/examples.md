# Examples

HypoForge comes with 3 pre-built domain examples. Each generates sample data and runs the full pipeline.

## Urban Microclimate & Air Quality

Explore how green space, traffic, and building density affect temperature and PM2.5.

```bash
python examples/urban_climate.py
```

## Biodiversity & Climate Adaptation

Study how temperature and precipitation affect species richness in fragmented habitats.

```bash
python examples/biodiversity_climate.py
```

## Environmental Health & Wearables

Investigate how air quality and noise exposure impact sleep quality and heart rate.

```bash
python examples/health_environment.py
```

## Running Your Own Data

Replace the sample data with your own CSV or Parquet file:

```bash
python -c "
from src.orchestrator import run_pipeline
from src.state import HypothesisState
state = HypothesisState(research_goal='Your question here', data_path='path/to/your/data.csv')
result = run_pipeline(state)
print(result.meta_review_report)
"
```

Or upload your file through the Streamlit UI at `src/ui/app.py`.
