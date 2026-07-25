import streamlit as st


def render_header(research_goal: str = ""):
    goal_text = research_goal if research_goal else "Enter a research goal and optional dataset to generate testable scientific hypotheses."
    html = (
        '<div class="hf-header">'
        '<div>'
        '<span class="hf-header-title">HypoForge</span>'
        '<span class="hf-header-subtitle">  AI Co-Scientist</span>'
        '</div>'
        '<div class="hf-header-goal">' + goal_text + '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)
