import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import pandas as pd
import numpy as np
import os
import tempfile

from src.orchestrator import run_pipeline
from src.state import HypothesisState, CausalGraphData
from src.data_engine import load_dataframe, summarize_dataframe
from src.causal.causal_discovery import build_graph_from_data
from src.simulation.surrogate_sim import train_surrogate, counterfactual_predict


st.set_page_config(page_title="HypoForge", layout="wide")

# Ensure persistent uploads directory exists
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


st.title("HypoForge")
st.caption("Multi-agent AI co-scientist. Enter a research goal and optional dataset to generate, debate, simulate, and design testable scientific hypotheses.")


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
            saved_file_path = UPLOAD_DIR / st.session_state.uploaded_data.name
            with open(saved_file_path, "wb") as f:
                f.write(st.session_state.uploaded_data.getvalue())
            data_path = str(saved_file_path)
            st.session_state.saved_csv_path = data_path

        state = HypothesisState(
            research_goal=research_goal,
            data_path=data_path,
        )

        with st.spinner("Running multi-agent co-scientist pipeline..."):
            result = run_pipeline(state)

        st.session_state.state = result
        st.session_state.pipeline_run = True
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
                    st.markdown(f"**Agent: {msg.agent_role.title()}**")
                    st.markdown(f"*Claim:* {msg.claim}")
                    if msg.counter_argument:
                        st.markdown(f"*Response / Critique:* {msg.counter_argument}")
                    st.caption(f"Status: {msg.consensus_status} | Timestamp: {msg.timestamp}")


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
                        st.markdown(f"**Simulation Outcome**: Intervention on **{sim.intervention_variable}** $\\rightarrow$ Predicted **{sim.target_variable}** change: **{sim.delta:+.4f}**")


def render_pyvis_graph(cg: CausalGraphData) -> str:
    try:
        from pyvis.network import Network
        net = Network(height="400px", width="100%", bgcolor="#0E1117", font_color="#E2E8F0")
        net.toggle_physics(True)
        for node in cg.nodes:
            net.add_node(node, label=node, color="#1E293B", border="#38BDF8")
        for edge in cg.edges:
            label = str(edge.weight) if edge.weight else ""
            color = "#38BDF8"
            net.add_edge(edge.source, edge.target, title=label, color=color, arrows="to")
        return net.generate_html()
    except Exception:
        return ""


with tab_sim:
    if not st.session_state.pipeline_run:
        st.info("Run the pipeline first to see causal graph and simulations.")
    else:
        state = st.session_state.state

        if state.causal_graph and state.causal_graph.nodes:
            st.subheader("Interactive Causal Graph (DAG)")
            pyvis_html = render_pyvis_graph(state.causal_graph)
            if pyvis_html:
                st.components.v1.html(pyvis_html, height=420)
            elif state.causal_graph.dot_source:
                try:
                    st.graphviz_chart(state.causal_graph.dot_source)
                except Exception:
                    st.code(state.causal_graph.dot_source, language="dot")

            if state.causal_graph.confounders:
                with st.expander("Identified Confounders"):
                    st.write(", ".join(state.causal_graph.confounders))
            if state.causal_graph.mediators:
                with st.expander("Identified Mediators"):
                    st.write(", ".join(state.causal_graph.mediators))
        else:
            st.info("No causal graph generated. Provide data to enable causal discovery.")


        st.subheader("Counterfactual Simulator")
        csv_path = st.session_state.get("saved_csv_path", None)
        if csv_path and Path(csv_path).exists():
            df = load_dataframe(csv_path)
            if df is not None:
                num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                target_col = st.selectbox("Target variable", num_cols if num_cols else ["None"], key="sim_target")
                intervention_col = st.selectbox("Intervention variable", [c for c in num_cols if c != target_col] if num_cols else ["None"], key="sim_intervention")
                if target_col != "None" and intervention_col != "None":
                    col1, col2 = st.columns([3, 1])
                    baseline = float(df[intervention_col].mean())
                    with col1:
                        perturbed = st.slider(
                            f"Set value for {intervention_col}",
                            min_value=float(df[intervention_col].min()),
                            max_value=float(df[intervention_col].max()),
                            value=baseline,
                            step=round(float(df[intervention_col].std()) / 10, 2),
                        )
                    with col2:
                        st.metric("Baseline", f"{baseline:.2f}")
                    model = train_surrogate(df, target_col)
                    if model:
                        result = counterfactual_predict(model, df, intervention_col, perturbed)
                        if result:
                            c1, c2, c3 = st.columns(3)
                            c1.metric("Predicted Outcome", f"{result.predicted_outcome:.4f}" if result.predicted_outcome else "N/A")
                            c2.metric("Delta from Baseline", f"{result.delta:+.4f}" if result.delta else "N/A")
                            if result.ci_lower is not None and result.ci_upper is not None:
                                c3.metric("95% CI", f"[{result.ci_lower:.4f}, {result.ci_upper:.4f}]")
        elif state.simulations:
            sim_data = []
            for s in state.simulations:
                sim_data.append({
                    "Hypothesis ID": s.hypothesis_id[:8] if s.hypothesis_id else "N/A",
                    "Intervention Variable": s.intervention_variable,
                    "Target Outcome": s.target_variable,
                    "Intervention Value": f"{s.intervention_value:.2f}" if s.intervention_value is not None else "N/A",
                    "Baseline Outcome": f"{s.baseline_outcome:.4f}" if s.baseline_outcome is not None else "N/A",
                    "Predicted Outcome": f"{s.predicted_outcome:.4f}" if s.predicted_outcome is not None else "N/A",
                    "Delta": f"{s.delta:+.4f}" if s.delta is not None else "N/A",
                    "95% CI Lower": f"{s.ci_lower:.4f}" if s.ci_lower is not None else "N/A",
                    "95% CI Upper": f"{s.ci_upper:.4f}" if s.ci_upper is not None else "N/A",
                })
            if sim_data:
                st.dataframe(pd.DataFrame(sim_data), use_container_width=True)
        else:
            st.info("Upload a dataset with numeric variables to run counterfactual simulations.")


with tab_report:
    if not st.session_state.pipeline_run:
        st.info("Run the pipeline first to generate a report.")
    else:
        state = st.session_state.state
        if state.meta_review_report:
            st.markdown(state.meta_review_report)
            st.download_button(
                label="Download Research Proposal Report (Markdown)",
                data=state.meta_review_report,
                file_name="hypoforge_research_proposal.md",
                mime="text/markdown",
                use_container_width=True,
            )
        else:
            st.info("No report generated.")

