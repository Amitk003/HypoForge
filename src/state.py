from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Hypothesis(BaseModel):
    id: str = Field(description="Unique identifier for the hypothesis")
    title: str = Field(description="Short descriptive title")
    core_statement: str = Field(description="The main hypothesis claim")
    supporting_evidence: list[str] = Field(default_factory=list, description="Evidence snippets from literature or data")
    proposed_mechanism: str = Field(default="", description="How the causal mechanism is proposed to work")
    novelty_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Novelty score 0-1")
    testability_score: float = Field(default=0.0, ge=0.0, le=1.0, description="How testable the hypothesis is")
    causal_rigor_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Strength of causal reasoning")
    impact_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Potential impact if confirmed")
    safety_flags: list[str] = Field(default_factory=list)
    critique_notes: list[str] = Field(default_factory=list)


class CausalEdge(BaseModel):
    source: str
    target: str
    edge_type: str = "directed"
    weight: float = 1.0


class CausalGraphData(BaseModel):
    nodes: list[str] = Field(default_factory=list)
    edges: list[CausalEdge] = Field(default_factory=list)
    confounders: list[str] = Field(default_factory=list)
    mediators: list[str] = Field(default_factory=list)
    dot_source: str = Field(default="", description="Graphviz DOT format string")


class SimulationResult(BaseModel):
    hypothesis_id: str = ""
    target_variable: str = ""
    intervention_variable: str = ""
    intervention_value: Optional[float] = None
    predicted_outcome: Optional[float] = None
    baseline_outcome: Optional[float] = None
    delta: Optional[float] = None
    ci_lower: Optional[float] = None
    ci_upper: Optional[float] = None
    plot_path: str = ""


class ExperimentProtocol(BaseModel):
    hypothesis_id: str = ""
    title: str = ""
    independent_variables: list[str] = Field(default_factory=list)
    dependent_variables: list[str] = Field(default_factory=list)
    confounders_to_control: list[str] = Field(default_factory=list)
    recommended_test: str = ""
    required_sample_size: int = 0
    step_by_step_procedure: list[str] = Field(default_factory=list)
    success_metrics: list[str] = Field(default_factory=list)
    estimated_duration: str = ""


class DebateMessage(BaseModel):
    agent_role: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    claim: str = ""
    counter_argument: str = ""
    consensus_status: str = "pending"


class HypothesisState(BaseModel):
    research_goal: str = ""
    data_path: Optional[str] = None
    dataframe_summary: str = ""
    literature_context: list[str] = Field(default_factory=list)
    causal_graph: Optional[CausalGraphData] = None
    hypotheses: list[Hypothesis] = Field(default_factory=list)
    simulations: list[SimulationResult] = Field(default_factory=list)
    protocols: list[ExperimentProtocol] = Field(default_factory=list)
    debate_log: list[DebateMessage] = Field(default_factory=list)
    pipeline_stage: str = "initialized"
    errors: list[str] = Field(default_factory=list)

    @property
    def top_hypotheses(self) -> list[Hypothesis]:
        """Dynamically sorted top hypotheses by overall average score."""
        def score(h: Hypothesis) -> float:
            return (h.novelty_score + h.testability_score + h.causal_rigor_score + h.impact_score) / 4.0
        return sorted(self.hypotheses, key=score, reverse=True)[:5]

