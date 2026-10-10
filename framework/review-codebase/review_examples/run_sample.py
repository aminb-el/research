#!/usr/bin/env python3
"""Review helper added for admissions packaging in August 2026.

This file is NOT an original historical research artifact. It exercises the unchanged
V3.2 formula engine on five rows copied directly from the V3.5 target-free LIAR scorer output.
It does not use benchmark targets.
"""
from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from formula_engine_relevance_gated_v3_2 import compute_all, validate_scores

sample = ROOT / "review_examples" / "liar_first_5_numeric_inputs.csv"
df = pd.read_csv(sample)
issues = validate_scores(df)
if issues:
    print("Validation notes:")
    for issue in issues:
        print(" -", issue)
else:
    print("Validation notes: none")

out = compute_all(df)
cols = [
    "item_id", "dataset", "tested_output",
    "T_abs_model", "T_perc_model", "I_model", "model_score"
]
print("\nComputed outputs for the five target-free sample rows:")
print(out[cols].to_string(index=False))
