import uuid
from typing import Optional
from src.state import Hypothesis, HypothesisState, CausalGraphData


def generate_hypotheses(state: HypothesisState) -> HypothesisState:
    candidates: list[Hypothesis] = []
    data_summary = state.dataframe_summary if state.dataframe_summary else ""
    lit_context = state.literature_context[0] if state.literature_context else ""
    dag = state.causal_graph

    base_goal = state.research_goal.strip().rstrip("?.")

    anomalies = extract_anomalies(data_summary)
    causal_paths = extract_causal_paths(dag)
    lit_gaps = extract_literature_gaps(lit_context, base_goal)

    for i, anomaly in enumerate(anomalies[:3]):
        h = Hypothesis(
            id=str(uuid.uuid4()),
            title=f"{base_goal}: Anomaly-driven hypothesis {i + 1}",
            core_statement=anomaly["statement"],
            supporting_evidence=[anomaly["evidence"]],
            proposed_mechanism=anomaly["mechanism"],
            novelty_score=round(0.5 + 0.3 * (i / max(len(anomalies), 1)), 2),
            testability_score=0.8,
            causal_rigor_score=0.5,
            impact_score=0.6,
        )
        candidates.append(h)

    for i, path in enumerate(causal_paths[:3]):
        h = Hypothesis(
            id=str(uuid.uuid4()),
            title=f"{base_goal}: Causal pathway hypothesis {i + 1}",
            core_statement=path["statement"],
            supporting_evidence=[f"Causal path: {path['path_str']}"],
            proposed_mechanism=path["mechanism"],
            novelty_score=round(0.4 + 0.2 * (i / max(len(causal_paths), 1)), 2),
            testability_score=0.7,
            causal_rigor_score=0.8,
            impact_score=0.7,
        )
        candidates.append(h)

    for i, gap in enumerate(lit_gaps[:2]):
        h = Hypothesis(
            id=str(uuid.uuid4()),
            title=f"{base_goal}: Literature gap hypothesis {i + 1}",
            core_statement=gap["statement"],
            supporting_evidence=[gap["evidence"]],
            proposed_mechanism=gap["mechanism"],
            novelty_score=0.8,
            testability_score=0.6,
            causal_rigor_score=0.4,
            impact_score=0.7,
        )
        candidates.append(h)

    if not candidates:
        h = Hypothesis(
            id=str(uuid.uuid4()),
            title=f"General hypothesis on {base_goal}",
            core_statement=f"We hypothesize that {base_goal.lower()} is influenced by multiple interacting factors that can be measured and tested.",
            supporting_evidence=["Generated from user research goal"],
            proposed_mechanism="Multi-factor interaction model",
            novelty_score=0.5,
            testability_score=0.7,
            causal_rigor_score=0.4,
            impact_score=0.5,
        )
        candidates.append(h)

    state.hypotheses = candidates[:state.max_hypotheses]
    state.pipeline_stage = "hypotheses_generated"
    return state


def extract_anomalies(summary: str) -> list[dict]:
    results = []
    if not summary:
        return results
    lines = summary.split("\n")
    in_corr_section = False
    for line in lines:
        line_clean = line.strip()
        if "high correlation" in line_clean.lower():
            in_corr_section = True
            continue
        if in_corr_section and "<->" in line_clean:
            parts = line_clean.split(":")
            if len(parts) >= 2:
                pair = parts[0].strip()
                val = parts[1].strip()
                vars_split = pair.split("<->")
                v1 = vars_split[0].strip() if len(vars_split) > 0 else "X"
                v2 = vars_split[1].strip() if len(vars_split) > 1 else "Y"
                results.append({
                    "statement": f"Observed strong statistical coupling between {v1} and {v2} suggests an underlying interaction.",
                    "evidence": f"Correlation detected: {v1} <-> {v2} (r = {val})",
                    "mechanism": f"{v1} and {v2} may share a direct feedback mechanism or common unobserved driver.",
                })
        elif in_corr_section and not line_clean:
            in_corr_section = False
    return results



def extract_causal_paths(dag: Optional[CausalGraphData]) -> list[dict]:
    results = []
    if dag is None or not dag.edges:
        return results
    for edge in dag.edges[:5]:
        results.append({
            "statement": f"Changes in {edge.source} are predicted to cause changes in {edge.target}.",
            "path_str": f"{edge.source} -> {edge.target}",
            "mechanism": f"{edge.source} directly influences {edge.target} through the identified causal pathway.",
        })
    return results


def extract_literature_gaps(lit_context: str, goal: str) -> list[dict]:
    results = []
    if not lit_context or lit_context == "No literature found.":
        results.append({
            "statement": f"There is limited existing research on {goal}, making it a strong candidate for novel investigation.",
            "evidence": "No relevant papers found in initial literature search.",
            "mechanism": "Novel domain with unexplored causal mechanisms waiting to be discovered.",
        })
        return results

    paper_count = lit_context.count("\n2. ") + 1 if lit_context else 0
    if paper_count < 3:
        results.append({
            "statement": f"Few studies exist on this specific question. Existing work may not have tested causal mechanisms directly.",
            "evidence": f"Only {paper_count} relevant papers found, suggesting an under-studied area.",
            "mechanism": "Under-explored domain where new causal pathways may exist.",
        })
    return results
