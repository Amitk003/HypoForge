import streamlit as st
from src.state import HypothesisState


def render_report(state: HypothesisState):
    st.subheader("Executive Summary")

    top = state.top_hypotheses
    top_title = top[0].title if top else "N/A"
    top_score = (
        (top[0].novelty_score + top[0].causal_rigor_score + top[0].testability_score + top[0].impact_score) / 4.0
        if top else 0.0
    )

    st.markdown(
        f'<div class="hf-card">'
        f'<p style="font-weight:600;margin:0 0 8px 0;">Research Goal: {state.research_goal}</p>'
        f'<p style="color:#475569;margin:0 0 4px 0;">'
        f'Generated {len(state.hypotheses)} hypotheses, ran {len(state.simulations)} simulations, '
        f'designed {len(state.protocols)} experiment protocols.</p>'
        f'<p style="color:#475569;margin:0;">Top hypothesis: <strong>{top_title}</strong> &mdash; Score: {top_score:.2f}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if state.meta_review_report:
        st.markdown("---")
        st.markdown("### Full Report")
        st.markdown(state.meta_review_report)

        st.download_button(
            label="Download Markdown",
            data=state.meta_review_report,
            file_name="hypoforge_report.md",
            mime="text/markdown",
            use_container_width=True,
        )
    else:
        st.info("No report generated.")
