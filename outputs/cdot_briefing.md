# CDOT Priority Cells Briefing

Generated from LightGBM-Poisson predictions on the forward holdout test period (2025-04-05 → 2025-12-31).

## Headline

- **24** CRITICAL cells (top-1% predicted risk)
- **97** HIGH cells (top 1-5%)
- The top **200** flagged cells captured **26.1%** of actual severe crashes during the test period.

## Top 10 cells

|   rank | tier     |    lat |     lon |   pred |   true |
|-------:|:---------|-------:|--------:|-------:|-------:|
|      1 | CRITICAL | 41.888 | -87.623 |  6.351 |      3 |
|      2 | CRITICAL | 41.892 | -87.633 |  5.112 |      3 |
|      3 | CRITICAL | 41.877 | -87.627 |  4.795 |      3 |
|      4 | CRITICAL | 41.752 | -87.588 |  4.489 |      2 |
|      5 | CRITICAL | 41.767 | -87.623 |  3.876 |      2 |
|      6 | CRITICAL | 41.883 | -87.627 |  3.800 |      4 |
|      7 | CRITICAL | 41.888 | -87.633 |  3.788 |      1 |
|      8 | CRITICAL | 41.892 | -87.638 |  3.785 |      2 |
|      9 | CRITICAL | 41.737 | -87.588 |  3.774 |      3 |
|     10 | CRITICAL | 41.883 | -87.638 |  3.696 |      1 |

## What CDOT should do with this list

1. Cross-check against existing Vision Zero High Crash Corridors. Cells already on that list confirm the model; new cells are candidates for the next planning cycle.
2. Field-audit the top 20-30 cells with engineering staff before any infrastructure spend.
3. Pair with community input before deploying enforcement-based interventions, particularly in the cells flagged in the equity audit.
4. Track post-intervention crash counts in treated cells and feed back into the next model retraining.

## Methodology notes

- Predictions based on 2023-Jan to 2025-Apr training; tested on 2025-Apr to 2025-Dec.
- Cell resolution: 500m × 500m. Time resolution: 6-hour windows.
- This list is a starting point for corridor audits, not a substitute for field validation.
- The equity audit flags areas where predictions should be checked against demographic context before deployment.
