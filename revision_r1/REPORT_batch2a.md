# JMIR #109710 — R1 Batch 2a report (human-coding instruments)

Branch `jmir-r1-major-revision`, worktree `.claude/worktrees/jmir-r1-batch-1-fc3398`. Nothing pushed. LLM calls were made only in A2 (USD 40.35, against a USD 60 ceiling). The API key was read from the main checkout's `.env` without being printed, logged or committed; a grep of the committed raw responses and of `revision_r1/` finds no key string.

## A0 · Protocol and pre-specification (D1, X2, D2a)

Protocol: [coding/PROTOCOL_r1_validation.md](coding/PROTOCOL_r1_validation.md)

| Freeze | Commit | Time | Contents | Released |
|---|---|---|---|---|
| **Freeze 1** | `0d21f6c` | 2026-10-23 17:26 | Protocol; all sampling and labelling scripts (`a1_theme_sample.py`, `a2_prefilter_fullabstract_batch.py`, `a3_prefilter_sample.py`, `r1_coding.py`); A1 manifest, key and template | A1 workbook released to Peter after this commit |
| **Freeze 2** | `47cf6fe` | 2026-10-23 18:02 | A3 manifest, key and template | Before the A3 workbook is released |

- **Deviation from the brief: two freezes instead of one.** The brief asked for one commit that holds the protocol, sampling scripts, manifests and keys. That was not possible, because the A3 frames depend on the A2 results.
  - The A3 sampling script was frozen in Freeze 1. It was run unchanged after A2: `git diff 0d21f6c` on that script and its helper is empty.
  - Its outputs were committed as Freeze 2, before the A3 workbook is released.
  - The protocol states this, and its change log records Freeze 2.
- **Both freezes come before their workbooks are released.** The A1 workbook was announced only after `0d21f6c`; the A3 workbook is being released with this report, after `47cf6fe`.

## Instruments

**Do not open the key files.**

| | Template (give to coder) | Key (do not open) | Manifest |
|---|---|---|---|
| A1 themes | `revision_r1/coding/theme_validation_TEMPLATE.xlsx` | `revision_r1/coding/theme_key.csv` | `theme_sampling_manifest.csv` |
| A3 prefilter | `revision_r1/coding/prefilter_audit_TEMPLATE.xlsx` | `revision_r1/coding/prefilter_key.csv` | `prefilter_sampling_manifest.csv` |

- **What the workbooks contain.** Each has two visible sheets ("Read me first" and "Coding") and shows only `row_id`, title and the full abstract. An empty abstract is shown as `[No abstract available. Code from the title.]`.
- **Blinding check.** Each build script asserts that no sampled PMID appears anywhere in the workbook and that no hidden sheet exists.
- **Codebook source.** The codebook text is read programmatically, using `ast` on the source file, from `classify_themes_batch.py` and `prefilter_batch.py` at commit `9c79cd5`. The commit hash and the SHA-256 of the full prompt are printed on each "Read me first" sheet.

## A1 · Theme validation (D2a)

Frame: critical records dated 2021–2025 with a theme label. Title-only records are included.

| Year | Frame | Title-only in frame | Sample | Sampling fraction |
|---|---|---|---|---|
| 2021 | 270 | 25 | 40 | 14.8% |
| 2022 | 333 | 48 | 40 | 12.0% |
| 2023 | 624 | 80 | 40 | 6.4% |
| 2024 | 1,228 | 151 | 40 | 3.3% |
| 2025 | 1,828 | 71 | 40 | 2.2% |
| Total | 4,283 | 375 | 200 | 4.7% |

21 of the 200 sampled records are title-only.

## A2 · Full-abstract prefilter re-run (D1, X2)

Full output: [outputs/A2/A2_summary.md](outputs/A2/A2_summary.md). Labels: `outputs/A2/a2_fullabstract_labels.csv`. Raw responses: `outputs/A2/raw_round{1,2}.jsonl.gz`.

- **Script.** A copy of `prefilter_batch.py`; the diff is in `outputs/A2/a2_diff_vs_prefilter_batch.patch`.
  - The model, `max_tokens` (120), unset temperature and Batch API are unchanged.
  - `SYSTEM_PROMPT` SHA-256 is asserted identical to the original at every run (`3fdfbbad…`).
  - The input is the title plus the full abstract.
  - Failures are recorded as `FAILED`. A `paper_type` outside the vocabulary is also treated as a failure rather than forced to `application`.
- **Cost.** Projected USD **44.09**, from an exact `count_tokens` run on 1,000 records (mean 705 input tokens) with 40 output tokens per request assumed. Actual cost USD **40.35** (68.9 M input and 2.36 M output tokens, at Batch pricing).
- **FAILED.** Round 1 had 10 batch-level errors. All 10 succeeded on the single resubmission, so the final count is **0**.
- **Production × full-abstract labels**, all 97,492 records:

