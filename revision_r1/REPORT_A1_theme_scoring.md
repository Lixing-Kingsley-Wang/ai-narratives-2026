# A1 · Theme-classifier validation: scoring of the coded sheet (D2a)

Coded sheet returned on 2026-10-26 (Numbers CSV export). Numbers only.

**Primary analysis: all 200 sampled records** (protocol Amendment 1, §9). Records where the coder ticked no theme are scored as empty human sets, so every model theme on them counts as a false positive. The manuscript reports model themes for every critical record, including these.

**Secondary analysis:** the originally pre-specified rule (protocol §6), which excludes those records (n = 187).

**Timing of Amendment 1:** it was made after the sheet was returned and after the pre-specified analysis had been run. It lowers the agreement estimates.

## Input checks

| Check | Result |
|---|---|
| Source file | `Coding-Table 1.csv`, SHA-256 `e4d00724…81ef60` |
| Copy of record | `revision_r1/coding/completed/` (logged in `theme_import_log.txt`) |
| Conversion | Copied into the template format by `a4_import_theme_csv.py` |
| Row IDs | 200/200 present |
| Titles and abstracts | Identical to the template row by row (whitespace-normalised), so no re-sorting |
| Tick values | Only `1` or blank |
| Ticks per row | Never more than 3 |
| `n_themes` | Consistent with the ticks in every row |
| Rows with no ticked theme | 13 |

- **Rows with no ticked theme (13):** by year 1 / 3 / 3 / 4 / 2 (2021→2025). 12 carry a note ("can't tell", "no theme detected"). 9 of the 13 are title-only records; the sample has 21 title-only records in all.
- **What the model gave them:** 1 theme for 1 record, 2 themes for 6 records, 3 themes for 6 records.

## Primary results (N = 200)

Script: `a4_score_theme_n200.py`, which reuses the frozen `a4_score_theme.py` functions unchanged. Full output: [outputs/A4_theme_primary_n200/theme_scores.md](outputs/A4_theme_primary_n200/theme_scores.md). Long format: `theme_scores_long.csv`.

95% CIs: bootstrap with 1000 resamples within year, seed 42. "Weighted" means weighted to the frame by year.

| Metric | Unweighted | Weighted |
|---|---|---|
| micro-F1 | 0.885 (0.855–0.914) | 0.888 (0.853–0.919) |
| macro-F1 | 0.824 (0.747–0.881) | 0.813 (0.727–0.881) |
| exact-match ratio | 0.695 (0.635–0.765) | 0.708 (0.630–0.782) |
| Hamming loss | 0.048 (0.036–0.059) | 0.046 (0.033–0.059) |
| mean Jaccard | 0.822 (0.779–0.863) | 0.825 (0.773–0.872) |
| mean n themes, human / model | 1.95 / 2.17 | 1.95 / 2.16 |

**Per-theme results** (unweighted precision / recall / F1, with 95% CI on F1; n = human-positive records):

| Theme | n | Precision | Recall | F1 (95% CI) | Note |
|---|---|---|---|---|---|
| hallucination | 68 | 0.844 | 0.956 | 0.897 (0.839–0.942) | |
| safety_clinical | 110 | 0.820 | 0.955 | 0.882 (0.834–0.921) | |
| ethics_bias | 70 | 0.901 | 0.914 | 0.908 (0.855–0.954) | |
| regulation | 85 | 0.872 | 0.965 | 0.916 (0.872–0.956) | |
| cognitive | 12 | 0.857 | 1.000 | 0.923 (0.783–1.000) | |
| data_privacy | 18 | 0.737 | 0.778 | 0.757 (0.571–0.897) | |
| education | 8 | 0.875 | 0.875 | 0.875 | insufficient support |
| existential | 9 | 0.778 | 0.778 | 0.778 | insufficient support |
| replacement | 6 | 0.667 | 1.000 | 0.800 | insufficient support |
| other | 3 | 0.400 | 0.667 | 0.500 | insufficient support |

"Insufficient support" means fewer than 10 human-positive records.

**By year band** (weighted):

| Band | micro-F1 | macro-F1 |
|---|---|---|
| 2021–2022 | 0.897 (0.856–0.934) | 0.861 (0.765–0.923) |
| 2023 | 0.861 (0.784–0.929) | 0.636 (0.492–0.820) |
| 2024–2025 | 0.892 (0.845–0.934) | 0.864 (0.702–0.938) |

The 2023 macro-F1 is lower because several rare themes have few or no positives in that band.

**Number of themes per record, human × model:**
- 147 of 200 records fall on the diagonal (1/1, 2/2, 3/3).
- The 13 records with no human theme received 1, 2 or 3 model themes (1, 6 and 6 records respectively).

## Secondary: originally pre-specified analysis (N = 187)

Script: frozen `a4_score_theme.py`. Output: [outputs/A4_theme/theme_scores.md](outputs/A4_theme/theme_scores.md).

| Metric | Unweighted | Weighted |
|---|---|---|
| micro-F1 | 0.919 (0.897–0.940) | 0.926 (0.901–0.948) |
| macro-F1 | 0.840 | 0.829 |
| exact match | 0.743 | 0.759 |
| mean Jaccard | 0.879 | 0.885 |

- **Recall** is identical in the two analyses, because the 13 records add no human positives.
- **Precision** is higher in the secondary analysis. For the four large themes it is 0.91–0.97 here, against 0.82–0.90 in the primary.

`outputs/A4_theme/theme_scores_posthoc.md` was an earlier version of the N=200 analysis. Its estimates are identical to the primary results above, and it is superseded by `outputs/A4_theme_primary_n200/`.

## Checks

- `output/` checksums are unchanged in the worktree and the main checkout.
- No tracked file outside `revision_r1/` was modified.
- Nothing was pushed.
