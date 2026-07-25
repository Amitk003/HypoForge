# HypoForge: AI Co-Scientist

Turn your research questions into ranked, testable hypotheses with experiment designs.

```
You:  "How does urban green space affect air temperature?"
AI:   "Hypothesis #1: Green space reduces peak temperature by 0.4C
       Evidence: causal path found in your data, 3 supporting papers
       Simulation: increasing green space by 20% predicts -0.4C change
       Protocol: t-test, 64 samples, 6 week duration"
```

No GPT API keys. No GPU. No monthly subscription. Just Python, open data, and 8 AI agents working together.

## What It Does

Upload a CSV of your data (or just ask a question). HypoForge runs 8 AI agents in sequence:

| Agent | Job |
|-------|-----|
| Literature Scout | Searches arXiv for related papers |
| Data Analyst | Builds summary stats and discovers cause-effect relationships |
| Hypothesis Generator | Creates candidate hypotheses from data patterns + causal paths + literature gaps |
| Critic | Tests each hypothesis for flaws, fallacies, and ethical concerns |
| Evolver | Scores and ranks hypotheses by novelty, rigor, testability, and impact |
| Simulator | Predicts what happens if you change a variable (with confidence intervals) |
| Experiment Designer | Gives you a step-by-step protocol to test the hypothesis |
| Meta-Reviewer | Compiles everything into a full research report |

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Start the API server
uvicorn src.api.main:app --reload --port 8000

# Open the API docs
# -> http://localhost:8000/docs
```

Or run a pre-built example:

```bash
python examples/urban_climate.py
```

## Use It Your Way

**REST API** -- FastAPI backend with automatic Swagger docs. Call it from React, curl, Python, or any HTTP client. CORS enabled.

**Streamlit Dashboard** -- The old UI still works if you prefer a visual interface:

```bash
streamlit run src/ui/app.py
```

**Headless Mode** -- Run the pipeline from Python scripts and save reports to disk.

## What You Get

- Ranked hypotheses with 4 scores (novelty, rigor, testability, impact)
- Interactive causal graph showing cause-effect relationships
- Counterfactual simulations with 95% confidence intervals
- Experiment protocols with sample size and step-by-step procedure
- Full research report in Markdown (downloadable)

## Examples

```bash
python examples/urban_climate.py           # Green space, temperature, air quality
python examples/biodiversity_climate.py    # Species diversity, climate factors
python examples/health_environment.py      # Sleep quality, air pollution, noise
```

## Tech Stack

| Part | Technology |
|------|-----------|
| Agent pipeline | Python with Pydantic state |
| Literature search | arXiv API + Chroma vector DB |
| Causal discovery | PC algorithm (conditional independence + orientation) |
| ML simulation | RandomForest + bootstrap confidence intervals |
| REST API | FastAPI with Swagger docs |
| Frontend | Streamlit (old) / React (coming soon) |

## Requirements

- Python 3.10+
- Dependencies in `requirements.txt`
- Internet connection for arXiv lookups (optional for data-only runs)

## License

MIT
