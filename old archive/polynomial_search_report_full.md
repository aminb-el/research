# Polynomial Search Report

Generated: 2026-01-28 13:18:38

## Data included

This report summarizes the current in-memory computation outputs: `results_df` (saved candidates) and `results_topk_df` (top-1000).

- results_df rows: 309268
- results_topk_df rows: 1000

## Global distribution of saved candidates

|               |   count |        mean |         std |        min |         50% |         90% |         95% |         99% |       max |
|:--------------|--------:|------------:|------------:|-----------:|------------:|------------:|------------:|------------:|----------:|
| density       |  309268 |    0.263836 |   0.0613206 |   0.1028   |    0.2594   |    0.3476   |    0.3716   |    0.4154   |    0.5468 |
| early_density |  309268 |    0.422382 |   0.104847  |   0.253333 |    0.413333 |    0.573333 |    0.613333 |    0.693333 |    1      |
| max_streak    |  309268 |    5.45308  |   2.2606    |   2        |    5        |    8        |    9        |   12        |   80      |
| total_primes  |  309268 | 1319.18     | 306.603     | 514        | 1297        | 1738        | 1858        | 2077        | 2734      |

Interpretation: the median density is around the 0.26 range, while the best observed density is 0.5468, which is deep in the extreme tail.

## Best observed polynomials (top 20 by density)

|       |   a |    b |    c |   density |   early_density |   max_streak |   total_primes |
|------:|----:|-----:|-----:|----------:|----------------:|-------------:|---------------:|
| 53783 |   1 | 2329 | 1697 |    0.5468 |        0.826667 |           18 |           2734 |
| 53838 |   1 | 2331 | 4027 |    0.5468 |        0.826667 |           18 |           2734 |
| 44325 |   1 | 1837 | 1013 |    0.5154 |        0.826667 |           16 |           2577 |
| 35962 |   1 | 1417 |  743 |    0.514  |        0.773333 |           13 |           2570 |
| 36031 |   1 | 1419 | 2161 |    0.5138 |        0.76     |           12 |           2569 |
| 36075 |   1 | 1421 | 3581 |    0.5138 |        0.76     |           12 |           2569 |
| 31048 |   1 | 1183 |  359 |    0.5084 |        0.8      |           13 |           2542 |
| 31103 |   1 | 1185 | 1543 |    0.5084 |        0.8      |           13 |           2542 |
| 31160 |   1 | 1187 | 2729 |    0.5082 |        0.8      |           13 |           2541 |
| 31240 |   1 | 1189 | 3917 |    0.508  |        0.8      |           13 |           2540 |
| 51651 |   1 | 2217 | 3643 |    0.5068 |        0.786667 |           12 |           2534 |
| 51596 |   1 | 2215 | 1427 |    0.5068 |        0.786667 |           12 |           2534 |
| 30276 |   1 | 1147 |  839 |    0.5036 |        0.8      |           14 |           2518 |
| 30344 |   1 | 1149 | 1987 |    0.5036 |        0.8      |           14 |           2518 |
| 30386 |   1 | 1151 | 3137 |    0.5034 |        0.8      |           14 |           2517 |
| 30442 |   1 | 1153 | 4289 |    0.5032 |        0.786667 |           14 |           2516 |
| 54329 |   1 | 2357 | 1493 |    0.502  |        0.72     |           12 |           2510 |
| 54381 |   1 | 2359 | 3851 |    0.5018 |        0.706667 |           12 |           2509 |
| 34602 |   1 | 1351 |  827 |    0.4998 |        0.786667 |           10 |           2499 |
| 34651 |   1 | 1353 | 2179 |    0.4996 |        0.786667 |           10 |           2498 |

## Best density by a (coverage check)

|   a |   best_density |   median_density |   n_rows |
|----:|---------------:|-----------------:|---------:|
|   1 |         0.5468 |           0.2772 |    56944 |
|   2 |         0.4888 |           0.2688 |    56591 |
|   3 |         0.493  |           0.2632 |    39279 |
|   4 |         0.4764 |           0.2602 |    60574 |
|   5 |         0.4834 |           0.235  |    54691 |
|   6 |         0.467  |           0.256  |    41189 |

Interpretation: in the retained results, only a = 1..6 appear. This does not prove a >= 7 is bad; it means your kept-candidate set has no a>=7 rows at this checkpoint.

## Top-1000 composition by a

|   a |   n_topk |   best_density |   median_density |
|----:|---------:|---------------:|-----------------:|
|   1 |      503 |         0.5468 |           0.4558 |
|   2 |      249 |         0.4888 |           0.4612 |
|   3 |       54 |         0.493  |           0.4531 |
|   4 |      146 |         0.4764 |           0.4506 |
|   5 |       26 |         0.4834 |           0.4542 |
|   6 |       22 |         0.467  |           0.4535 |

## Metric relationships

Correlation matrix among key metrics:

|               |   density |   early_density |   max_streak |   total_primes |
|:--------------|----------:|----------------:|-------------:|---------------:|
| density       |  1        |        0.865515 |     0.677111 |       1        |
| early_density |  0.865515 |        1        |     0.660244 |       0.865515 |
| max_streak    |  0.677111 |        0.660244 |     1        |       0.677111 |
| total_primes  |  1        |        0.865515 |     0.677111 |       1        |

Interpretation: density and early_density are strongly positively correlated, and density tracks total_primes essentially perfectly in this dataset (likely because total_primes is derived from density times a fixed evaluation horizon).

## Early filter diagnostic

Fraction of saved candidates with early_density >= 0.8: 0.0013774460985294308
Fraction of saved candidates with early_density >= 0.8 AND density >= 0.45: 0.0004494483748722791

Interpretation: very few saved candidates have extremely high early_density, and an even smaller fraction turn into strong overall density. That makes early_density a useful but not sufficient proxy.

## Specific question you asked earlier: is a >= 7 plausibly better?

Based on the retained results at this checkpoint, there is no empirical support yet for a >= 7 beating the current best density 0.5468, because there are no retained rows with a >= 7. This indicates either the sweep hasn't produced kept candidates for those a values yet, or the filters excluded them.
