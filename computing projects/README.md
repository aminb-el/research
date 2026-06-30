# Computing Projects

This folder contains computational explorations connected to number theory and mathematical experimentation.

The files here are not presented as proofs, final papers, or current research claims. They are included as evidence of programming, search design, data collection, saved outputs, and exploratory mathematical testing.

## Main project: Prime-Polynomial Search

The main project in this folder is a large computational search over quadratic polynomials of the form:

```txt id="8m2m8c"
P(n) = a n^2 + b n + c
```

The goal was to search for polynomial parameter triples `(a, b, c)` that produce unusually high prime density over a fixed range of integer inputs.

This is a computational exploration, not a proof. It does not claim a theorem about prime-generating polynomials. Its value is in the search process, saved outputs, and the scale of the computation.

## Search scale

The saved checkpoint summarizes a run with:

```txt id="ruimkd"
a range:        1 to 10
b range:       -2500 to 2500
c values:       primes below 5002
n range:        1 to 5000
early test:     n = 1 to 75
saved results:  309,268 rows
top results:    top 1000 candidates
```

The checkpoint records:

```txt id="m6yscp"
tested candidates:   309,268
skipped candidates:  20,029,732
```

This means the search did not simply test a few famous examples. It generated, filtered, scored, saved, and summarized a large candidate space.

## Best observed result

The best observed density in the saved candidate set was:

```txt id="p3eem0"
density = 0.5468
```

Two top candidates reached this value:

```txt id="h8bqj0"
P(n) = n^2 + 2329n + 1697
P(n) = n^2 + 2331n + 4027
```

For the evaluation range `n = 1` to `5000`, each produced:

```txt id="7r29yz"
2734 prime values out of 5000
```

This is an extreme-tail result within the saved candidate set. The median saved-candidate density was around `0.2594`, while the best observed density was `0.5468`.

## Files

```txt id="hko1bw"
README.md
Collatz computations.md
polynomial_prime_search.cpp
polynomial_prime_search.exe
polynomial_search_state_summary.json
polynomial_search_summary.pdf
top_1000_results.csv
topk_by_a_summary.csv
best_by_a_summary.csv
json.hpp
hello
```

## File guide

### `polynomial_prime_search.cpp`

Main source file for the polynomial search program.

It includes:

```txt id="m83vdu"
prime checking
sieve-based optimization
early filtering
candidate evaluation
autosave/resume support
density scoring
top-result ranking
PDF report generation
```

Note: this file should eventually be renamed if the source is Python code rather than C++.

### `polynomial_prime_search.exe`

Executable version of the search tool, kept for convenience so the exact program used in the exploration can be run more easily.

The source file is included so the logic can be inspected rather than relying only on the executable.

### `polynomial_search_state_summary.json`

Compact checkpoint summary of the computation.

It records:

```txt id="2fcqcd"
search parameters
progress boundary
number of saved results
number of tested/skipped candidates
summary statistics for density, early density, max streak, and total prime count
```

### `top_1000_results.csv`

The top 1000 saved polynomial candidates ranked by search performance.

### `topk_by_a_summary.csv`

A summary of how the top 1000 candidates are distributed across different values of `a`.

### `best_by_a_summary.csv`

The best observed density, median density, and saved-row count for each retained value of `a`.

### `polynomial_search_summary.pdf`

A PDF summary report of the search output.

### `json.hpp`

Supporting header/dependency file retained with the project files.

### `Collatz computations.md`

A note pointing to older Collatz-style computational tools from my earlier GitHub account.

These Collatz materials are included only as programming and computational exploration history. They are not presented as a proof of the Collatz conjecture or as a current mathematical claim.

## Interpretation

The prime-polynomial search is useful because it shows:

```txt id="i21srk"
large-scale computational exploration
search-space design
early filtering
saved checkpoints
data summaries
ranking of results
statistical comparison across candidates
```

It should not be interpreted as:

```txt id="73h839"
a proof
a formal theorem
a completed research paper
a claim that the best observed polynomial is mathematically optimal
```

## Scope

The search is checkpoint-based and exploratory. The saved results reflect the retained candidate set and the state of the computation at that checkpoint. They do not prove that larger ranges, different coefficient bounds, or different filters would behave the same way.

This folder exists to document computational work that developed alongside my number theory projects.
