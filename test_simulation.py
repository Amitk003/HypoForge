import sys, os, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
import numpy as np
from src.state import HypothesisState, Hypothesis
from src.simulation.surrogate_sim import train_surrogate, counterfactual_predict, run_simulations
from src.agents.experiment_designer import design_experiments
from src.agents.meta_reviewer import synthesize_review
from src.orchestrator import run_pipeline


def create_test_csv():
    np.random.seed(42)
    df = pd.DataFrame({
        "temperature": np.random.randn(200) * 5 + 25,
        "green_space": np.random.rand(200) * 100,
        "pm25": np.random.randn(200) * 10 + 30 + 0.3 * np.random.randn(200),
        "traffic": np.random.rand(200) * 1000,
        "humidity": np.random.rand(200) * 30 + 40,
    })
    # Add some causal structure: green_space -> temperature, traffic -> pm25
    df["temperature"] = df["temperature"] - df["green_space"] * 0.03
    df["pm25"] = df["pm25"] + df["traffic"] * 0.01
    path = os.path.join(tempfile.gettempdir(), "test_simulation_data.csv")
    df.to_csv(path, index=False)
    return path


def test_train_surrogate():
    path = create_test_csv()
    df = pd.read_csv(path)
    model = train_surrogate(df, "temperature")
    assert model is not None
    assert "model" in model
    assert model["target_col"] == "temperature"
    print("test_train_surrogate PASSED")


def test_counterfactual():
    path = create_test_csv()
    df = pd.read_csv(path)
    model = train_surrogate(df, "temperature")
    result = counterfactual_predict(model, df, "green_space", 80.0)
    assert result is not None
    assert result.intervention_variable == "green_space"
    assert result.delta is not None
    print("test_counterfactual PASSED")


def test_run_simulations():
    path = create_test_csv()
    h = Hypothesis(id="s1", title="Green space cools temperature", core_statement="Increasing green space reduces temperature in urban areas.", novelty_score=0.7, testability_score=0.8, causal_rigor_score=0.6, impact_score=0.7)
    state = HypothesisState(research_goal="Test", data_path=path, hypotheses=[h])
    result = run_simulations(state)
    assert result.pipeline_stage == "simulation_complete"
    print("test_run_simulations PASSED")


def test_design_experiments():
    h1 = Hypothesis(id="e1", title="Test hypothesis", core_statement="Temperature affects humidity levels in urban environments.", novelty_score=0.7, testability_score=0.8, causal_rigor_score=0.6, impact_score=0.7)
    h2 = Hypothesis(id="e2", title="Lower", core_statement="Noise.", novelty_score=0.1, testability_score=0.1, causal_rigor_score=0.1, impact_score=0.1)
    state = HypothesisState(hypotheses=[h2, h1])
    result = design_experiments(state)
    assert len(result.protocols) > 0
    assert result.protocols[0].required_sample_size > 0
    print("test_design_experiments PASSED")


def test_synthesize_review():
    h1 = Hypothesis(id="r1", title="Top hypothesis", core_statement="Green space reduces temperature.", novelty_score=0.9, testability_score=0.8, causal_rigor_score=0.7, impact_score=0.8)
    h2 = Hypothesis(id="r2", title="Low", core_statement="Nothing.", novelty_score=0.1, testability_score=0.1, causal_rigor_score=0.1, impact_score=0.1)
    state = HypothesisState(research_goal="How does green space affect temperature?", hypotheses=[h2, h1])
    result = synthesize_review(state)
    assert result.pipeline_stage == "review_synthesized"
    assert "Meta-Review" in result.literature_context[-1]
    print("test_synthesize_review PASSED")


def test_end_to_end_simulation():
    path = create_test_csv()
    state = HypothesisState(research_goal="How does green space affect temperature in cities?", data_path=path)
    result = run_pipeline(state)
    assert result.pipeline_stage == "complete"
    assert len(result.hypotheses) > 0
    print("test_end_to_end_simulation PASSED")


if __name__ == "__main__":
    test_train_surrogate()
    test_counterfactual()
    test_run_simulations()
    test_design_experiments()
    test_synthesize_review()
    test_end_to_end_simulation()
    print("\nAll simulation tests passed.")
