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
        "sleep_quality": np.random.rand(n) * 10 + 50,
        "aqi_exposure": np.random.rand(n) * 100 + 20,
        "ambient_noise_db": np.random.rand(n) * 30 + 40,
        "physical_activity_min": np.random.randint(0, 120, n),
        "heart_rate_variability": np.random.randn(n) * 10 + 60,
    })
    df["sleep_quality"] = df["sleep_quality"] - df["aqi_exposure"] * 0.15 - df["ambient_noise_db"] * 0.1 + df["physical_activity_min"] * 0.05
    df["heart_rate_variability"] = df["heart_rate_variability"] - df["aqi_exposure"] * 0.08 + df["physical_activity_min"] * 0.03
    path = str(Path(__file__).parent.parent / "data" / "health_environment_sample.csv")
    df.to_csv(path, index=False)
    return path


if __name__ == "__main__":
    print("Generating environmental health sample data...")
    data_path = generate_sample_data()

    state = HypothesisState(
        research_goal="How do air quality and noise exposure affect sleep quality and heart rate variability?",
        data_path=data_path,
    )

    print("Running HypoForge pipeline...")
    result = run_pipeline(state)

    print(f"\nPipeline complete: {len(result.hypotheses)} hypotheses generated.")
    for h in result.top_hypotheses[:3]:
        print(f"  - {h.title} (score: {h.novelty_score:.2f})")
