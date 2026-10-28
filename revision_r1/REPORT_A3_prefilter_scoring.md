# A3 · Prefilter audit: scoring of the coded sheet (D1, X2)

Coded sheet returned on 2026-10-26 as a Numbers file. Numbers only.

**Primary analysis (protocol Amendment 2, §9):** all 370 rows. An unlabelled row counts as an error of whichever classifier is being evaluated:
- against the production prefilter, human KEEP is set to the opposite of the production label;
- against the full-abstract re-run, human KEEP is set to the opposite of the full-abstract label;
- in the PILOT rows, it counts as a disagreement.

**Secondary analysis:** the originally pre-specified rule (protocol §6), which excludes unlabelled rows. It uses the frozen `a4_score_prefilter.py`.

**Timing of Amendment 2:** it was decided when the sheet was returned, before any A3 result was computed.

## Input checks

| Check | Result |
|---|---|
| Original file | `prefilter_audit_Tcomplete.numbers`, SHA-256 `76b32339…ca9398`, unchanged |
| How it was read | A copy was exported to CSV with Numbers |
| Copy of record | `.numbers` file and CSV in `revision_r1/coding/completed/` (`prefilter_import_log.txt`) |
| Row IDs | 370/370 present |
| Titles and abstracts | Identical to the template row by row, so no re-sorting |
| Label values | Only valid labels, or blank |
| Unlabelled rows | **1** (EX-F stratum, 2023, note "Can't tell"; also marked borderline) |
| Borderline = Y | 9 rows |
| Notes | 10 rows |

## Primary results (N = 370)

Full output: [outputs/A4_prefilter_primary/prefilter_scores.md](outputs/A4_prefilter_primary/prefilter_scores.md). Long format: `prefilter_scores_long.csv`.

Method:
- **KEEP** means discourse or evaluative.
- **Weights:** by stratum × year, equal to the frame size divided by the number of coded records.
- **95% CIs:** bootstrap with 1000 resamples within cells, seed 42.

**Production prefilter, population-weighted 2×2 (2021–2025):**

| Metric | Estimate (95% CI) |
|---|---|
| Sensitivity | 78.5% (71.7–85.6) |
| Specificity | 99.5% (98.7–100.0) |
| PPV | 97.6% (93.7–100.0) |
| NPV | 94.8% (92.6–96.8) |
| Cohen κ | 0.842 (0.782–0.897) |
| Gwet AC1 | 0.933 (0.903–0.958) |

**False negatives among the excluded records** (1 − NPV; estimated number of missed AI-engaged records):

| Year | 1 − NPV | Missed records | PPV among retained |
|---|---|---|---|
| 2021 | 2.0% (1.3–2.5) | 202 (128–257) | 100% (10/10) |
| 2022 | 4.4% (1.9–9.1) | 518 (220–1,071) | 90% (9/10) |
| 2023 | 6.7% (2.0–13.6) | 812 (241–1,642) | 90% (9/10) |
| 2024 | 2.6% (1.6–3.3) | 404 (257–514) | 100% (10/10) |
| 2025 | 7.9% (3.4–14.1) | 1,812 (773–3,222) | 100% (10/10) |
| **Pooled 2021–2025** | **5.2% (3.2–7.4)** | **3,747 (2,332–5,398)** | **97.6% (93.7–100.0)** |

- **By period:** 1 − NPV was 3.3% (1.8–5.9) in 2021–2022 and 5.7% (3.0–9.4) in 2024–2025. The difference is +2.5 pp (−1.6 to 6.4).
- **Logistic test of year on human KEEP** within the excluded strata, adjusted for stratum: OR 1.263 per year (Wald 95% CI 0.898–1.776), P = .18. The design-weighted OR is 1.267 (bootstrap 0.940–1.760).

**Full-abstract re-run:**

| Metric | Estimate (95% CI) |
|---|---|
| Precision within EX-F (human KEEP rate), pooled | 80.4% (71.7–89.0) |
| — by year, 2021 → 2025 | 73.3%, 80.0%, 66.7%, 73.3%, 93.3% |
| Population-weighted sensitivity | 82.0% (72.1–91.9) |
| Population-weighted specificity | 99.3% (99.0–99.6) |
| Population-weighted κ | 0.862 (0.785–0.931) |

**Intra-rater agreement** (20 PILOT rows: your original `my_label` against the new code): 19/20 agree (95.0%), for both 3 classes and KEEP/DROP. KEEP/DROP κ is 0.773; 3-class κ is 0.780.

**Borderline sensitivity analyses** (pooled):

| Borderline rows treated as | 1 − NPV | Production sensitivity | Production κ |
|---|---|---|---|
| application | 4.4% (2.9–6.3) | 81.0% | 0.860 |
| KEEP | 5.4% (3.4–7.6) | 77.9% | 0.837 |

