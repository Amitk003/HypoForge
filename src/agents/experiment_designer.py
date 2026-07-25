import uuid
from src.state import ExperimentProtocol, HypothesisState


def design_experiments(state: HypothesisState) -> HypothesisState:
    if not state.top_hypotheses:
        state.pipeline_stage = "experiments_designed"
        return state

    protocols = []
    
    # Extract candidate variable names from DAG nodes or simulations
    known_nodes = state.causal_graph.nodes if state.causal_graph else []
    
    for h in state.top_hypotheses[:3]:
        statement_lower = h.core_statement.lower()
        
        # Match real domain variables from causal graph if available
        matched_vars = [
            node for node in known_nodes 
            if node.lower() in statement_lower or node.lower().replace("_", " ") in statement_lower
        ]
        
        if len(matched_vars) >= 2:
            ivs = [matched_vars[0]]
            dvs = [matched_vars[1]]
        elif len(matched_vars) == 1:
            ivs = [matched_vars[0]]
            dvs = ["target_outcome"]
        else:
            ivs = ["primary_intervention"]
            dvs = ["measured_outcome"]

        confounders = [c for c in known_nodes if c not in ivs and c not in dvs][:3]

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
            success_metrics=[f"Statistically significant change in {dvs[0]} (p < 0.05)"],
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
    steps.append("Identify target study population and baseline sampling criteria.")
    steps.append(f"Measure baseline values for {', '.join(dvs)} across all experimental units.")
    steps.append("Randomly assign subjects into control and treatment groups.")
    steps.append(f"Apply intervention: systematically vary {', '.join(ivs)} according to protocol parameters.")
    steps.append(f"Measure post-intervention outcomes for {', '.join(dvs)}.")
    steps.append(f"Perform hypothesis testing on {dvs[0]} outcomes using appropriate statistical methods.")
    return steps

