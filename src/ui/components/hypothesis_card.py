import streamlit as st
from src.state import Hypothesis, SimulationResult, ExperimentProtocol
from src.ui.components.score_pill import render_score_pills


def render_hypothesis_card(
    h: Hypothesis,
    rank: int,
    simulations: list[SimulationResult] | None = None,
    protocols: list[ExperimentProtocol] | None = None,
):
    with st.expander(f"#{rank}  {h.title}"):
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

            # Inline linked simulation results
            if simulations:
                st.markdown("---")
                st.markdown("**Linked Simulation Results**")
                for sim in simulations:
                    delta_class = "hf-sim-delta-pos" if sim.delta and sim.delta > 0 else "hf-sim-delta-neg"
                    delta_str = f"{sim.delta:+.4f}" if sim.delta is not None else "N/A"
                    ci_str = f"[{sim.ci_lower:.4f}, {sim.ci_upper:.4f}]" if sim.ci_lower is not None and sim.ci_upper is not None else "N/A"
                    st.markdown(
                        f'<div class="hf-sim-result">'
                        f'Intervention: <strong>{sim.intervention_variable}</strong> &rarr; {sim.intervention_value}<br>'
                        f'Predicted <strong>{sim.target_variable}</strong> change: '
                        f'<span class="{delta_class}">{delta_str}</span><br>'
                        f'95% CI: <code>{ci_str}</code>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

            # Inline linked experiment protocols
            if protocols:
                st.markdown("---")
                st.markdown("**Linked Experiment Protocols**")
                for p in protocols:
                    steps_html = "".join(f"<li>{step}</li>" for step in p.step_by_step_procedure)
                    meta_parts = []
                    if p.recommended_test:
                        meta_parts.append(f"Test: {p.recommended_test}")
                    if p.required_sample_size:
                        meta_parts.append(f"Sample: {p.required_sample_size}")
                    if p.estimated_duration:
                        meta_parts.append(f"Duration: {p.estimated_duration}")
                    meta_str = " &middot; ".join(meta_parts)
                    st.markdown(
                        f'<div class="hf-protocol">'
                        f'<div class="hf-protocol-header">{p.title}</div>'
                        f'<div class="hf-protocol-meta">{meta_str}</div>'
                        f'<div class="hf-protocol-steps"><ol>{steps_html}</ol></div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )


        with col_b:
            render_score_pills({
                "Novelty": h.novelty_score,
                "Rigor": h.causal_rigor_score,
                "Test": h.testability_score,
                "Impact": h.impact_score,
            })


def render_sort_filter():
    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox(
            "Sort by",
            ["Composite Score", "Novelty", "Causal Rigor", "Testability", "Impact"],
            key="hyp_sort",
        )
    with col2:
        filter_by = st.selectbox(
            "Filter",
            ["All", "High Impact (>0.7)", "Novel (>0.8)", "With Critiques", "With Safety Flags"],
            key="hyp_filter",
        )
    return sort_by, filter_by


def apply_sort_filter(hypotheses: list[Hypothesis], sort_by: str, filter_by: str) -> list[Hypothesis]:
    result = list(hypotheses)

    sort_key_map = {
        "Composite Score": lambda h: (h.novelty_score + h.causal_rigor_score + h.testability_score + h.impact_score) / 4.0,
        "Novelty": lambda h: h.novelty_score,
        "Causal Rigor": lambda h: h.causal_rigor_score,
        "Testability": lambda h: h.testability_score,
        "Impact": lambda h: h.impact_score,
    }
    result.sort(key=sort_key_map.get(sort_by, sort_key_map["Composite Score"]), reverse=True)

    if filter_by == "High Impact (>0.7)":
        result = [h for h in result if h.impact_score > 0.7]
    elif filter_by == "Novel (>0.8)":
        result = [h for h in result if h.novelty_score > 0.8]
    elif filter_by == "With Critiques":
        result = [h for h in result if h.critique_notes]
    elif filter_by == "With Safety Flags":
        result = [h for h in result if h.safety_flags]

    return result
