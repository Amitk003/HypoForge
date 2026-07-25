import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from src.state import HypothesisState
from src.orchestrator import run_pipeline
from src.data_engine import load_dataframe
from src.simulation.surrogate_sim import train_surrogate, counterfactual_predict

router = APIRouter()

UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

_runs: dict[str, HypothesisState] = {}


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/pipeline")
def start_pipeline(
    research_goal: str = Form(...),
    file: UploadFile = None,
    alpha: float = Form(0.05),
    max_hypotheses: int = Form(10),
):
    data_path = None
    if file and file.filename:
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        data_path = str(file_path)

    state = HypothesisState(
        research_goal=research_goal,
        data_path=data_path,
        alpha=alpha,
        max_hypotheses=max_hypotheses,
    )

    result = run_pipeline(state)
    run_id = str(uuid.uuid4())
    _runs[run_id] = result

    return {
        "run_id": run_id,
        "pipeline_stage": result.pipeline_stage,
        "hypothesis_count": len(result.hypotheses),
        "simulation_count": len(result.simulations),
        "protocol_count": len(result.protocols),
        "error_count": len(result.errors),
        "errors": [e.split("\n")[0] for e in result.errors],
        "timings": result.pipeline_stage_timings,
    }


@router.get("/runs/{run_id}")
def get_run(run_id: str):
    state = _runs.get(run_id)
    if not state:
        raise HTTPException(status_code=404, detail="Run not found")
    return {
        "run_id": run_id,
        "pipeline_stage": state.pipeline_stage,
        "research_goal": state.research_goal,
        "data_path": state.data_path,
        "hypothesis_count": len(state.hypotheses),
        "simulation_count": len(state.simulations),
        "protocol_count": len(state.protocols),
        "error_count": len(state.errors),
        "errors": [e.split("\n")[0] for e in state.errors],
        "timings": state.pipeline_stage_timings,
    }


@router.get("/runs/{run_id}/hypotheses")
def get_hypotheses(run_id: str):
    state = _runs.get(run_id)
    if not state:
        raise HTTPException(status_code=404, detail="Run not found")
    ranked = state.top_hypotheses
    return [
        {
            "id": h.id,
            "title": h.title,
            "core_statement": h.core_statement,
            "proposed_mechanism": h.proposed_mechanism,
            "supporting_evidence": h.supporting_evidence,
            "novelty_score": h.novelty_score,
            "causal_rigor_score": h.causal_rigor_score,
            "testability_score": h.testability_score,
            "impact_score": h.impact_score,
            "critique_notes": h.critique_notes,
            "safety_flags": h.safety_flags,
        }
        for h in ranked
    ]


@router.get("/runs/{run_id}/causal-graph")
def get_causal_graph(run_id: str):
    state = _runs.get(run_id)
    if not state:
        raise HTTPException(status_code=404, detail="Run not found")
    cg = state.causal_graph
    if not cg:
        return {"nodes": [], "edges": [], "confounders": [], "mediators": []}
    return {
        "nodes": cg.nodes,
        "edges": [
            {"source": e.source, "target": e.target, "weight": e.weight}
            for e in cg.edges
        ],
        "confounders": cg.confounders,
        "mediators": cg.mediators,
    }


@router.post("/runs/{run_id}/simulate")
def run_simulation(
    run_id: str,
    target_variable: str = Form(...),
    intervention_variable: str = Form(...),
    intervention_value: float = Form(...),
):
    state = _runs.get(run_id)
    if not state:
        raise HTTPException(status_code=404, detail="Run not found")
    if not state.data_path:
        raise HTTPException(status_code=400, detail="No data uploaded for this run")

    df = load_dataframe(state.data_path)
    if df is None:
        raise HTTPException(status_code=400, detail="Could not load data file")

    model = train_surrogate(df, target_variable)
    if not model:
        raise HTTPException(
            status_code=400,
            detail="Could not train model. Check that target variable has enough numeric data.",
        )

    result = counterfactual_predict(model, df, intervention_variable, intervention_value)
    if not result:
        raise HTTPException(
            status_code=400,
            detail="Simulation failed. Check that intervention variable exists in data.",
        )

    return {
        "target_variable": result.target_variable,
        "intervention_variable": result.intervention_variable,
        "intervention_value": result.intervention_value,
        "baseline_outcome": result.baseline_outcome,
        "predicted_outcome": result.predicted_outcome,
        "delta": result.delta,
        "ci_lower": result.ci_lower,
        "ci_upper": result.ci_upper,
    }


@router.get("/runs/{run_id}/report")
def get_report(run_id: str):
    state = _runs.get(run_id)
    if not state:
        raise HTTPException(status_code=404, detail="Run not found")
    top = state.top_hypotheses
    return {
        "research_goal": state.research_goal,
        "meta_review_report": state.meta_review_report,
        "hypothesis_count": len(state.hypotheses),
        "simulation_count": len(state.simulations),
        "protocol_count": len(state.protocols),
        "top_hypothesis_title": top[0].title if top else None,
        "top_hypothesis_score": (
            round(
                (top[0].novelty_score + top[0].causal_rigor_score + top[0].testability_score + top[0].impact_score) / 4.0,
                2,
            )
            if top
            else None
        ),
    }
