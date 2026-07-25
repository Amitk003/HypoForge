import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

from src.data_engine import load_dataframe
from src.simulation.surrogate_sim import train_surrogate, counterfactual_predict


def render_simulator(csv_path: str | None):
    st.subheader("Counterfactual Simulator")
    if csv_path and Path(csv_path).exists():
        df = load_dataframe(csv_path)
        if df is not None:
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if not num_cols:
                st.info("No numeric columns found in dataset.")
                return

            col_left, col_right = st.columns([3, 2])
            with col_left:
                target_col = st.selectbox("Target variable", num_cols, key="sim_target")
                intervention_col = st.selectbox(
                    "Intervention variable",
                    [c for c in num_cols if c != target_col],
                    key="sim_intervention",
                )
            with col_right:
                baseline = float(df[intervention_col].mean())
                st.metric("Baseline", f"{baseline:.2f}")
                perturbed = st.slider(
                    f"Set value for {intervention_col}",
                    min_value=float(df[intervention_col].min()),
                    max_value=float(df[intervention_col].max()),
                    value=baseline,
                    step=round(float(df[intervention_col].std()) / 10, 2),
                )

            model = train_surrogate(df, target_col)
            if model:
                result = counterfactual_predict(model, df, intervention_col, perturbed)
                if result:
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Predicted Outcome", f"{result.predicted_outcome:.4f}" if result.predicted_outcome else "N/A")
                    c2.metric("Delta from Baseline", f"{result.delta:+.4f}" if result.delta else "N/A")
                    if result.ci_lower is not None and result.ci_upper is not None:
                        c3.metric("95% CI", f"[{result.ci_lower:.4f}, {result.ci_upper:.4f}]")
    else:
        st.info("Upload a dataset with numeric variables to run counterfactual simulations.")
