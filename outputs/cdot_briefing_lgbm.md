# CDOT Priority Cells Briefing — LGBM

Generated from **LGBM** predictions on the forward holdout test period.

## Headline

- **24** CRITICAL cells, top 1% predicted risk
- **97** HIGH cells, top 1–5%
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

1. Cross-check against existing Vision Zero High Crash Corridors.
2. Field-audit the top 20–30 cells before any infrastructure spend.
3. Pair with community input before enforcement-based interventions.
4. Track post-intervention crash counts and feed back into retraining.

## Methodology notes

- Model used: **LGBM**
- Cell resolution: 500m × 500m.
- Time resolution: 6-hour windows.
- This list is a starting point for corridor audits, not a substitute for field validation.
