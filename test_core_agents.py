import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.state import Hypothesis, HypothesisState, CausalGraphData, CausalEdge
from src.agents.generator import generate_hypotheses, extract_anomalies, extract_causal_paths
from src.agents.critic import critique_hypotheses
from src.agents.evolver import evolve_and_rank, composite_score
from src.orchestrator import run_pipeline


def test_generator_creates_hypotheses():
    state = HypothesisState(research_goal="How does green space affect urban temperature?")
    state.literature_context = ["Relevant papers found:\n1. Urban heat island effect\n2. Green space cooling"]
    result = generate_hypotheses(state)
    assert len(result.hypotheses) > 0
    assert all(h.core_statement for h in result.hypotheses)
    print("test_generator_creates_hypotheses PASSED")


def test_generator_uses_causal_graph():
    cg = CausalGraphData(
        nodes=["temperature", "green_space", "pm25"],
        edges=[
            CausalEdge(source="green_space", target="temperature"),
            CausalEdge(source="temperature", target="pm25"),
        ],
        dot_source="digraph {}"
    )
    state = HypothesisState(
        research_goal="How does green space affect temperature?",
        causal_graph=cg,
    )
    result = generate_hypotheses(state)
    assert len(result.hypotheses) > 0
    print("test_generator_uses_causal_graph PASSED")


def test_critique_adds_notes():
    h = Hypothesis(
        id="test-1",
        title="Test hypothesis",
        core_statement="Temperature increases cause higher pollution.",
        proposed_mechanism="",
        supporting_evidence=[],
    )
    state = HypothesisState(hypotheses=[h])
    result = critique_hypotheses(state)
    assert len(result.hypotheses[0].critique_notes) > 0
    print("test_critique_adds_notes PASSED")


def test_evolver_ranks_by_score():
    h1 = Hypothesis(id="a", title="A", core_statement="H1", novelty_score=0.9, testability_score=0.9, causal_rigor_score=0.9, impact_score=0.9)
    h2 = Hypothesis(id="b", title="B", core_statement="H2", novelty_score=0.1, testability_score=0.1, causal_rigor_score=0.1, impact_score=0.1)
    state = HypothesisState(hypotheses=[h2, h1])
    result = evolve_and_rank(state)
    assert result.hypotheses[0].id == "a"
    assert result.hypotheses[-1].id == "b"
    print("test_evolver_ranks_by_score PASSED")


def test_evolver_creates_children():
    h1 = Hypothesis(id="a", title="Temp hypothesis", core_statement="Temperature affects X.", proposed_mechanism="Heat mechanism", supporting_evidence=["Paper 1"], novelty_score=0.7, testability_score=0.7, causal_rigor_score=0.7, impact_score=0.7)
    h2 = Hypothesis(id="b", title="Green hypothesis", core_statement="Green space affects Y.", proposed_mechanism="Cooling mechanism", supporting_evidence=["Paper 2"], novelty_score=0.6, testability_score=0.6, causal_rigor_score=0.6, impact_score=0.6)
    state = HypothesisState(hypotheses=[h1, h2])
    result = evolve_and_rank(state)
    assert len(result.hypotheses) >= 2
    assert any("Evolved" in h.title for h in result.hypotheses)
    print("test_evolver_creates_children PASSED")


def test_end_to_end_pipeline():
    state = HypothesisState(research_goal="How does urban green space affect local temperature?")
    result = run_pipeline(state)
    assert result.pipeline_stage == "complete"
    assert len(result.hypotheses) > 0
    scores = [composite_score(h) for h in result.hypotheses]
    assert scores == sorted(scores, reverse=True)
    print("test_end_to_end_pipeline PASSED")


if __name__ == "__main__":
    test_generator_creates_hypotheses()
    test_generator_uses_causal_graph()
    test_critique_adds_notes()
    test_evolver_ranks_by_score()
    test_evolver_creates_children()
    test_end_to_end_pipeline()
    print("\nAll core-agents tests passed.")
