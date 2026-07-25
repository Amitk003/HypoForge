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
        "species_richness": np.random.randint(5, 50, n),
        "annual_temp": np.random.randn(n) * 1.5 + 15,
        "precipitation_mm": np.random.randn(n) * 100 + 800,
        "habitat_area_km2": np.random.rand(n) * 100 + 10,
        "human_population": np.random.randint(100, 50000, n),
    })
    df["species_richness"] = df["species_richness"] + df["habitat_area_km2"] * 0.1 - df["annual_temp"] * 1.5
    df["species_richness"] = df["species_richness"].clip(lower=0).astype(int)
    path = str(Path(__file__).parent.parent / "data" / "biodiversity_sample.csv")
    df.to_csv(path, index=False)
    return path


if __name__ == "__main__":
    print("Generating biodiversity sample data...")
    data_path = generate_sample_data()

    state = HypothesisState(
        research_goal="How do temperature and precipitation changes affect local species richness in fragmented habitats?",
        data_path=data_path,
    )

    print("Running HypoForge pipeline...")
    result = run_pipeline(state)

    print(f"\nPipeline complete: {len(result.hypotheses)} hypotheses generated.")
    print(f"Top hypothesis: {result.top_hypotheses[0].title}")
    if result.simulations:
        print(f"Simulations run: {len(result.simulations)}")
    if result.protocols:
        print(f"Protocols designed: {len(result.protocols)}")

    report_path = Path(__file__).parent.parent / "hypoforge_report_biodiversity.md"
    report_path.write_text(result.meta_review_report)
    print(f"\nMeta-review report saved to: {report_path}")
