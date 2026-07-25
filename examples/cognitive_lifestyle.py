import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)
n = 600

df = pd.DataFrame({
    "sleep_hours": np.clip(np.random.normal(7.0, 1.4, n), 3.5, 10.5),
    "activity_minutes": np.clip(np.random.normal(45, 30, n), 0, 180),
    "caffeine_mg": np.clip(np.random.normal(120, 80, n), 0, 450),
    "age": np.random.randint(18, 55, n),
    "screen_time_hours": np.clip(np.random.normal(6.5, 2.2, n), 1, 14),
})

# Inject realistic causal relationships
df["cognitive_score"] = (
    55
    + df["sleep_hours"] * 3.8
    + df["activity_minutes"] * 0.12
    - df["caffeine_mg"] * 0.015
    - df["screen_time_hours"] * 1.1
    - (df["age"] - 30) * 0.15
    + np.random.normal(0, 6, n)
)

df["stress_level"] = (
    4.5
    - df["sleep_hours"] * 0.35
    - df["activity_minutes"] * 0.012
    + df["caffeine_mg"] * 0.004
    + df["screen_time_hours"] * 0.28
    + np.random.normal(0, 0.9, n)
)

df["cognitive_score"] = df["cognitive_score"].clip(20, 100).round(1)
df["stress_level"] = df["stress_level"].clip(1, 10).round(1)

# Save
path = Path("data/cognitive_lifestyle_sample.csv")
path.parent.mkdir(exist_ok=True)
df.to_csv(path, index=False)
print(f"Saved → {path}")
print(df.describe().round(2))