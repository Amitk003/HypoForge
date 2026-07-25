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


def _get_stage_status(key: str, timings: dict, error_keys: list[str]) -> str:
    if key in timings:
        return "complete"
    if key in error_keys:
        return "error"
    return "pending"


def render_stepper(timings: dict[str, float], error_keys: list[str]):
    html_parts = ['<div class="hf-stepper">']
    for i, (key, label) in enumerate(zip(STAGE_KEYS, STAGE_LABELS)):
        status = _get_stage_status(key, timings, error_keys)
        if status == "complete":
            dot_class = "hf-step-dot--complete"
            dot_content = "&#10003;"
        elif status == "error":
            dot_class = "hf-step-dot--error"
            dot_content = "&#10007;"
        else:
            dot_class = "hf-step-dot--pending"
            dot_content = str(i + 1)

        line_class = ""
        if i < len(STAGE_KEYS) - 1:
            next_status = _get_stage_status(STAGE_KEYS[i + 1], timings, error_keys)
            if next_status == "complete":
                line_class = "hf-step-line--complete"

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


def render_stage_detail(timings: dict[str, float], errors: list[str], error_keys: list[str]):
    with st.expander("Stage Details", expanded=True):
        for key, label in zip(STAGE_KEYS, STAGE_LABELS):
            display_label = label.replace("\n", " ")
            status = _get_stage_status(key, timings, error_keys)
            if status == "complete":
                st.markdown(
                    f"**{display_label}** &nbsp; "
                    f'<span style="color:#0D9488;">&#10003; Complete</span> '
                    f"({timings[key]}s)",
                    unsafe_allow_html=True,
                )
            elif status == "error":
                related = [e for e in errors if key in e.lower() or key.replace("_", " ") in e.lower()]
                msg = related[0].split("\n")[0] if related else "Unknown error"
                st.markdown(
                    f"**{display_label}** &nbsp; "
                    f'<span style="color:#DC2626;">&#10007; Failed</span>',
                    unsafe_allow_html=True,
                )
                st.error(msg)
            else:
                st.markdown(
                    f"**{display_label}** &nbsp; "
                    f'<span style="color:#94A3B8;">&#9679; Pending</span>',
                    unsafe_allow_html=True,
                )


def _get_stage_summary(state, key: str) -> str:
    summaries = {
        "literature_scout": lambda s: f"Found {len(s.literature_context)} paper(s)" if s.literature_context else "No papers found",
        "data_analysis": lambda s: f"Graph: {len(s.causal_graph.nodes)} nodes, {len(s.causal_graph.edges)} edges" if s.causal_graph and s.causal_graph.nodes else "No graph generated",
        "hypothesis_generator": lambda s: f"Generated {len(s.hypotheses)} hypotheses",
        "critic": lambda s: f"Critiqued {len(s.hypotheses)} hypotheses ({sum(1 for h in s.hypotheses if h.critique_notes)} with notes)",
        "evolver": lambda s: f"Ranked {len(s.hypotheses)} hypotheses (top score: {s.top_hypotheses[0].novelty_score:.2f})" if s.top_hypotheses else "No hypotheses to rank",
        "simulator": lambda s: f"Ran {len(s.simulations)} counterfactual simulations",
        "experiment_designer": lambda s: f"Designed {len(s.protocols)} experiment protocols",
        "meta_reviewer": lambda s: "Report synthesized" if s.meta_review_report else "No report",
    }
    fn = summaries.get(key)
    if fn:
        try:
            return fn(state)
        except Exception:
            return "Completed"
    return "Completed"


def render_activity_log(state):
    with st.expander("Activity Log"):
        for key, label in zip(STAGE_KEYS, STAGE_LABELS):
            display_label = label.replace("\n", " ")
            timing = state.pipeline_stage_timings.get(key)
            timing_str = f" ({timing}s)" if timing is not None else ""
            if key in state.pipeline_stage_timings:
                summary = _get_stage_summary(state, key)
                st.caption(f"**{display_label}**: {summary}{timing_str}")
            else:
                st.caption(f"**{display_label}**: pending")
