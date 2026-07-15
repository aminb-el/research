# Prime-gap repeat analysis — final package

## Flagship paper

- `paper/prime_gap_repeat_analysis.pdf`
- `paper/prime_gap_repeat_analysis.tex`
- `paper/figures/`

The paper presents the approved count-first analysis:

1. Total real repeats versus unrestricted exact shuffle.
2. Scale trend and bootstrap uncertainty.
3. Gap-range contribution and Kitagawa decomposition.
4. Modulo-3 as an explanatory mechanism, not a removed component.
5. Exact shuffle versus corrected Hardy–Poisson.
6. Exhaustive hybrid exact-gap/range test of Hardy–Poisson marginal accuracy.
7. Scale-adjusted Hardy–Poisson repeat predictor.
8. The retained clean constant candidates:
   - `exp(-1/(e-1) - 4/ln(x))`
   - `exp(-gamma - (4 + gamma^2/2)/ln(x))`
9. Limitations and claim discipline.

## Supplementary material

- `supplementary/data/`: selected analysis-ready tables and model comparisons.
- `supplementary/workbook/`: interactive results workbook.
- `supplementary/code/`: total-count statistical pipeline.
- `reports/`: concise methodological summaries.

## Scope

The original prime-generation computation is treated as fixed input. This package analyzes the resulting data; it does not rerun or audit the three-day prime computation. The clean constant formulas are empirical conjectures, not proven identities or asymptotic laws.
