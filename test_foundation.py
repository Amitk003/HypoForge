import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.state import HypothesisState
from src.orchestrator import run_pipeline
from src.data_engine import load_dataframe, summarize_dataframe


def test_pipeline_no_data():
    state = HypothesisState(research_goal="How does urban green space affect air temperature?")
    result = run_pipeline(state)
    assert len(result.literature_context) > 0
    assert result.pipeline_stage == "complete"
    print("test_pipeline_no_data PASSED")


def test_data_engine():
    import pandas as pd
    import numpy as np
    df = pd.DataFrame({
        "temperature": np.random.randn(100) + 20,
        "green_space": np.random.rand(100) * 100,
        "pm25": np.random.randn(100) * 10 + 30,
        "traffic": np.random.rand(100) * 1000,
    })
    summary = summarize_dataframe(df)
    assert "Shape: 100 rows x 4 columns" in summary
    print("test_data_engine PASSED")


if __name__ == "__main__":
    test_data_engine()
    test_pipeline_no_data()
    print("\nAll foundation tests passed.")
