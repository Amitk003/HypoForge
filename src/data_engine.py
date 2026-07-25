import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional


def load_dataframe(path: Optional[str] = None, uploaded_file=None) -> Optional[pd.DataFrame]:
    if uploaded_file is not None:
        name = uploaded_file.name
        if name.endswith(".csv"):
            return pd.read_csv(uploaded_file)
        elif name.endswith(".parquet"):
            return pd.read_parquet(uploaded_file)
    if path is not None:
        p = Path(path)
        if p.suffix == ".csv":
            return pd.read_csv(p)
        elif p.suffix == ".parquet":
            return pd.read_parquet(p)
    return None


def summarize_dataframe(df: pd.DataFrame) -> str:
    if df is None:
        return "No data loaded."

    lines = []
    lines.append(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    lines.append("")

    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    lines.append(f"Numeric columns ({len(num_cols)}): {', '.join(num_cols[:10])}")
    if len(num_cols) > 10:
        lines[-1] += f" ... and {len(num_cols) - 10} more"
    lines.append(f"Categorical columns ({len(cat_cols)}): {', '.join(cat_cols[:10])}")
    if len(cat_cols) > 10:
        lines[-1] += f" ... and {len(cat_cols) - 10} more"
    lines.append("")

    lines.append("Missing values:")
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if len(missing) > 0:
        for col, val in missing.items():
            lines.append(f"  {col}: {val} missing ({100 * val / len(df):.1f}%)")
    else:
        lines.append("  None")
    lines.append("")

    lines.append("Numeric summary:")
    if num_cols:
        lines.append(df[num_cols].describe().to_string())
    lines.append("")

    corr = df.select_dtypes(include=[np.number]).corr()
    high_corr = []
    for i in range(len(corr.columns)):
        for j in range(i + 1, len(corr.columns)):
            val = corr.iloc[i, j]
            if abs(val) > 0.7:
                high_corr.append(f"  {corr.columns[i]} <-> {corr.columns[j]}: {val:.3f}")
    if high_corr:
        lines.append("High correlations (|r| > 0.7):")
        lines.extend(high_corr[:10])
    else:
        lines.append("No high correlations found.")

    return "\n".join(lines)
