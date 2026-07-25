const API_BASE = import.meta.env.VITE_API_URL || '/api';

export interface PipelineResponse {
  run_id: string;
  pipeline_stage: string;
  hypothesis_count: number;
  simulation_count: number;
  protocol_count: number;
  error_count: number;
  errors: string[];
  timings: Record<string, number>;
}

export interface Hypothesis {
  id: string;
  title: string;
  core_statement: string;
  proposed_mechanism: string;
  supporting_evidence: string[];
  novelty_score: number;
  causal_rigor_score: number;
  testability_score: number;
  impact_score: number;
  critique_notes: string[];
  safety_flags: string[];
}

export interface CausalGraph {
  nodes: string[];
  edges: { source: string; target: string; weight: number }[];
  confounders: string[];
  mediators: string[];
}

export interface SimulationResult {
  target_variable: string;
  intervention_variable: string;
  intervention_value: number;
  baseline_outcome: number;
  predicted_outcome: number;
  delta: number;
  ci_lower: number;
  ci_upper: number;
}

export interface ReportResponse {
  research_goal: string;
  meta_review_report: string;
  hypothesis_count: number;
  simulation_count: number;
  protocol_count: number;
  top_hypothesis_title: string | null;
  top_hypothesis_score: number | null;
}

export async function runPipeline(
  researchGoal: string,
  file?: File,
  alpha = 0.05,
  maxHypotheses = 10
): Promise<PipelineResponse> {
  const formData = new FormData();
  formData.append('research_goal', researchGoal);
  formData.append('alpha', String(alpha));
  formData.append('max_hypotheses', String(maxHypotheses));
  if (file) {
    formData.append('file', file);
  }
  const resp = await fetch(`${API_BASE}/pipeline`, {
    method: 'POST',
    body: formData,
  });
  if (!resp.ok) {
    const err = await resp.text();
    throw new Error(`Pipeline failed: ${err}`);
  }
  return resp.json();
}

export async function getHypotheses(runId: string): Promise<Hypothesis[]> {
  const resp = await fetch(`${API_BASE}/runs/${runId}/hypotheses`);
  if (!resp.ok) throw new Error('Failed to fetch hypotheses');
  return resp.json();
}

export async function getCausalGraph(runId: string): Promise<CausalGraph> {
  const resp = await fetch(`${API_BASE}/runs/${runId}/causal-graph`);
  if (!resp.ok) throw new Error('Failed to fetch causal graph');
  return resp.json();
}

export async function runSimulation(
  runId: string,
  targetVariable: string,
  interventionVariable: string,
  interventionValue: number
): Promise<SimulationResult> {
  const formData = new FormData();
  formData.append('target_variable', targetVariable);
  formData.append('intervention_variable', interventionVariable);
  formData.append('intervention_value', String(interventionValue));
  const resp = await fetch(`${API_BASE}/runs/${runId}/simulate`, {
    method: 'POST',
    body: formData,
  });
  if (!resp.ok) throw new Error('Simulation failed');
  return resp.json();
}

export async function getReport(runId: string): Promise<ReportResponse> {
  const resp = await fetch(`${API_BASE}/runs/${runId}/report`);
  if (!resp.ok) throw new Error('Failed to fetch report');
  return resp.json();
}

export async function getRunStatus(runId: string): Promise<PipelineResponse> {
  const resp = await fetch(`${API_BASE}/runs/${runId}`);
  if (!resp.ok) throw new Error('Failed to fetch run status');
  return resp.json();
}
