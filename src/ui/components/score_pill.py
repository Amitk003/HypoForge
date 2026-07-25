import streamlit as st


def render_score_pill(label: str, score: float) -> str:
    score_class = "score-pill--high" if score > 0.7 else ("score-pill--low" if score < 0.4 else "")
    return f'<span class="score-pill {score_class}">{label} <span class="score-value">{score:.2f}</span></span>'


def render_score_pills(scores: dict[str, float]):
    pills = "".join(render_score_pill(k, v) for k, v in scores.items())
    st.markdown(f'<div style="margin: 8px 0;">{pills}</div>', unsafe_allow_html=True)
