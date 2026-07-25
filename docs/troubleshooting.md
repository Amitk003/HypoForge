# Troubleshooting

## ModuleNotFoundError: No module named 'src'

**Problem**: Python cannot find the source code

**Fix**: Run commands from the project root folder and add the path at the top of your script:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
```

For the dashboard, this is already handled in `src/ui/app.py`. Just run:

```bash
cd hypoforge
streamlit run src/ui/app.py
```

## ImportError: No module named 'chromadb' / 'sentence_transformers'

**Problem**: Missing optional dependencies

**Fix**: Install them:

```bash
pip install chromadb sentence-transformers
```

The system works without these -- it falls back to basic arXiv search without semantic ranking.

## No hypotheses generated / Only 1 hypothesis

**Problem**: The system needs specific domain nouns in your research goal

**Fix**: Use concrete language. Instead of "What is the effect of the environment on health?", try "How does air pollution affect sleep quality?" Include variable names that could match column names in your data.

## No simulations shown

**Problem**: Simulations need numeric data to train the ML model

**Fix**: Upload a CSV with at least 50 rows and 5+ numeric columns. The last numeric column is used as the target variable.

## Causal graph is empty

**Problem**: The PC algorithm needs enough data to find correlations

**Fix**: Upload data with at least 50 rows and 3+ numeric columns. Strong correlations between variables produce better graphs.

## arXiv API returns no papers

**Problem**: arXiv might be slow or your query might be too specific

**Fix**: The system returns results even without papers (it creates "literature gap" hypotheses). Try shorter queries with fewer stop words.

## Dashboard shows "No data loaded"

**Problem**: The CSV was not uploaded properly

**Fix**: Use the file uploader in the Research Setup tab. Supported formats: CSV (.csv) and Parquet (.parquet). Column names should be descriptive without special characters.

## Pipeline is slow

**Problem**: Some steps take time (arXiv API, ML training, Chroma indexing)

**Fix**: This is normal. The pipeline runs 8 agents sequentially. Most time is spent on arXiv lookups (network) and embedding papers (first run downloads the model).

## Error: "Cannot connect to ChromaDB"

**Problem**: Chroma might be locked from a previous run

**Fix**: Delete the `chroma_db/` folder and retry:

```bash
rm -rf chroma_db/
```
