# CDOT Priority Cells Briefing — CONVLSTM

Generated from **CONVLSTM** predictions on the forward holdout test period.

## Headline

- **25** CRITICAL cells, top 1% predicted risk
- **100** HIGH cells, top 1–5%
- The top **200** flagged cells captured **15.4%** of actual severe crashes during the test period.

## Top 10 cells

|   rank | tier     |    lat |     lon |   pred |   true |
|-------:|:---------|-------:|--------:|-------:|-------:|
|      1 | CRITICAL | 41.718 | -87.543 |  3.942 |  0.000 |
|      2 | CRITICAL | 41.828 | -87.603 |  1.897 |  2.000 |
|      3 | CRITICAL | 41.922 | -87.633 |  1.889 |  1.000 |
|      4 | CRITICAL | 41.847 | -87.612 |  1.690 |  1.000 |
|      5 | CRITICAL | 41.822 | -87.597 |  1.674 |  0.000 |
|      6 | CRITICAL | 41.833 | -87.603 |  1.557 |  0.000 |
|      7 | CRITICAL | 41.928 | -87.633 |  1.556 |  0.000 |
|      8 | CRITICAL | 41.833 | -87.608 |  1.493 |  3.000 |
|      9 | CRITICAL | 41.722 | -87.543 |  1.478 |  0.000 |
|     10 | CRITICAL | 41.837 | -87.608 |  1.318 |  2.000 |

## What CDOT should do with this list

1. Cross-check against existing Vision Zero High Crash Corridors.
2. Field-audit the top 20–30 cells before any infrastructure spend.
3. Pair with community input before enforcement-based interventions.
4. Track post-intervention crash counts and feed back into retraining.

## Methodology notes

- Model used: **CONVLSTM**
- Cell resolution: 500m × 500m.
- Time resolution: 6-hour windows.
- This list is a starting point for corridor audits, not a substitute for field validation.
