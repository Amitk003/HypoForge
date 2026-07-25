import streamlit as st
import pandas as pd
import os
import tempfile

from src.orchestrator import run_pipeline
from src.state import HypothesisState, CausalGraphData
from src.data_engine import load_dataframe, summarize_dataframe
from src.causal.causal_discovery import build_graph_from_data


st.set_page_config(page_title="HypoForge", layout="wide")

if "state" not in st.session_state:
    st.session_state.state = HypothesisState()
if "pipeline_run" not in st.session_state:
    st.session_state.pipeline_run = False
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None


st.title("HypoForge")
st.caption("Multi-agent AI co-scientist. Enter a research goal and optional data to generate ranked, testable hypotheses.")


tab_setup, tab_debate, tab_hypotheses, tab_sim, tab_report = st.tabs([
    "Research Setup", "Agent Debate", "Ranked Hypotheses", "Causal Graph & Simulator", "Report & Export"
])


with tab_setup:
    col1, col2 = st.columns([2, 1])

    with col1:
        research_goal = st.text_area(
            "Research Goal",
            placeholder="e.g. How does urban green space affect local air temperature and air quality?",
            height=100,
        )

        uploaded_file = st.file_uploader("Upload data (CSV or Parquet)", type=["csv", "parquet"])

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
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
            tmp.write(st.session_state.uploaded_data.getvalue())
            tmp.close()
            data_path = tmp.name

        state = HypothesisState(
            research_goal=research_goal,
            data_path=data_path,
        )

        with st.spinner("Running pipeline..."):
            result = run_pipeline(state)

        st.session_state.state = result
        st.session_state.pipeline_run = True

        if data_path and os.path.exists(data_path):
            os.unlink(data_path)

        st.success("Pipeline complete!")

    if st.session_state.pipeline_run:
        state = st.session_state.state
        st.subheader("Pipeline Summary")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Hypotheses Generated", len(state.hypotheses))
        c2.metric("Simulations Run", len(state.simulations))
        c3.metric("Protocols Designed", len(state.protocols))
        c4.metric("Debate Messages", len(state.debate_log))

        if state.errors:
            with st.expander("Warnings / Errors"):
                for err in state.errors:
                    st.warning(err.split("\n")[0])


with tab_debate:
    if not st.session_state.pipeline_run:
        st.info("Run the pipeline first to see agent debate logs.")
    else:
        state = st.session_state.state
        if not state.debate_log:
            st.info("No debate messages recorded.")
        else:
            for msg in state.debate_log:
                with st.chat_message(msg.agent_role):
                    st.markdown(f"**{msg.agent_role}**")
                    st.markdown(f"*Claim:* {msg.claim}")
                    if msg.counter_argument:
                        st.markdown(f"*Response:* {msg.counter_argument}")
                    st.caption(f"Status: {msg.consensus_status}")


with tab_hypotheses:
    if not st.session_state.pipeline_run:
        st.info("Run the pipeline first to see ranked hypotheses.")
    else:
        state = st.session_state.state
        top = state.top_hypotheses
        if not top:
            st.info("No hypotheses generated.")
        else:
            for i, h in enumerate(top, 1):
                with st.expander(f"#{i}  {h.title}"):
                    col_a, col_b = st.columns([3, 1])

                    with col_a:
                        st.markdown(f"**Statement**")
                        st.markdown(h.core_statement)

                        if h.proposed_mechanism:
                            st.markdown(f"**Proposed Mechanism**")
                            st.markdown(h.proposed_mechanism)

                        if h.supporting_evidence:
                            st.markdown(f"**Supporting Evidence**")
                            for ev in h.supporting_evidence:
                                st.markdown(f"- {ev}")

                        if h.critique_notes:
                            st.markdown(f"**Critique Notes**")
                            for note in h.critique_notes:
                                st.warning(note)

                        if h.safety_flags:
                            st.markdown(f"**Safety Flags**")
                            for flag in h.safety_flags:
                                st.error(flag)

                    with col_b:
                        st.metric("Novelty", f"{h.novelty_score:.2f}")
                        st.metric("Causal Rigor", f"{h.causal_rigor_score:.2f}")
                        st.metric("Testability", f"{h.testability_score:.2f}")
                        st.metric("Impact", f"{h.impact_score:.2f}")

                    # Link simulation if exists
                    sims = [s for s in state.simulations if s.hypothesis_id == h.id]
                    for sim in sims:
                        st.markdown(f"**Simulation**: Change {sim.intervention_variable} to {sim.intervention_value} -> {sim.target_variable} delta: {sim.delta:+.4f}")


with tab_sim:
    if not st.session_state.pipeline_run:
        st.info("Run the pipeline first to see causal graph and simulations.")
    else:
        state = st.session_state.state

        if state.causal_graph and state.causal_graph.dot_source:
            st.subheader("Causal Graph (DAG)")
            try:
                import graphviz
                graph = graphviz.Source(state.causal_graph.dot_source)
                st.graphviz_chart(graph)
            except ImportError:
                st.text(state.causal_graph.dot_source)
        else:
            st.info("No causal graph generated. Provide data to enable causal discovery.")

        if state.simulations:
            st.subheader("Counterfactual Simulations")
            sim_data = []
            for s in state.simulations:
                sim_data.append({
                    "Hypothesis": s.hypothesis_id[:8],
                    "Intervention": s.intervention_variable,
                    "Target": s.target_variable,
                    "Delta": f"{s.delta:+.4f}" if s.delta is not None else "N/A",
                    "95% CI Lower": f"{s.ci_lower:.4f}" if s.ci_lower is not None else "N/A",
                    "95% CI Upper": f"{s.ci_upper:.4f}" if s.ci_upper is not None else "N/A",
                })
            if sim_data:
                st.dataframe(pd.DataFrame(sim_data), use_container_width=True)
        else:
            st.info("No simulations available. Provide data with numeric columns.")


with tab_report:
    if not st.session_state.pipeline_run:
        st.info("Run the pipeline first to generate a report.")
    else:
        state = st.session_state.state
        if state.meta_review_report:
            st.markdown(state.meta_review_report)
            st.download_button(
                label="Download Report (Markdown)",
                data=state.meta_review_report,
                file_name="hypoforge_report.md",
                mime="text/markdown",
                use_container_width=True,
            )
        else:
            st.info("No report generated.")
