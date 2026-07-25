from typing import Optional
from src.state import Hypothesis, HypothesisState, DebateMessage


def critique_hypotheses(state: HypothesisState) -> HypothesisState:
    if not state.hypotheses:
        state.pipeline_stage = "critique_complete"
        return state

    dag = state.causal_graph
    for h in state.hypotheses:
        review_plausibility(h)
        review_causal_fallacy(h, dag)
        review_feasibility(h)

        msg = DebateMessage(
            agent_role="critic",
            claim=f"Reviewed: {h.title}",
            counter_argument="; ".join(h.critique_notes) if h.critique_notes else "No major issues found.",
            consensus_status="reviewed",
        )
        state.debate_log.append(msg)

    state.pipeline_stage = "critique_complete"
    return state


def review_plausibility(h: Hypothesis) -> None:
    issues = []
    if not h.supporting_evidence or all(not e.strip() for e in h.supporting_evidence):
        issues.append("No supporting evidence provided.")
    if len(h.core_statement) < 20:
        issues.append("Hypothesis statement is too short to be meaningful.")
    if not h.proposed_mechanism:
        issues.append("No causal mechanism proposed.")
    for issue in issues:
        h.critique_notes.append(f"Plausibility: {issue}")
    if not issues and not h.safety_flags:
        h.causal_rigor_score = min(1.0, h.causal_rigor_score + 0.1)


def review_causal_fallacy(h: Hypothesis, dag: Optional[object]) -> None:
    if not dag or not dag.edges:
        return
    dag_nodes = set(dag.nodes)
    words_in_statement = set(h.core_statement.lower().split())
    mentioned_vars = [v for v in dag_nodes if v.lower() in words_in_statement]
    if len(mentioned_vars) >= 2:
        edge_present = False
        for i in range(len(mentioned_vars)):
            for j in range(i + 1, len(mentioned_vars)):
                for e in dag.edges:
                    if (e.source == mentioned_vars[i] and e.target == mentioned_vars[j]) or \
                       (e.source == mentioned_vars[j] and e.target == mentioned_vars[i]):
                        edge_present = True
                        break
        if not edge_present:
            h.critique_notes.append(
                "Causal fallacy: Hypothesis assumes causal link between variables "
                "that show no direct edge in the discovered causal graph."
            )
            h.causal_rigor_score = max(0.0, h.causal_rigor_score - 0.2)


def review_feasibility(h: Hypothesis) -> None:
    if h.testability_score < 0.3:
        h.critique_notes.append("Feasibility: Hypothesis may be difficult to test with available data.")
    if not h.safety_flags:
        if "human" in h.core_statement.lower() or "patient" in h.core_statement.lower():
            h.safety_flags.append("Involves human subjects - ethical approval may be required.")