| Production \ full-abstract | discourse | evaluative | application | Total |
|---|---|---|---|---|
| application | 1,282 | 1,568 | 77,883 | 80,733 |
| discourse | 7,724 | 198 | 977 | 8,899 |
| evaluative | 128 | 6,868 | 864 | 7,860 |
| Total | 9,134 | 8,634 | 79,724 | 97,492 |

- **Flips:**
  - application → discourse or evaluative: **2,850** of 80,733 (3.5%);
  - retained → application: **1,841** of 16,759 (11.0%);
  - discourse ↔ evaluative swaps: 326.
- **By year**, as application → KEEP / retained → application / full-abstract keep rate:

| Year | application → KEEP | retained → application | Full-abstract keep rate |
|---|---|---|---|
| 2021 | 2.7% | 16.0% | 10.5% |
| 2022 | 2.8% | 15.0% | 11.2% |
| 2023 | 3.3% | 13.0% | 15.5% |
| 2024 | 3.5% | 9.6% | 20.1% |
| 2025 | 3.9% | 10.1% | 21.5% |
| Jan–Apr 2026 | 4.9% | 9.4% | 26.3% |

  Full per-year cross-tab: `outputs/A2/A2_crosstab_by_year.csv`.

## A3 · Prefilter-audit workbook (D1, X2)

- **Total rows:** 370 (EX-F 75, EX-S 225, RET 50, PILOT 20), shuffled together.
- **Exclusions:** the 200 pilot PMIDs were excluded from EX-F, EX-S and RET. No record was FAILED, so none were excluded for that reason.
- **No stratum-year fell below its target.**

| Year | EX-F frame (sampled) | EX-S frame (sampled) | RET frame (sampled) |
|---|---|---|---|
| 2021 | 275 (15) | 9,839 (45) | 1,061 (10) |
| 2022 | 330 (15) | 11,435 (45) | 1,342 (10) |
| 2023 | 401 (15) | 11,647 (45) | 2,051 (10) |
| 2024 | 551 (15) | 15,081 (45) | 3,698 (10) |
| 2025 | 892 (15) | 22,036 (45) | 5,885 (10) |

- **PILOT:** 20 of the 200 pilot records.

## A4 · Scoring scripts (D1, X2, D2a)

| Script | Synthetic test output |
|---|---|
| `revision_r1/scripts/a4_score_theme.py` | `coding/_synthetic_test/theme_scores_SYNTHETIC/` |
| `revision_r1/scripts/a4_score_prefilter.py` | `coding/_synthetic_test/prefilter_scores_SYNTHETIC/` |

- Both ran end to end on synthetic copies of the **real** templates. The copies were randomly filled by `a4_make_synthetic.py` and are labelled SYNTHETIC.
- Every estimand listed in protocol §6 is produced:
  - weighted and unweighted metrics with bootstrap CIs;
  - year bands;
  - the three borderline variants;
  - the logistic year tests;
  - the population-weighted 2×2 tables;
  - intra-rater agreement.
- **Neither script has been run on real labels.**

## Deviations from classifier text

- **None substantive.** Each "Read me first" sheet reproduces the classifier prompt verbatim, from its first line to its last rule. The only omissions are the machine output-format lines: `Return ONLY valid JSON …`, and for the prefilter also `No preamble, no explanation.`
- **Procedural additions:**
  - the theme sheet's "use `other` only when no listed theme fits" restates the classifier's own `other` definition;
  - the prefilter sheet's `borderline` flag records uncertainty and adds no decision rule.

## Other decisions to flag

1. **Out-of-vocabulary `paper_type`.** The original code forces this to `application`. In A2 it was recorded as `FAILED`, because the brief says never to default to `application`. In practice no such case occurred: all 10 round-1 failures were batch errors.
2. **Estimate scope.** Estimates refer to the frame population, which excludes the 200 pilot PMIDs. Because FAILED = 0, there is no FAILED exclusion.

## Checks

- **Checksums.** `output/` in the worktree (189 files) and in the main checkout (174 files) match the Batch 1 pre-run manifests. The post-Batch-2a manifests are in `outputs/checksums/*_post_batch2a.sha256`.
- **Repository.** No tracked file outside `revision_r1/` was modified.
- **Push.** Nothing has been pushed.

## Commits (Batch 2a)

| Commit | Contents |
|---|---|
| `0d21f6c` | A0 freeze 1 (protocol, scripts, A1 sample, key, manifest and template) |
| `4ea79e5` | A4 scorers, synthetic theme test, A2 token count and submission record |
| `2d1ae78` | A2 labels, raw responses, summary |
| `47cf6fe` | A0 freeze 2 (A3 sample, key, manifest and template) |
| (final) | Synthetic prefilter test, post-run checksums, this report |
