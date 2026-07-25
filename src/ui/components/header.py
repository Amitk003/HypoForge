import streamlit as st


def render_header(research_goal: str = ""):
    st.markdown("""
        <style>
        .hf-header {
            display: flex; flex-direction: column;
            margin-bottom: 8px;
        }
        .hf-header-title {
            font-family: 'Inter', sans-serif;
            font-weight: 600; font-size: 20px;
            color: #0F172A; margin: 0;
        }
        .hf-header-subtitle {
            font-family: 'Inter', sans-serif;
            font-weight: 400; font-size: 12px;
            color: #94A3B8; margin: 0;
        }
        .hf-header-goal {
            font-family: 'Inter', sans-serif;
            font-size: 13px; color: #475569;
            margin-top: 4px;
            white-space: nowrap; overflow: hidden;
            text-overflow: ellipsis;
        }
        </style>
        <div class="hf-header">
            <div>
                <span class="hf-header-title">HypoForge</span>
                <span class="hf-header-subtitle">  AI Co-Scientist</span>
            </div>
            <div class="hf-header-goal">{goal}</div>
        </div>
    """.format(goal=research_goal if research_goal else "Enter a research goal and optional dataset to generate, debate, simulate, and design testable scientific hypotheses."),
        unsafe_allow_html=True,
    )
