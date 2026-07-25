# Troubleshooting

Common issues and how to fix them.

## ImportError: No module named 'src'

**Problem:** You ran a script from the wrong folder.

**Fix:** Always run commands from the project root folder (where `src/` and `requirements.txt` are).

Or add the project root to your Python path:

```bash
$env:PYTHONPATH = "$pwd"
```

## ModuleNotFoundError: No module named 'fastapi'

**Problem:** Missing dependencies.

**Fix:** Install all required packages:

```bash
pip install -r requirements.txt
```

## Pipeline runs but no hypotheses are generated

**Problem:** The research goal is too short or the generator could not find enough content.

**Fix:** Write a more specific research goal. Include the variables you care about. For example, instead of "How does the environment affect health?", write "How does air pollution (PM2.5) and green space affect sleep quality and stress levels in urban areas?"

## Causal graph is empty

**Problem:** Not enough numeric data for the PC algorithm.

**Fix:** Make sure your data has at least 2 numeric columns with 50+ rows. Check that your CSV is loading correctly by looking at the data preview.

## Simulation failed

**Problem:** The ML model could not be trained.

**Fix:** Check that:
- Your data has at least 10 complete rows (no missing values)
- The target variable is numeric
- There are other numeric columns to use as features

## ChromaDB lock error

**Problem:** The vector database gets corrupted if multiple processes try to write to it.

**Fix:** Delete the chroma_db folder and restart:

```bash
Remove-Item -Recurse -Force chroma_db
```

## Port already in use

**Problem:** Another application is using port 8000 or 8501.

**Fix 1:** Find and stop the process using the port:

```bash
# For port 8501
Get-Process -Id (Get-NetTCPConnection -LocalPort 8501).OwningProcess | Stop-Process -Force

# For port 8000
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
```

**Fix 2:** Use a different port:

```bash
uvicorn src.api.main:app --port 8001
```

## Slow pipeline

The pipeline does 8 tasks in sequence. Literature search and causal discovery take the most time. Expect 10-30 seconds for a full run with data. Without data it is faster.