**3-class tables:** the coded-sample confusion tables (human against the production label, and human against the full-abstract label) are in the full output. The unlabelled row appears there as its own row.

### Zero-event cells and intervals robust to them (protocol Amendment 3)

Five stratum-year cells have no variation:
- EX-S 2021: 0/45 human KEEP;
- EX-S 2024: 0/45 human KEEP;
- RET 2021, 2024 and 2025: 10/10 human KEEP.

The within-cell bootstrap cannot vary these cells, so the bootstrap intervals above understate the uncertainty. Amendment 3 adds two kinds of interval. It was made after the primary results were known, at the authors' request.

Full output: [outputs/A4_prefilter_exact_ci/prefilter_exact_ci.md](outputs/A4_prefilter_exact_ci/prefilter_exact_ci.md). Single-cell table: `prefilter_cell_exact_ci.csv`.

- **Single cells: exact Clopper–Pearson.**
  - EX-S (human KEEP among excluded records): 0/45 = 0% (0.0–7.9) in 2021 and 2024; 1/45 = 2.2% (0.1–11.8) in 2022; 2/45 = 4.4% (0.5–15.1) in 2023 and 2025.
  - RET (PPV among retained records): 10/10 = 100% (69.2–100) in 2021, 2024 and 2025; 9/10 = 90% (55.5–99.7) in 2022 and 2023.
  - EX-F (full-abstract precision): from 10/15 = 66.7% (38.4–88.2) in 2023 to 14/15 = 93.3% (68.1–99.8) in 2025.
- **Weighted combinations: Jeffreys posterior simulation.** Each cell's proportion is drawn 10,000 times from Beta(k+½, n−k+½), and the weighted estimate is recomputed on each draw. No exact interval exists for a weighted combination of cells. Results for the primary analysis:

| Estimand | Estimate | Jeffreys 95% interval | Bootstrap 95% interval |
|---|---|---|---|
| 1 − NPV pooled 2021–2025 | 5.2% | 4.1–8.9 | 3.2–7.4 |
| 1 − NPV 2021 / 2024 | 2.0% / 2.6% | 1.6–7.3 / 2.0–7.6 | 1.3–2.5 / 1.6–3.3 |
| 1 − NPV 2024–25 minus 2021–22 | +2.5 pp | −2.5 to 7.6 | −1.6 to 6.4 |
| Missed AI-engaged records, total | 3,747 | 2,946–6,447 | 2,332–5,398 |
| PPV among retained, pooled | 97.6% | 84.8–98.1 | 93.7–100.0 |
| Full-abstract precision (EX-F), pooled | 80.4% | 69.0–86.2 | 71.7–89.0 |
| Production sensitivity | 78.5% | 66.8–81.7 | 71.7–85.6 |
| Production specificity | 99.5% | 97.0–99.6 | 98.7–100.0 |
| Production NPV | 94.8% | 91.1–95.9 | 92.6–96.8 |
| Production κ | 0.842 | 0.713–0.856 | 0.782–0.897 |
| Production AC1 | 0.933 | 0.873–0.941 | 0.903–0.958 |

- **Shape of the Jeffreys intervals.** They are asymmetric, and for the zero-event years they are much wider upward. The Jeffreys prior moves a 0/45 cell to a posterior mean of about 1.1%, and that is multiplied by frames of roughly 10,000–22,000 records. For the same reason the lower bounds of PPV and κ fall below the bootstrap bounds.
- **Full-abstract 2×2: Jeffreys intervals not used.** This table must split RET cells by full-abstract label, leaving sub-cells of n = 1–3. For full-abstract specificity and PPV, the Jeffreys interval excludes the point estimate. Report the bootstrap interval for that table.
- **Coverage check.** Every other Jeffreys interval contains its point estimate. The point estimates were recomputed at cell level and asserted equal to the frozen estimator.

## Secondary: originally pre-specified analysis (369 labelled rows)

Output: [outputs/A4_prefilter_secondary_excl_blank/prefilter_scores.md](outputs/A4_prefilter_secondary_excl_blank/prefilter_scores.md)

Only EX-F 2023 changes. The pooled estimates differ in the third decimal place:

| Metric | Secondary | Primary |
|---|---|---|
| Pooled 1 − NPV | 5.2% (3.2–7.4) | same |
| Missed records | 3,740 (2,336–5,369) | 3,747 |
| Production sensitivity / κ | 78.6% / 0.842 | 78.5% / 0.842 |
| Full-abstract precision | 81.2% (71.9–89.5) | 80.4% |

## For reference: Batch 1 pilot (T1)

These numbers come from a different sample and design. In the 200-record pilot (production labels, unweighted), sensitivity was 20/38 = 0.526 and NPV was 152/170 = 0.894.

## Checks

- `output/` checksums are unchanged in the worktree and the main checkout.
- No tracked file outside `revision_r1/` was modified.
- Nothing was pushed.
