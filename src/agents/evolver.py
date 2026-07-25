from src.state import Hypothesis, HypothesisState, DebateMessage
import copy


def evolve_and_rank(state: HypothesisState) -> HypothesisState:
    if not state.hypotheses:
        state.pipeline_stage = "evolution_complete"
        return state

    score_hypotheses(state.hypotheses)
    state.hypotheses.sort(key=lambda h: composite_score(h), reverse=True)

    evolved = genetic_evolution(state.hypotheses)
    if evolved:
        score_hypotheses(evolved)
        state.hypotheses.extend(evolved)
        state.hypotheses.sort(key=lambda h: composite_score(h), reverse=True)

    state.hypotheses = state.hypotheses[:10]

    msg = DebateMessage(
        agent_role="evolver",
        claim=f"Ranked and evolved {len(state.hypotheses)} hypotheses.",
        counter_argument=f"Top hypothesis: {state.hypotheses[0].title} (score: {composite_score(state.hypotheses[0]):.3f})",
        consensus_status="ranked",
    )
    state.debate_log.append(msg)

    state.pipeline_stage = "evolution_complete"
    return state


def composite_score(h: Hypothesis) -> float:
    w1, w2, w3, w4 = 0.25, 0.25, 0.25, 0.25
    return (
        w1 * h.novelty_score
        + w2 * h.causal_rigor_score
        + w3 * h.testability_score
        + w4 * h.impact_score
    )


def score_hypotheses(hypotheses: list[Hypothesis]) -> None:
    for h in hypotheses:
        penalty = len(h.critique_notes) * 0.05
        if h.causal_rigor_score > 0.0:
            h.causal_rigor_score = max(0.0, h.causal_rigor_score - penalty)


def genetic_evolution(hypotheses: list[Hypothesis]) -> list[Hypothesis]:
    if len(hypotheses) < 2:
        return []

    evolved: list[Hypothesis] = []
    top = hypotheses[:4]

    for i in range(0, len(top) - 1, 2):
        p1, p2 = top[i], top[i + 1]
        child = crossover(p1, p2)
        if child:
            child = mutate(child)
            evolved.append(child)

    return evolved


def crossover(p1: Hypothesis, p2: Hypothesis) -> Hypothesis:
    from src.state import Hypothesis
    import uuid

    merged_evidence = list(set(p1.supporting_evidence + p2.supporting_evidence))
    merged_notes = list(set(p1.critique_notes + p2.critique_notes))
    merged_safety = list(set(p1.safety_flags + p2.safety_flags))

    title = f"Evolved: {p1.title.split(':')[0].strip()} & {p2.title.split(':')[0].strip()}"
    statement = (
        f"Combined hypothesis: {p1.core_statement[:200]} "
        f"Integrated with: {p2.core_statement[:200]}"
    )
    mechanism = (
        f"{p1.proposed_mechanism[:200]} "
        f"Further supported by: {p2.proposed_mechanism[:200]}"
    )

    return Hypothesis(
        id=str(uuid.uuid4()),
        title=title,
        core_statement=statement,
        supporting_evidence=merged_evidence,
        proposed_mechanism=mechanism,
        novelty_score=min(1.0, (p1.novelty_score + p2.novelty_score) / 2 + 0.1),
        testability_score=(p1.testability_score + p2.testability_score) / 2,
        causal_rigor_score=max(p1.causal_rigor_score, p2.causal_rigor_score),
        impact_score=(p1.impact_score + p2.impact_score) / 2,
        safety_flags=merged_safety,
        critique_notes=merged_notes,
    )


def mutate(h: Hypothesis) -> Hypothesis:
    import random
    mut = random.random()
    if mut < 0.3:
        h.novelty_score = min(1.0, h.novelty_score + 0.1)
    elif mut < 0.6:
        h.testability_score = min(1.0, h.testability_score + 0.1)
    return h
