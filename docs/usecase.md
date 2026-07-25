# Use Cases

Here are real-world examples of what you can do with HypoForge.

## Urban Climate Research

**Question:** How does urban green space affect local air temperature and air quality?

**Data needed:** CSV with columns like green_space_pct, temperature, pm25, traffic_density for different city areas.

**What you get:**
- A causal graph showing if green space directly cools temperature
- Ranked hypotheses with supporting evidence
- Counterfactual simulation: what happens to temperature if you increase green space by 20%?
- An experiment protocol to test the findings

**Run it:**

```bash
python examples/urban_climate.py
```

## Biodiversity and Climate

**Question:** How do changes in temperature and rainfall affect species diversity?

**Data needed:** CSV with columns like species_richness, temperature, rainfall, elevation for different locations.

**What you get:**
- Causal relationships between climate factors and biodiversity
- Ranked hypotheses about which factor matters most
- Simulated scenarios for different climate conditions

**Run it:**

```bash
python examples/biodiversity_climate.py
```

## Environmental Health

**Question:** Does air quality and noise pollution affect sleep quality and stress levels?

**Data needed:** CSV with columns like sleep_quality, stress_score, pm25, noise_level, exercise_hours.

**What you get:**
- Discovered confounders (hidden factors like exercise that affect both)
- Testable hypotheses with safety flags
- Experiment protocol with specific measurements

**Run it:**

```bash
python examples/health_environment.py
```

## Agriculture

**Question:** How do soil nutrients and water availability affect crop yield?

**Data needed:** CSV with columns like yield, nitrogen, phosphorus, rainfall, temperature for different plots.

**What you get:**
- Causal graph showing direct vs indirect effects
- Counterfactual: what yield would be with more nitrogen?
- Experiment design with recommended sample size

## Education Research

**Question:** How do class size and teaching method affect student performance?

**Data needed:** CSV with columns like test_score, class_size, teaching_method, study_hours, parent_education.

**What you get:**
- Identified confounders (like study hours)
- Ranked hypotheses with critique notes
- Protocol for a controlled experiment
