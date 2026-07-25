# Quick Start Guide

Get from zero to running HypoForge in 5 minutes.

## Step 1: Install

Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

This installs all the packages HypoForge needs.

## Step 2: Run the Pipeline (Headless)

Generate sample data and run the pipeline without any UI:

```bash
python examples/urban_climate.py
```

This creates sample data and runs the full pipeline. A report file is saved to disk.

## Step 3: Start the API Server (Recommended)

For the new frontend (or any HTTP client), start the FastAPI backend:

```bash
uvicorn src.api.main:app --reload --port 8000
```

Open `http://localhost:8000/docs` in your browser. You will see the interactive Swagger UI with all available endpoints.

## Step 4: Quick API Test

Using the Swagger docs page (http://localhost:8000/docs):

1. Click on `POST /api/pipeline`
2. Click "Try it out"
3. In `research_goal` field, type: `How does urban green space affect temperature?`
4. Click "Execute"
5. Copy the `run_id` from the response

Then use the `run_id` to call `GET /api/runs/{run_id}/hypotheses` to see the results.

## Step 5: Open the React Frontend

```bash
cd frontend && npm run dev
```

Then open `http://localhost:5173` in your browser. Enter a research goal, upload data (optional), and click "Run Pipeline".

## What If Something Goes Wrong?

Check `docs/troubleshooting.md` for common issues and fixes.
