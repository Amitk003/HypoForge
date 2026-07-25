import uuid
from src.state import ExperimentProtocol, HypothesisState


def design_experiments(state: HypothesisState) -> HypothesisState:
    if not state.top_hypotheses:
        state.pipeline_stage = "experiments_designed"
        return state
    protocols = []
    for h in state.top_hypotheses[:3]:
        words = h.core_statement.lower().split()
        dvs = [w for w in words if len(w) > 4]
        ivs = dvs[:2] if dvs else ["intervention_variable"]
        dvs = dvs[2:4] if len(dvs) > 2 else ["outcome_measure"]
        confounders = []
        if state.causal_graph:
            confounders = state.causal_graph.confounders[:3]

        n = estimate_sample_size(effect_size=0.5, power=0.8)
        protocol = ExperimentProtocol(
            hypothesis_id=h.id,
            title=f"Experimental protocol for: {h.title}",
            independent_variables=ivs,
            dependent_variables=dvs,
            confounders_to_control=confounders,
            recommended_test="ANOVA" if len(ivs) > 1 else "t-test",
            required_sample_size=n,
            step_by_step_procedure=build_procedure(ivs, dvs),
            success_metrics=[f"Significant change in {dvs[0]} (p < 0.05)"],
            estimated_duration=f"{max(4, n // 10)} weeks",
        )
        protocols.append(protocol)
    state.protocols = protocols
    state.pipeline_stage = "experiments_designed"
    return state


def estimate_sample_size(effect_size: float = 0.5, power: float = 0.8, alpha: float = 0.05) -> int:
    n = int(16 / (effect_size ** 2))
    return max(n, 10)


def build_procedure(ivs: list[str], dvs: list[str]) -> list[str]:
    steps = []
    steps.append(f"Identify study population and sampling frame.")
    steps.append(f"Measure baseline for {', '.join(dvs)} across all subjects.")
    steps.append(f"Randomly assign subjects to control and treatment groups.")
    steps.append(f"Apply intervention: vary {', '.join(ivs)} according to protocol.")
    steps.append(f"Measure {', '.join(dvs)} after intervention period.")
    steps.append(f"Run {dvs[0] if dvs else 'outcome'} and compare groups using appropriate statistical test.")
    return steps
