# A1 · Theme-classifier validation: scoring of the coded sheet (D2a)

Coded sheet returned on 2026-10-26 (Numbers CSV export). Scored with the frozen `a4_score_theme.py` (protocol §6.1, Freeze 1 `0d21f6c`). Numbers only.

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
- **Handling:** the primary analysis excludes these 13 rows, as protocol §6 specifies, leaving **187** records.

## Primary results (pre-specified)

Full output: [outputs/A4_theme/theme_scores.md](outputs/A4_theme/theme_scores.md). Long format: `theme_scores_long.csv`.

95% CIs: bootstrap with 1000 resamples within year, seed 42. "Weighted" means weighted to the frame by year.

| Metric | Unweighted | Weighted |
|---|---|---|
| micro-F1 | 0.919 (0.897–0.940) | 0.926 (0.901–0.948) |
| macro-F1 | 0.840 (0.760–0.899) | 0.829 (0.742–0.895) |
| exact-match ratio | 0.743 (0.679–0.807) | 0.759 (0.688–0.828) |
| Hamming loss | 0.034 (0.025–0.044) | 0.031 (0.022–0.041) |
| mean Jaccard | 0.879 (0.847–0.910) | 0.885 (0.843–0.920) |
| mean n themes, human / model | 2.08 / 2.16 | 2.10 / 2.13 |

**Per-theme results** (unweighted precision / recall / F1; n = human-positive records):

| Theme | n | Precision | Recall | F1 | Note |
|---|---|---|---|---|---|
| hallucination | 68 | 0.970 | 0.956 | 0.963 | |
| safety_clinical | 110 | 0.913 | 0.955 | 0.933 | |
| ethics_bias | 70 | 0.914 | 0.914 | 0.914 | |
| regulation | 85 | 0.943 | 0.965 | 0.953 | |
| cognitive | 12 | 0.857 | 1.000 | 0.923 | |
| data_privacy | 18 | 0.737 | 0.778 | 0.757 | |
| education | 8 | 0.875 | 0.875 | 0.875 | insufficient support |
| existential | 9 | 0.778 | 0.778 | 0.778 | insufficient support |
| replacement | 6 | 0.667 | 1.000 | 0.800 | insufficient support |
| other | 3 | 0.400 | 0.667 | 0.500 | insufficient support |

"Insufficient support" means fewer than 10 human-positive records.

**By year band** (weighted):

| Band | micro-F1 | macro-F1 |
|---|---|---|
| 2021–2022 | 0.921 (0.886–0.951) | 0.875 (0.776–0.934) |
| 2023 | 0.907 (0.847–0.959) | 0.657 (0.517–0.859) |
| 2024–2025 | 0.931 (0.898–0.961) | 0.882 (0.745–0.957) |

The 2023 macro-F1 is lower because several rare themes have few or no positives in that band.

**Number of themes per record, human × model:** the diagonal (1/1, 2/2, 3/3) holds 147 of 187 records.

## Post-hoc sensitivity (not pre-specified)

[outputs/A4_theme/theme_scores_posthoc.md](outputs/A4_theme/theme_scores_posthoc.md)

This analysis keeps the 13 no-theme rows as empty human sets, so every model theme on them counts as a false positive. It was added after the sheet was returned and is logged in the protocol change log.

| Metric | Unweighted | Weighted |
|---|---|---|
| micro-F1 | 0.885 (0.855–0.914) | 0.888 (0.853–0.919) |
| exact match | 0.695 | 0.708 |
| mean Jaccard | 0.822 | 0.825 |

The precision of the large themes falls to 0.82–0.90 (unweighted).

## Checks

- `output/` checksums are unchanged in the worktree and the main checkout.
- No tracked file outside `revision_r1/` was modified.
- Nothing was pushed.
