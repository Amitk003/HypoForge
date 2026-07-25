import streamlit as st
from src.state import Hypothesis
from src.ui.components.score_pill import render_score_pills


def render_hypothesis_card(h: Hypothesis, rank: int):
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
