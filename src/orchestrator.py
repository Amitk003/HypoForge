from typing import Optional
from src.state import HypothesisState


def run_pipeline(state: HypothesisState) -> HypothesisState:
    state.pipeline_stage = "running"
    errors = []

    # Stage 1: Literature search
    try:
        from src.agents.literature_scout import search_papers, format_papers_for_context
        papers = search_papers(state.research_goal)
        state.literature_context = [format_papers_for_context(papers)]
    except Exception as e:
        errors.append(f"Literature scout failed: {e}")
        state.literature_context = ["Literature search unavailable."]

    # Stage 2: Data analysis
    if state.data_path:
        try:
            from src.data_engine import load_dataframe, summarize_dataframe
            from src.causal.causal_discovery import build_graph_from_data
            df = load_dataframe(state.data_path)
            if df is not None:
                state.dataframe_summary = summarize_dataframe(df)
                state.causal_graph = build_graph_from_data(df)
        except Exception as e:
            errors.append(f"Data analysis failed: {e}")
            state.dataframe_summary = "Data could not be analyzed."

    state.errors = errors
    state.pipeline_stage = "literature_and_data_complete"
    return state
