import streamlit as st

STAGE_LABELS = [
    "Literature Scout",
    "Data Analysis",
    "Generator",
    "Critic",
    "Evolver",
    "Simulator",
    "Experiment\nDesigner",
    "Meta-Reviewer",
]

STAGE_KEYS = [
    "literature_scout",
    "data_analysis",
    "hypothesis_generator",
    "critic",
    "evolver",
    "simulator",
    "experiment_designer",
    "meta_reviewer",
]


def render_stepper(timings: dict[str, float], errors: list[str]):
    html_parts = ['<div class="hf-stepper">']
    for i, (key, label) in enumerate(zip(STAGE_KEYS, STAGE_LABELS)):
        if key in timings:
            dot_class = "hf-step-dot--complete"
            dot_content = "&#10003;"
            line_class = "hf-step-line--complete"
        elif any(key in e for e in errors):
            dot_class = "hf-step-dot--error"
            dot_content = "&#10007;"
            line_class = ""
        else:
            dot_class = "hf-step-dot--pending"
            dot_content = str(i + 1)
            line_class = ""

        html_parts.append(
            f'<div style="display:flex;flex-direction:column;align-items:center;flex:1;">'
            f'<div class="hf-step-dot {dot_class}">{dot_content}</div>'
            f'<div class="hf-step-label">{label}</div>'
            f'</div>'
        )
        if i < len(STAGE_KEYS) - 1:
            html_parts.append(f'<div class="hf-step-line {line_class}"></div>')

    html_parts.append("</div>")
    st.markdown("".join(html_parts), unsafe_allow_html=True)


def render_stage_detail(timings: dict[str, float], errors: list[str]):
    with st.expander("Stage Details", expanded=True):
        for key, label in zip(STAGE_KEYS, STAGE_LABELS):
            display_label = label.replace("\n", " ")
            if key in timings:
                st.markdown(
                    f"**{display_label}** &nbsp; "
                    f'<span style="color:#0D9488;">&#10003; Complete</span> '
                    f"({timings[key]}s)",
                    unsafe_allow_html=True,
                )
            elif any(key in e for e in errors):
                related = [e for e in errors if key in e]
                msg = related[0].split("\n")[0] if related else "Unknown error"
                st.markdown(
                    f"**{display_label}** &nbsp; "
                    f'<span style="color:#DC2626;">&#10007; Failed</span>',
                    unsafe_allow_html=True,
                )
                st.error(msg)


def render_activity_log(state):
    with st.expander("Activity Log"):
        if not state.literature_context and not state.dataframe_summary:
            st.caption("No activity recorded.")
        else:
            for key, label in zip(STAGE_KEYS, STAGE_LABELS):
                display_label = label.replace("\n", " ")
                timing = state.pipeline_stage_timings.get(key, None)
                timing_str = f"({timing}s)" if timing is not None else ""
                st.caption(f"  {display_label}: completed {timing_str}")
