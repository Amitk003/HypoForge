# Data Guide

## What Data Works Best

HypoForge works with CSV and Parquet files. For best results:

- At least 50 rows of data
- At least 5 numeric columns
- Column names that describe what they measure (like "temperature", "green_space_pct")
- No more than 50% missing values

## How to Prepare Your Data

1. Save your data as a CSV file
2. Make sure column names are clear (use underscores instead of spaces)
3. Remove columns that are just IDs or labels (like "city_name" or "participant_id") - these do not help causal discovery
4. Keep only the columns you want the system to analyze

## How Data Is Used

The pipeline uses your data in three ways:

1. **Summary statistics** -- The Data Analyst shows you row count, column types, missing values, and correlations
2. **Causal discovery** -- The PC algorithm finds cause-effect relationships between numeric variables
3. **Simulation** -- A RandomForest model is trained to predict what happens when you change a variable

## Data Without Column Headers

If your CSV has no header row, the system will use column names like "0", "1", "2" which produces poor results. Always use descriptive column names.

## No Data Mode

You can run HypoForge without any data. Just provide a research question. The system will search literature and generate hypotheses from what it finds. You will not get causal graphs or simulations without data.
