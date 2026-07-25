import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
import numpy as np
import tempfile
import os
from src.state import HypothesisState
from src.orchestrator import run_pipeline
from src.data_engine import load_dataframe, summarize_dataframe
from src.causal.causal_discovery import build_graph_from_data
from src.agents.generator import generate_hypotheses
from src.agents.critic import critique_hypotheses
from src.agents.evolver import evolve_and_rank, composite_score
from src.simulation.surrogate_sim import train_surrogate, counterfactual_predict, run_simulations
from src.agents.experiment_designer import design_experiments
from src.agents.meta_reviewer import synthesize_review


def create_test_dataset() -> str:
    np.random.seed(42)
    n = 200
    green_space = np.random.rand(n) * 100
    traffic = np.random.rand(n) * 1000
    df = pd.DataFrame({
        "temperature": np.random.randn(n) * 2 + 25 - green_space * 0.08,
        "green_space": green_space,
        "pm25": np.random.randn(n) * 5 + 30 + traffic * 0.015 + green_space * 0.02,
        "traffic": traffic,
        "humidity": np.random.randn(n) * 30 + 40,
    })
    path = os.path.join(tempfile.gettempdir(), "hypoforge_test_data.csv")
    df.to_csv(path, index=False)
    return path


def test_data_loading():
    path = create_test_dataset()
    df = load_dataframe(path)
    assert df is not None
    assert df.shape[0] == 200
    print("PASS: test_data_loading")


def test_eda_summary():
    path = create_test_dataset()
    df = load_dataframe(path)
    summary = summarize_dataframe(df)
    assert "Shape: 200 rows" in summary
    assert "High correlations" in summary
    print("PASS: test_eda_summary")


def test_causal_discovery():
    path = create_test_dataset()
    df = load_dataframe(path)
    dag = build_graph_from_data(df)
    assert len(dag.nodes) >= 4
    assert len(dag.edges) > 0
    assert dag.dot_source != ""
    print("PASS: test_causal_discovery")


def test_hypothesis_generation():
    state = HypothesisState(research_goal="How does green space affect temperature?")
    result = generate_hypotheses(state)
    assert len(result.hypotheses) > 0
    print("PASS: test_hypothesis_generation")


def test_critique():
    state = HypothesisState(research_goal="Test")
    state = generate_hypotheses(state)
    result = critique_hypotheses(state)
    assert len(result.debate_log) > 0
    print("PASS: test_critique")


def test_evolution():
    state = HypothesisState(research_goal="Test")
    state = generate_hypotheses(state)
    state = critique_hypotheses(state)
    result = evolve_and_rank(state)
    assert len(result.hypotheses) > 0
    scores = [composite_score(h) for h in result.hypotheses]
    assert scores == sorted(scores, reverse=True)
    print("PASS: test_evolution")


def test_simulation():
    path = create_test_dataset()
    df = load_dataframe(path)
    model = train_surrogate(df, "temperature")
    assert model is not None
    result = counterfactual_predict(model, df, "green_space", 80.0)
    assert result is not None
    assert result.delta is not None
    print("PASS: test_simulation")


def test_experiment_design():
    h = HypothesisState(research_goal="Test")
    h = generate_hypotheses(h)
    result = design_experiments(h)
    assert len(result.protocols) > 0
    print("PASS: test_experiment_design")


def test_meta_review():
    state = HypothesisState(research_goal="How does green space affect temperature?")
    state = generate_hypotheses(state)
    result = synthesize_review(state)
    assert "Meta-Review" in result.meta_review_report
    print("PASS: test_meta_review")


def test_end_to_end():
    path = create_test_dataset()
    state = HypothesisState(
        research_goal="How does urban green space affect local air temperature?",
        data_path=path,
    )
    result = run_pipeline(state)
    assert result.pipeline_stage == "complete"
    assert len(result.hypotheses) > 0
    assert result.meta_review_report != ""
    print("PASS: test_end_to_end")


def test_edge_case_no_data():
    state = HypothesisState(research_goal="What factors influence urban heat island intensity?")
    result = run_pipeline(state)
    assert result.pipeline_stage == "complete"
    assert len(result.hypotheses) > 0
    print("PASS: test_edge_case_no_data")


def test_edge_case_empty_goal():
    state = HypothesisState(research_goal="")
    result = run_pipeline(state)
    assert result.pipeline_stage == "complete"
    print("PASS: test_edge_case_empty_goal")


if __name__ == "__main__":
    tests = [
        test_data_loading,
        test_eda_summary,
        test_causal_discovery,
        test_hypothesis_generation,
        test_critique,
        test_evolution,
        test_simulation,
        test_experiment_design,
        test_meta_review,
        test_end_to_end,
        test_edge_case_no_data,
        test_edge_case_empty_goal,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"FAIL: {t.__name__} - {e}")
            failed += 1
    print(f"\n{passed}/{passed + failed} tests passed.")
    if failed > 0:
        exit(1)
