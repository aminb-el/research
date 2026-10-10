# Truth, Perceived Truth, and Importance — Python codebase

**MIT Maker Portfolio: reviewer-facing code and reproducible demonstration.**

- [Project overview and interactive demonstration](https://aminb-el.github.io/me/truthportfolio/index.html)
- [Interactive scoring interface](https://aminb-el.github.io/me/truthportfolio/interactive.html)
- [Original research papers and full archives](https://github.com/aminb-el/research/tree/main/framework)

## What this folder contains

- `code/formula_engine_relevance_gated_v3_2.py` — the surviving owner-side Python implementation of evidence-weighted truth, perceived truth, and receiver-dependent importance. Includes the V3.2 root-normalization correction.
- `code/evaluate_external_outputs_v3_2.py` — owner-side benchmark evaluation script; requires target files that are **not** included here.
- `review_examples/run_sample.py` — reviewer-oriented runnable demonstration of the original formula engine.
- `review_examples/liar_first_5_numeric_inputs.csv` — the required numeric/input columns from the **first five original V3.5 LIAR scorer rows**, preserving original values while omitting text rationales.
- `requirements.txt` — Python dependencies.

## Run the included code demonstration

From this directory, using Python:

```bash
python -m pip install -r requirements.txt
python review_examples/run_sample.py
```

It validates five target-free score-input rows, computes all three outputs, and prints the results. Benchmark target labels are **not** inputs to the scoring engine.

## Provenance and scope

The two files in `code/` are unchanged from the surviving V3.2 owner-side source package; the review script and compact input excerpt were prepared for inspection. The full source/scorer archives, technical papers, and historical outputs are in the parent [framework](https://github.com/aminb-el/research/tree/main/framework) directory. This folder is a reviewer-friendly presentation of surviving materials, **not a reconstructed historical Git commit history**.

The code expresses an independently developed modeling framework with AI-assisted work in organization, presentation, checking logs/results, and occasional code troubleshooting. External AI models also assigned atomic scores under an evaluation protocol. The reported benchmark tests are preliminary and do not establish that the system is free of bias.

## Notes

The owner-side evaluator joins separately held target files to calculate benchmark metrics, so it is available for code inspection but is not fully reproducible from this folder alone. The separate five-row demonstration above runs without benchmark targets.
