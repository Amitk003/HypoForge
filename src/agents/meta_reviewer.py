from src.state import HypothesisState


def synthesize_review(state: HypothesisState) -> HypothesisState:
    lines = []
    lines.append("# Meta-Review: Hypothesis Synthesis Report")
    lines.append("")
    lines.append("## Research Goal")
    lines.append(state.research_goal)
    lines.append("")

    lines.append("## Summary")
    num_h = len(state.hypotheses)
    num_sim = len(state.simulations)
    num_prot = len(state.protocols)
    lines.append(f"Generated {num_h} hypotheses, ran {num_sim} simulations, designed {num_prot} experiment protocols.")
    lines.append("")

    if state.top_hypotheses:
        lines.append("## Top Ranked Hypotheses")
        for i, h in enumerate(state.top_hypotheses[:5], 1):
            lines.append("")
            lines.append(f"### {i}. {h.title}")
            lines.append(f"**Statement**: {h.core_statement}")
            lines.append(f"**Novelty**: {h.novelty_score:.2f} | **Causal Rigor**: {h.causal_rigor_score:.2f} | **Testability**: {h.testability_score:.2f} | **Impact**: {h.impact_score:.2f}")
            if h.critique_notes:
                lines.append("**Critique notes:**")
                for note in h.critique_notes:
                    lines.append(f"- {note}")
            if h.safety_flags:
                lines.append("**Safety flags:**")
                for flag in h.safety_flags:
                    lines.append(f"- {flag}")

    if state.simulations:
        lines.append("")
        lines.append("## Simulation Results")
        for sim in state.simulations:
            lines.append("")
            lines.append(f"- **Intervention**: Change {sim.intervention_variable} to {sim.intervention_value}")
            lines.append(f"- **Effect on {sim.target_variable}**: {sim.delta:+.4f} (baseline: {sim.baseline_outcome:.4f}, predicted: {sim.predicted_outcome:.4f})")
            lines.append(f"- **95% CI**: [{sim.ci_lower:.4f}, {sim.ci_upper:.4f}]")

    if state.protocols:
        lines.append("")
        lines.append("## Experiment Protocols")
        for p in state.protocols:
            lines.append("")
            lines.append(f"### {p.title}")
            lines.append(f"- **Design**: {p.recommended_test}")
            lines.append(f"- **Sample size needed**: {p.required_sample_size}")
            lines.append(f"- **Estimated duration**: {p.estimated_duration}")
            lines.append("**Steps:**")
            for step in p.step_by_step_procedure:
                lines.append(f"1. {step}")

    if state.errors:
        lines.append("")
        lines.append("## Warnings / Errors")
        for e in state.errors:
            lines.append(f"- {e.splitlines()[0]}")

    state.meta_review_report = "\n".join(lines)
    state.pipeline_stage = "review_synthesized"
    return state

