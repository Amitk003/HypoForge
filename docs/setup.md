# Setup Guide

## Requirements

-   Python 3.10 or higher
-   pip (Python package manager)

## Installation Steps

1.  Clone or download the repository:
    ```
    git clone <repo-url>
    cd hypoforge
    ```

2.  Install dependencies:
    ```
    pip install -r requirements.txt
    ```

3.  Run the app:
    ```
    streamlit run src/ui/app.py
    ```

## Configuration

You can set these environment variables in a `.env` file:

-   `OPENAI_API_KEY` - Optional. Used if you want to use GPT models for ranking.
-   `TAVILY_API_KEY` - Optional. Used for web search in the Literature Scout.

If you don't set these, the system uses local models and free APIs by default.

## Data

Place your CSV or Parquet files in the `data/` folder. The app has a file uploader in the UI, so you can also upload files directly.
