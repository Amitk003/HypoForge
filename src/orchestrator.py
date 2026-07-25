import traceback
from src.state import HypothesisState
from src.agents.literature_scout import search_papers, format_papers_for_context
from src.agents.generator import generate_hypotheses
from src.agents.critic import critique_hypotheses
from src.agents.evolver import evolve_and_rank
from src.data_engine import load_dataframe, summarize_dataframe
from src.causal.causal_discovery import build_graph_from_data


def run_literature_scout(state: HypothesisState) -> HypothesisState:
    try:
        papers = search_papers(state.research_goal)
        state.literature_context = [format_papers_for_context(papers)]
    except Exception as e:
        state.errors.append(f"Literature scout failed: {e}\n{traceback.format_exc()}")
        state.literature_context = ["Literature search unavailable."]
    state.pipeline_stage = "literature_complete"
    return state


def run_data_analysis(state: HypothesisState) -> HypothesisState:
    if state.data_path:
        try:
            df = load_dataframe(state.data_path)
            if df is not None:
                state.dataframe_summary = summarize_dataframe(df)
                state.causal_graph = build_graph_from_data(df)
        except Exception as e:
            state.errors.append(f"Data analysis failed: {e}\n{traceback.format_exc()}")
            state.dataframe_summary = "Data could not be analyzed."
    state.pipeline_stage = "data_analysis_complete"
    return state


def run_pipeline(state: HypothesisState) -> HypothesisState:
    state.pipeline_stage = "running"
    state.errors = []

    state = run_literature_scout(state)
    state = run_data_analysis(state)
    state = generate_hypotheses(state)
    state = critique_hypotheses(state)
    state = evolve_and_rank(state)

    state.pipeline_stage = "complete"
    return state
