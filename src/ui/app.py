import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import pandas as pd
import os

from src.orchestrator import run_pipeline
from src.state import HypothesisState
from src.data_engine import load_dataframe
from src.ui.styles import CUSTOM_CSS, FONT_LINK
from src.ui.components.header import render_header
from src.ui.components.empty_state import render_empty_state
from src.ui.components.error_card import render_errors
from src.ui.components.score_pill import render_score_pills
from src.ui.components.pipeline_stepper import render_stepper, render_stage_detail, render_activity_log
from src.ui.components.hypothesis_card import render_hypothesis_card, render_sort_filter, apply_sort_filter
from src.ui.components.causal_graph import render_graph
from src.ui.components.simulator import render_simulator
from src.ui.components.report import render_report


st.set_page_config(page_title="HypoForge", layout="wide")
st.markdown(FONT_LINK + "<style>" + CUSTOM_CSS + "</style>", unsafe_allow_html=True)

UPLOAD_DIR = Path(__file__).parent.parent.parent / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

if "state" not in st.session_state:
    st.session_state.state = HypothesisState()
if "pipeline_run" not in st.session_state:
    st.session_state.pipeline_run = False
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None
if "saved_csv_path" not in st.session_state:
    st.session_state.saved_csv_path = None


render_header(
    st.session_state.state.research_goal
    if st.session_state.pipeline_run and st.session_state.state.research_goal
    else ""
)

tab_setup, tab_pipeline, tab_hypotheses, tab_causal, tab_report = st.tabs([
    "Setup", "Pipeline", "Hypotheses", "Causal & Simulation", "Report"
])


with tab_setup:
    col1, col2 = st.columns([2, 1])

    with col1:
        research_goal = st.text_area(
            "Research Goal",
            placeholder="e.g. How does urban green space affect local air temperature and air quality?",
            height=120,
        )

        uploaded_file = st.file_uploader("Upload data (CSV or Parquet)", type=["csv", "parquet"])

        with st.expander("Advanced Settings"):
            alpha = st.number_input("Significance level (alpha)", min_value=0.001, max_value=0.5, value=0.05, step=0.001, format="%.3f")
            max_hypotheses = st.number_input("Max hypotheses", min_value=1, max_value=50, value=10, step=1)

        run_btn = st.button("Run Pipeline", type="primary", use_container_width=True)

    with col2:
        if uploaded_file is not None:
            st.session_state.uploaded_data = uploaded_file
            try:
                df = load_dataframe(uploaded_file=uploaded_file)
                if df is not None:
                    st.subheader("Data Preview")
                    st.dataframe(df.head(), use_container_width=True, height=150)
                    st.caption(f"{df.shape[0]} rows x {df.shape[1]} columns")
            except Exception as e:
                st.error(f"Could not load file: {e}")
        elif st.session_state.state.dataframe_summary:
            st.subheader("Data Summary")
            st.text(st.session_state.state.dataframe_summary[:500])

    if run_btn and research_goal:
        data_path = None
        if st.session_state.uploaded_data is not None:
            saved_file_path = UPLOAD_DIR / st.session_state.uploaded_data.name
            with open(saved_file_path, "wb") as f:
                f.write(st.session_state.uploaded_data.getvalue())
            data_path = str(saved_file_path)
            st.session_state.saved_csv_path = data_path

        state = HypothesisState(
            research_goal=research_goal,
            data_path=data_path,
        )

        with st.spinner("Running multi-agent pipeline..."):
            result = run_pipeline(state)

        st.session_state.state = result
        st.session_state.pipeline_run = True
        st.success("Pipeline complete!")

    if st.session_state.pipeline_run:
        state = st.session_state.state
        st.subheader("Last Run Summary")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Hypotheses", len(state.hypotheses))
        c2.metric("Simulations", len(state.simulations))
        c3.metric("Protocols", len(state.protocols))
        c4.metric("Debate Messages", len(state.debate_log))

        render_errors(state.errors)


with tab_pipeline:
    if not st.session_state.pipeline_run:
        render_empty_state("Run the pipeline to see agent progress.")

    state = st.session_state.state
    timings = getattr(state, "pipeline_stage_timings", {})

    render_stepper(timings, state.errors)
    render_stage_detail(timings, state.errors)
    render_activity_log(state)


with tab_hypotheses:
    if not st.session_state.pipeline_run:
        render_empty_state("Run the pipeline to generate hypotheses.")

    state = st.session_state.state
    if not state.hypotheses:
        st.info("No hypotheses generated.")
    else:
        sort_by, filter_by = render_sort_filter()
        ranked = apply_sort_filter(state.hypotheses, sort_by, filter_by)
        for i, h in enumerate(ranked, 1):
            render_hypothesis_card(h, i)

            sims = [s for s in state.simulations if s.hypothesis_id == h.id]
            for sim in sims:
                st.markdown(
                    f"**Simulation Outcome**: Intervention on **{sim.intervention_variable}** "
                    f"to {sim.intervention_value} &rarr; Predicted **{sim.target_variable}** "
                    f"change: **{sim.delta:+.4f}**",
                    unsafe_allow_html=True,
                )

            protocols = [p for p in state.protocols if p.hypothesis_id == h.id]
            for p in protocols:
                with st.expander("Linked Protocol"):
                    if p.step_by_step_procedure:
                        for j, step in enumerate(p.step_by_step_procedure, 1):
                            st.markdown(f"{j}. {step}")
                    st.code("\n".join(p.step_by_step_procedure), language=None)


with tab_causal:
    if not st.session_state.pipeline_run:
        render_empty_state("Run the pipeline to see causal graph and simulations.")

    state = st.session_state.state
    col_graph, col_sim = st.columns([3, 2])

    with col_graph:
        if state.causal_graph and state.causal_graph.nodes:
            render_graph(state.causal_graph)
        else:
            st.info("No causal graph generated. Provide data to enable causal discovery.")

    with col_sim:
        csv_path = st.session_state.get("saved_csv_path", None)
        render_simulator(csv_path)

        if state.simulations and not (csv_path and Path(csv_path).exists()):
            sim_data = []
            for s in state.simulations:
                sim_data.append({
                    "Hypothesis ID": s.hypothesis_id[:8] if s.hypothesis_id else "N/A",
                    "Intervention": s.intervention_variable,
                    "Target": s.target_variable,
                    "Delta": f"{s.delta:+.4f}" if s.delta is not None else "N/A",
                })
            if sim_data:
                st.subheader("Stored Simulations")
                st.dataframe(pd.DataFrame(sim_data), use_container_width=True)


with tab_report:
    if not st.session_state.pipeline_run:
        render_empty_state("Run the pipeline to generate a report.")

    state = st.session_state.state
    render_report(state)
