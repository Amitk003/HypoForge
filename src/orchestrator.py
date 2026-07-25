import traceback
import time
from src.state import HypothesisState
from src.agents.literature_scout import search_papers, format_papers_for_context
from src.agents.generator import generate_hypotheses
from src.agents.critic import critique_hypotheses
from src.agents.evolver import evolve_and_rank
from src.agents.experiment_designer import design_experiments
from src.agents.meta_reviewer import synthesize_review
from src.simulation.surrogate_sim import run_simulations
from src.data_engine import load_dataframe, summarize_dataframe
from src.causal.causal_discovery import build_graph_from_data


STAGE_NAMES = [
    ("literature_scout", "Literature Scout", "run_literature_scout"),
    ("data_analysis", "Data Analysis", "run_data_analysis"),
    ("hypothesis_generator", "Hypothesis Generator", "generate_hypotheses"),
    ("critic", "Critic", "critique_hypotheses"),
    ("evolver", "Evolver", "evolve_and_rank"),
    ("simulator", "Simulator", "run_simulations"),
    ("experiment_designer", "Experiment Designer", "design_experiments"),
    ("meta_reviewer", "Meta-Reviewer", "synthesize_review"),
]


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
    state.pipeline_stage_timings = {}

    stage_fns = {
        "run_literature_scout": run_literature_scout,
        "run_data_analysis": run_data_analysis,
        "generate_hypotheses": generate_hypotheses,
        "critique_hypotheses": critique_hypotheses,
        "evolve_and_rank": evolve_and_rank,
        "run_simulations": run_simulations,
        "design_experiments": design_experiments,
        "synthesize_review": synthesize_review,
    }

    for key, label, fn_name in STAGE_NAMES:
        t0 = time.time()
        fn = stage_fns[fn_name]
        try:
            state = fn(state)
        except Exception as e:
            state.errors.append(f"{label} failed: {traceback.format_exc()}")
        state.pipeline_stage_timings[key] = round(time.time() - t0, 2)

    state.pipeline_stage = "complete"
    return state
