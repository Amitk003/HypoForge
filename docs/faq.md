# Frequently Asked Questions

## General

**What is HypoForge?**
An open-source AI system that takes a research question and optional data, then generates ranked scientific hypotheses with experiment designs.

**Do I need to know programming?**
You need to know basic terminal commands to install and run it. The API can be used from any programming language or tool.

**Do I need a GPU?**
No. Everything runs on CPU.

**Do I need an internet connection?**
Yes, for arXiv paper lookups. The pipeline works without internet if you only use your own data.

## Data

**What kind of data works best?**
CSV files with 50+ rows and 5+ numeric columns. Column names should describe what they measure (like "temperature", "green_space_pct").

**Can I use data without column names?**
Not really. The system uses column names to match variables in hypotheses. Clear names give better results.

**What if I have no data?**
The system still runs. It searches literature and generates hypotheses from your research goal alone.

## Technical

**How does the causal discovery work?**
It uses the PC algorithm. This checks if pairs of variables are statistically independent. Then it finds the direction of cause-effect using orientation rules.

**How are hypotheses scored?**
Four scores from 0 to 1: novelty (is it new?), causal rigor (strong cause-effect evidence?), testability (can we test it?), impact (does it matter?). The composite score is the average.

**What ML model is used for simulation?**
RandomForest from scikit-learn. It is fast and works well with small datasets.

**Can I use my own ML model?**
Not currently. The simulation agent uses RandomForest internally.

## Errors

**The pipeline ran but I got 0 hypotheses.**
This often means the research goal was too short or generic. Try a more specific question with more details.

**The causal graph is empty.**
The data needs at least 2 numeric columns with enough variation. Check that your CSV loaded correctly.

**The simulation says "Could not train model".**
You need at least 10 complete rows (no missing values) with numeric columns.

## API

**How do I start the API server?**
```bash
uvicorn src.api.main:app --reload --port 8000
```

**Where is the API documentation?**
Open `http://localhost:8000/docs` in your browser after starting the server.

**Can I use the API from JavaScript?**
Yes. The API has CORS enabled. You can call it from any web frontend.
