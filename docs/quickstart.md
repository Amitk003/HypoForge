# Quick Start Guide

This guide gets you from zero to running HypoForge in 5 minutes.

## Step 1: Install

Open a terminal and run:

```bash
pip install -r requirements.txt
```

This installs all required packages.

## Step 2: Generate Sample Data

```bash
python examples/urban_climate.py
```

This creates sample climate data in `data/urban_climate_sample.csv` and runs the pipeline once to show you the output.

## Step 3: Launch the Dashboard

```bash
streamlit run src/ui/app.py
```

Your browser opens to the HypoForge dashboard.

## Step 4: Run Your First Pipeline

In the dashboard:

1. Click "Browse files" and select `data/urban_climate_sample.csv`
2. In the Research Goal box, type: `How does urban green space affect air temperature and PM2.5?`
3. Click "Run Pipeline"

The pipeline takes 10-30 seconds. When done, explore the tabs:

- **Ranked Hypotheses** -- Click on a hypothesis to see its scores and supporting evidence
- **Causal Graph & Simulator** -- See the discovered graph. Select a target variable and intervention variable, then drag the slider to simulate what-if scenarios
- **Report & Export** -- Download the full research proposal

## Step 5: Try Your Own Data

Replace the sample CSV with your own data. The system works best with:

- CSV files with numeric columns
- At least 50 rows
- Column names that describe what they measure

## What If Something Goes Wrong?

See `docs/troubleshooting.md` for common issues and fixes.
