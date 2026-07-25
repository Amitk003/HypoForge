import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from src.orchestrator import run_pipeline
from src.state import HypothesisState


def generate_sample_data() -> str:
    np.random.seed(42)
    n = 500
    df = pd.DataFrame({
        "temperature": np.random.randn(n) * 3 + 25,
        "green_space_pct": np.random.rand(n) * 80,
        "pm25": np.random.randn(n) * 8 + 35,
        "traffic_density": np.random.rand(n) * 1500,
        "surface_albedo": np.random.rand(n) * 0.3 + 0.1,
        "building_height": np.random.rand(n) * 30 + 5,
    })
    df["temperature"] = df["temperature"] - df["green_space_pct"] * 0.04 + df["building_height"] * 0.02
    df["pm25"] = df["pm25"] + df["traffic_density"] * 0.008 - df["green_space_pct"] * 0.01
    path = str(Path(__file__).parent.parent / "data" / "urban_climate_sample.csv")
    df.to_csv(path, index=False)
    return path


if __name__ == "__main__":
    print("Generating urban climate sample data...")
    data_path = generate_sample_data()

    state = HypothesisState(
        research_goal="How does urban green space cover affect local air temperature and PM2.5 levels?",
        data_path=data_path,
    )

    print("Running HypoForge pipeline...")
    result = run_pipeline(state)

    print(f"\nPipeline complete: {len(result.hypotheses)} hypotheses generated.")
    print(f"Top hypothesis: {result.top_hypotheses[0].title}")
    print(f"Novelty: {result.top_hypotheses[0].novelty_score:.2f}")
    print(f"Testability: {result.top_hypotheses[0].testability_score:.2f}")

    report_path = Path(__file__).parent.parent / "hypoforge_report_urban_climate.md"
    report_path.write_text(result.meta_review_report)
    print(f"\nMeta-review report saved to: {report_path}")
