# Setup Guide

## Requirements

- Python 3.10 or higher
- pip (Python package manager)

## Installation

1. Open a terminal in the project folder.

2. Install all required packages:

```bash
pip install -r requirements.txt
```

3. (Optional) If you want better paper search, install sentence-transformers. It downloads a small AI model for finding similar papers:

```bash
pip install sentence-transformers
```

## Run the API Server (For New Frontend)

```bash
uvicorn src.api.main:app --reload --port 8000
```

The API is now available at `http://localhost:8000`. Open `http://localhost:8000/docs` to see the interactive API documentation.

## Run the React Frontend

```bash
cd frontend && npm run dev
```

Opens at `http://localhost:5173`. Vite proxies API calls to `http://localhost:8000`.

## Environment Variables (Optional)

Create a `.env` file in the project root to set these:

- `OPENAI_API_KEY` - Only needed if you want to use GPT models. Not required for the default setup.
- `TAVILY_API_KEY` - Only needed for web search in the Literature Scout. Not required.

If you do not set these, the system uses free local models and the arXiv API.

## Data

Place your CSV or Parquet files in the `data/` folder. The API accepts file uploads, so you can also send data directly through the API endpoints.
