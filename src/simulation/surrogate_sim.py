import pandas as pd
import numpy as np
from typing import Optional
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from src.state import HypothesisState, SimulationResult


def train_surrogate(df: pd.DataFrame, target_col: str) -> Optional[object]:
    if target_col not in df.columns:
        return None
    num_df = df.select_dtypes(include=[np.number]).dropna()
    if target_col not in num_df.columns:
        return None
    X = num_df.drop(columns=[target_col])
    y = num_df[target_col]
    if X.shape[1] < 1 or len(y) < 10:
        return None
    is_classification = y.nunique() < 10
    model = RandomForestClassifier if is_classification else RandomForestRegressor
    clf = model(n_estimators=100, random_state=42, n_jobs=-1)
    clf.fit(X, y)
    return {"model": clf, "feature_cols": X.columns.tolist(), "target_col": target_col, "is_classification": is_classification}


def counterfactual_predict(model_dict: dict, df: pd.DataFrame, intervention_var: str, intervention_value: float) -> Optional[SimulationResult]:
    if model_dict is None:
        return None
    feature_cols = model_dict["feature_cols"]
    target_col = model_dict["target_col"]
    if intervention_var not in feature_cols:
        return None
    model = model_dict["model"]
    num_df = df.select_dtypes(include=[np.number]).dropna()
    X = num_df[feature_cols]

    baseline_preds = model.predict(X)
    baseline_mean = float(np.mean(baseline_preds))

    X_perturbed = X.copy()
    X_perturbed[intervention_var] = intervention_value
    perturbed_preds = model.predict(X_perturbed)
    perturbed_mean = float(np.mean(perturbed_preds))

    n_bootstrap = 50
    deltas = []
    n = len(X)
    for _ in range(n_bootstrap):
        idx = np.random.randint(0, n, n)
        X_boot = X.iloc[idx]
        X_pert = X_boot.copy()
        X_pert[intervention_var] = intervention_value
        boot_baseline = np.mean(model.predict(X_boot))
        boot_perturbed = np.mean(model.predict(X_pert))
        deltas.append(boot_perturbed - boot_baseline)
    ci_lower = float(np.percentile(deltas, 2.5))
    ci_upper = float(np.percentile(deltas, 97.5))

    return SimulationResult(
        target_variable=target_col,
        intervention_variable=intervention_var,
        intervention_value=intervention_value,
        predicted_outcome=round(perturbed_mean, 4),
        baseline_outcome=round(baseline_mean, 4),
        delta=round(perturbed_mean - baseline_mean, 4),
        ci_lower=round(ci_lower, 4),
        ci_upper=round(ci_upper, 4),
    )


def run_simulations(state: HypothesisState) -> HypothesisState:
    if not state.data_path:
        state.pipeline_stage = "simulation_complete"
        return state
    try:
        from src.data_engine import load_dataframe
        df = load_dataframe(state.data_path)
        if df is None:
            return state
        target_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if not target_cols:
            return state
        target = target_cols[-1]
        model_dict = train_surrogate(df, target)
        if model_dict is None:
            return state

        # Run counterfactual for each top hypothesis
        for h in state.top_hypotheses:
            words = h.core_statement.lower().split()
            for col in model_dict["feature_cols"]:
                if col.lower() in words or col.lower().replace("_", " ") in " ".join(words):
                    baseline_val = float(df[col].mean())
                    perturbed_val = baseline_val * 1.2
                    result = counterfactual_predict(model_dict, df, col, perturbed_val)
                    if result:
                        result.hypothesis_id = h.id
                        state.simulations.append(result)
                        break
    except Exception:
        pass
    state.pipeline_stage = "simulation_complete"
    return state
