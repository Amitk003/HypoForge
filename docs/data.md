# Working with Data

## Supported Formats

-   CSV (.csv)
-   Parquet (.parquet)

## Requirements

-   Data should be in tabular format (rows = observations, columns = variables)
-   Column names should be descriptive
-   Missing values are handled automatically

## How to Add Data

1.  Put your file in the `data/` folder
2.  Or use the file uploader in the Streamlit UI
3.  The Data Analyst agent will load and analyze it

## Tips for Good Results

-   More rows = better causal discovery and simulation
-   Include any columns that might be relevant to your research question
-   The system works best with 5+ numeric columns
-   Categorical columns are supported but work best with 2-10 categories each
