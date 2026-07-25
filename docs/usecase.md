# Use Cases

HypoForge works on any domain where you have a research question and optionally some data. Here are concrete scenarios.

## Urban Climate Research

**Goal**: Understand how green space affects temperature and air quality in cities

**Data needed**: CSV with columns like temperature, green space percentage, traffic density, building height, PM2.5

**What you get**:
- A causal graph showing how green space, traffic, and buildings connect to temperature and PM2.5
- Ranked hypotheses (e.g., "Increasing green space by 10% reduces peak temperature by X degrees")
- Counterfactual simulations showing predicted effects at different green space levels
- An experiment protocol for measuring these effects in a real neighborhood

**Example**: `python examples/urban_climate.py`

## Biodiversity and Climate Adaptation

**Goal**: Study how temperature and rainfall changes affect local wildlife

**Data needed**: CSV with columns like species count, annual temperature, rainfall, habitat area, human population

**What you get**:
- Causal links between climate variables and species richness
- Hypotheses about which factor matters most (habitat loss vs temperature vs rainfall)
- Simulations showing species count changes under different climate scenarios
- Field study protocol with sample size requirements

**Example**: `python examples/biodiversity_climate.py`

## Environmental Health

**Goal**: Investigate how air quality and noise affect sleep and heart health

**Data needed**: CSV with columns like sleep quality score, AQI exposure, noise level, physical activity, heart rate variability

**What you get**:
- Causal graph showing how environment factors connect to health outcomes
- Hypotheses about which environmental factor has the biggest health impact
- Counterfactual predictions (e.g., "If AQI drops by 20 points, sleep quality improves by X%")
- Wearable study protocol with recommended participant count

**Example**: `python examples/health_environment.py`

## Agriculture

**Goal**: Understand how soil properties and weather affect crop yield

**Data needed**: CSV with columns like yield, rainfall, soil nitrogen, temperature, pest count

**What you get**:
- Discovered causal relationships between soil, weather, and yield
- Testable hypotheses about intervention strategies
- Simulations of yield under different fertilizer or irrigation levels
- Field trial protocol

## Education Research

**Goal**: Study how class size and teaching method affect student performance

**Data needed**: CSV with columns like test scores, class size, hours of instruction, teacher experience, attendance rate

**What you get**:
- Causal graph of educational factors
- Hypotheses about which interventions work best
- Experiment protocol with control/treatment design

## Getting Started With Your Own Data

1. Prepare a CSV with numeric columns (at least 5 columns, at least 50 rows)
2. Think of a research question that involves two or more of your columns
3. Launch the dashboard: `streamlit run src/ui/app.py`
4. Upload your CSV and enter your question
5. Click "Run Pipeline"
