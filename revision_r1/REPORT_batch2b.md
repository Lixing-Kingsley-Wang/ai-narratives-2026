# JMIR #109710 — R1 Batch 2b report (analyses; no human coding)

Branch `jmir-r1-major-revision`. Nothing was pushed. Numbers only.

**Environment**
- `revision_r1/.venv`: Python 3.12.3, statsmodels 0.15.0, pinned in `requirements_r1.txt`. Excluded locally from git.
- The project venv was not modified. It was used read-only for one helper (`b4_prep_country.py`, which needs geopandas).

## B0 · Pre-specification

- **Plan:** [ANALYSIS_PLAN_batch2b.md](ANALYSIS_PLAN_batch2b.md), committed as **`f6f8c6d`** (2026-10-28 14:27). It includes the verbatim B3 prompt and the B6 lexicons.
- **Timing check:** all later commits come after it. The first B2/B3 token count and the first B4–B6 computation came after `f6f8c6d`.
- **B1 timing:** B1 was implemented earlier, as Amendment 3 (`c146e1b`), before the plan. In this batch it was only re-run into `outputs/B1/`.

## ⚠ Finding before analysis: the published stance prompt is not the one that produced the data

**The mismatch**
- **Prompt that produced the labels:** every reported stance label comes from the **v1** prompt (SHA-256 `b3949917…`). That prompt is identical in three places:
  - `classify_stance.py`;
  - `9c79cd5:classify_stance_batch.py`, the production batch run;
  - `classify_stance_batch.py.v1_backup`.
- **Prompt that was published:** Supplementary Note 2 prints the **v2** prompt, which is the current `classify_stance_batch.py`, used only in the v2 sensitivity analysis.
- **Methods text:** the Methods definition "Advocacy required both transformative language … and minimal or no acknowledged caveats" paraphrases v2.
- **v1's actual Advocacy definition:** "Advocacy: strongly pro-AI. Emphasises transformative potential, minimal caveats."

**Effect on this batch**
- B2 used v1 exactly, as production did.
- B3 ran as specified.
- This changes no number. It changes the text of Supplementary Note 2 and the Methods, and the premise of X1. It is listed in B7 §8.

## B1 · Prefilter CIs with zero-event cells (D1, X2)

Output: [outputs/B1/prefilter_exact_ci.md](outputs/B1/prefilter_exact_ci.md); old-vs-new comparison: `outputs/B1/B1_old_vs_new_ci.csv`.

**Method**
- Each stratum-year cell is drawn from Jeffreys Beta(x+½, n−x+½): 10,000 draws, seed 42, propagated through the design weights.
- Single cells also get exact Clopper–Pearson intervals.

**Results**
- **Point estimates are unchanged.**
- **Selected primary estimates**, new (Jeffreys) CI vs old (bootstrap) CI:

  | Estimate | Value | Jeffreys CI | Bootstrap CI |
  |---|---|---|---|
  | 1 − NPV, pooled | 5.2% | 4.1–8.9 | 3.2–7.4 |
  | Missed records | 3,747 | 2,946–6,447 | 2,332–5,398 |
  | Production sensitivity | 78.5% | 66.8–81.7 | 71.7–85.6 |
  | Production κ | 0.842 | 0.713–0.856 | 0.782–0.897 |

- **Width:** 25 of 29 primary estimands get wider intervals. The 4 that get narrower are all full-abstract quantities.
- **Full-abstract 2×2:** the Jeffreys interval excludes the point estimate for full-abstract specificity and PPV, because the sub-cells have n = 1–3. The bootstrap interval is kept for that table.
- **Protocol:** the Amendment 3 change-log entry states the timing (after the results were seen), that it changes only the CIs, and these width facts.

## B2 · Stance on recovered records; augmented-corpus trends (D1, X2)

Output: [outputs/B2/B2_analysis.md](outputs/B2/B2_analysis.md)

**Run details**
- **Prompt:** SHA-256 `b3949917159ea546ce7eb4c21224659be98c646aa937287d376f68c67992a39f`, asserted equal to production.
- **Settings:** `claude-sonnet-4-6`, Batch API, temperature not set, `max_tokens` 120.
- **Cost:** projected USD 4.81; actual **USD 4.47**.
- **FAILED:** 3 in round 1, still 3 after one resubmission.

**Recovered vs retained records**, 2021–2025:

| Set | n | Critical | Cautious Optimism | Advocacy |
|---|---|---|---|---|
| Recovered | 2,453 | 12.6% (310/2,453) | 81.1% | 1.1% (27) |
| Retained | 14,058 | 30.5% (4,283/14,058) | 62.9% | 1.6% (218) |

**Trend estimates by corpus**, 2021→2025:

| Corpus | Critical: change | Critical: OR per year | Advocacy: change | Advocacy: OR per year |
|---|---|---|---|---|
| (a) Production | 25.4 → 31.0% | 1.077 (1.046–1.108) | 2.92 → 1.12% | 0.793 (0.721–0.872) |
| (b) Augmented | 22.0 → 28.6% | 1.092 (1.063–1.122) | 2.46 → 1.19% | 0.840 (0.767–0.920) |
| (c) Precision-weighted | 22.7 → 28.7% | 1.082 (1.053–1.111) | 2.57 → 1.19% | 0.832 (0.759–0.911) |
| (d) Full-abstract | 24.0 → 30.7% | 1.089 (1.059–1.120) | 2.65 → 1.03% | 0.799 (0.725–0.880) |

- **Corpus (d)** drops the 1,841 records that production retained but the full-abstract re-run labelled `application`; 1,587 of them fall in 2021–2025.
- **Spearman, Advocacy:** ρ = −1.00 (P=.017) in (a), and −0.90 (P=.083) in (b)–(d).

## B3 · Symmetric endorsement re-classification (X1, D2b)

Output: [outputs/B3/B3_analysis.md](outputs/B3/B3_analysis.md)

**Run details**
- **Prompt:** SHA-256 `27d28077cd7485fddcdfe4f0da3f4a3c13ad36a310bcd23f1544a5a89db50cf6`, verbatim from the brief.
- **Settings:** `claude-sonnet-4-6`, Batch API, temperature 0, `max_tokens` 30.
- **Cost:** projected USD 12.01; actual **USD 11.88**.
- **B2 + B3 total:** USD 16.35.
- **Flags:** of 10,749 favourable records, 1,356 were flagged yes, 9,386 no, and **7 FAILED**.

**Why the 7 failed and were not resubmitted**
- In all 7, the model wrote prose before the JSON, and `max_tokens` 30 ran out first.
- The resubmission was refused with HTTP 400, "credit balance is too low".
- The 7 stay FAILED. They remain in the denominators and are not counted as yes. An upper bound that counts them as yes is reported; it changes the 2021 value by 0.09 pp at most.

**Strong endorsement trend**, 2021–2025, with all records as the denominator:

| Year | Share |
|---|---|
| 2021 | 10.8% (115/1,063) |
| 2022 | 13.2% (177/1,343) |
| 2023 | 9.8% (202/2,054) |
| 2024 | 8.0% (295/3,700) |
| 2025 | 6.6% (390/5,898) |

- **Trend statistics:** Spearman ρ −0.90 (exact P=.083); OR per year 0.834 (0.798–0.871), P<.001.
- **Advocacy, same records:** 2.9% → 1.1%; OR 0.793 (0.721–0.872).

**Consistency checks**
- **Production Advocacy flagged yes:** **91/235 = 38.7%** (32.5–45.3). The brief expected this to be near 100%; it is reported as observed.
- **Production Cautious Optimism flagged yes:** 1,265/10,514 = 12.0% (11.4–12.7).

**Agreement with human Advocacy labels** (130 model-favourable validation records)
- 2×2 table: TP 10, FN 14, FP 8, TN 98.
- Sensitivity 10/24 = 0.417 (0.211–0.633); PPV 10/18 = 0.556 (0.316–0.800); κ 0.378 (0.146–0.598).
- Human labels of the records flagged yes: Advocacy 10, Cautious Optimism 8.

**Corrected human-Advocacy prevalence** (secondary): 6.99% (2021) → 5.52% (2025). Two strata have fewer than 10 validation records: Cautious Optimism × flag yes (n=5) and Cautious Optimism × flag FAILED (n=0).

## B4 · Multivariable regression (D4a, X3, D3)

Output: [outputs/B4/B4_regression.md](outputs/B4/B4_regression.md)

**Data and references**
- n = 14,058; 4,283 critical events; **2,278 journal clusters**.
- Reference levels (most frequent): discourse; Research Article; Medical Informatics / Digital Health; North America.
- Excluded covariates: model type and FDA count, as stated in the output.

**Primary model (critical)**

| Term | Adjusted OR (95% CI) | P | Unadjusted OR |
|---|---|---|---|
| Year (per year) | **1.103 (1.066–1.141)** | <.001 | 1.08 |
| Evaluative genre | 0.54 (0.48–0.61) | | |
| Review | 0.47 (0.41–0.54) | | |
| East Asia | 0.44 (0.38–0.51) | | |
| Cardiology | 0.28 (0.21–0.36) | | |
| Mental Health | 1.22 (0.94–1.60) | .140 | |

**Average marginal predicted probability of critical stance**

| Group | Probability (95% CI) |
|---|---|
| 2021 | 25.3% (23.2–27.4) |
| 2025 | 32.6% (31.2–33.9) |
| Mental Health | 46.7% |
| Cardiology | 17.6% |
| East Asia | 19.3% |
| North America | 33.9% |
| Review | 21.5% |
| Research Article | 35.4% |

**Ordinal model**
- Year OR 0.94 (0.92–0.97), where OR < 1 means a shift toward the critical end.
- **The proportional-odds check fails for 27 of 32 terms** under the pre-specified rule. The failures are mostly at the "> Cautious Optimism", i.e. Advocacy, cut point.

**Advocacy model**
- 218 events. Year OR **0.841 (0.754–0.939)**, P=.002.
- Sparse levels were collapsed: 9 specialties, 2 regions and Commentary.

**Sensitivity models**

| Model | Year effect |
|---|---|
| S1: categorical year (vs 2021) | 2022: 1.00; 2023: 1.31; 2024: 1.53; 2025: 1.45 |
| S2: + Jan–Apr 2026 | 2026: 1.61 (1.35–1.92) |
| S3: journal fixed effects (275 journals, 8,529 records) | OR 1.082 (1.030–1.137) |
| S4: country in place of region | OR 1.110 |

- **Adjusted United States vs China (S4):** OR **2.81 (2.26–3.48)**, P<.001.

## B5 · SJR medical-category sensitivity (D6)

Output: [outputs/B5/B5_sjr_sensitivity.md](outputs/B5/B5_sjr_sensitivity.md)

**Records removed** (2021–Apr 2026):

| Definition | Removed |
|---|---|
| D1 | 2,781 |
| D2 | 4,607 |
| D3 | 1,546 |

The by-year breakdown is in the output.

**Trend robustness under D1**
- Critical: OR 1.066 (1.034–1.100), ρ +0.70 (P=.233).
- Advocacy: OR 0.771 (0.690–0.862).
- The theme directions are unchanged.
- FDA ρ −0.63 (P=.005).
- East Asia 18.7% vs North America 35.2%.
- Reviews 25.7%.

## B6 · MeSH and keyword triangulation (D5)

Output: [outputs/B6/B6_terms.md](outputs/B6/B6_terms.md); figure: `figures/B6_terms_r1_draft.png|pdf`.

**Re-fetch**
- NCBI returned 16,756 of 16,759 records.
- **TLS issue:** the first attempt failed because this Python build lacks a CA bundle. The fetch was re-run through the system `curl` with TLS verification on.
- **Storage:** raw XML is kept locally (81 MB) with a committed SHA-256 manifest.

**Completeness**
- At least one MeSH descriptor: 77.5%, falling from 88.5% (2021) to 74.0% (2025).
- At least one author keyword: 77.0%, rising from 68.4% to 81.6%.

**Lexicon vs LLM theme trend direction**, critical records 2021–2025:

| Theme | Lexicon trend | Lexicon OR | LLM OR | Same direction? |
|---|---|---|---|---|
| Errors | 8.1 → 22.6% | 1.384 | 1.367 | yes |
| Safety | 13.7 → 19.2% | 1.133 | 1.055 | yes |
| Regulation | 24.8 → 29.9% | 1.128 | 0.765 | **no** |
| Ethics | 44.1 → 44.8% | 1.008 | 0.915 | **no** |

**Emerging terms** (2024–25 vs 2021–22)
- Rising: "large language models" z 12.1, "chatgpt" z 11.3.
- Falling: "machine learning" z −17.8, "deep learning" z −16.5.

**Terms separating stance**
- Critical side: "delivery of health care" z 16.2, "ethics" 14.1, "bias" 12.8.
- Favourable side: "deep learning" z −17.0.

## B7 · Numeric corrections (E13, D8)

[outputs/B7_corrections.md](outputs/B7_corrections.md) covers:
- Table S1 exact P (both windows);
- Table S3 with deterministic seeds (both windows);
- region n's;
- Commentary 53.8%;
- Q1/Q2 88.1%;
- fabrication-involved share by year, with exact CIs (2021: 0/56, 0.0–6.4%);
- κ_max 0.755 and AC1 0.885;
- prefilter κ CI;
- text-only corrections, including the stance-prompt finding.

## Headline numbers

| Headline | Original (2021→Apr 2026) | 2021–2025 | Adjusted (B4) | B2 (corpus a→d) | B3 | B5 (D1 / D2 / D3) |
|---|---|---|---|---|---|---|
| Critical trend | 25.4→32.6%; ρ +0.77 | 25.4→31.0%; ρ +0.80 (P=.133); OR 1.077 (1.046–1.108) | OR 1.103 (1.066–1.141) | OR 1.077–1.092 | critical side unchanged | OR 1.066 / 1.085 / 1.071 |
| Advocacy trend | 2.9→0.6%; ρ −1.00 | 2.9→1.1%; ρ −1.00 (P=.017); OR 0.793 (0.721–0.872) | OR 0.841 (0.754–0.939) | OR 0.793–0.840 | Strong endorsement 10.8→6.6%; OR 0.834 (0.798–0.871) | OR 0.771 / 0.802 / 0.782 |
| Patient safety theme | +11.0 pp | +5.7 pp; OR 1.055 (1.002–1.111) | — | — | — | +7.6 / +8.7 / +6.5 pp |
| Hallucination/errors theme | +30.9 pp | +27.4 pp; OR 1.367 (1.296–1.442) | — | — | — | +27.7 / +25.8 / +28.1 pp |
| Regulation theme | −22.0 pp | −23.1 pp; OR 0.765 (0.727–0.805) | — | — | — | −21.9 / −21.3 / −22.8 pp |
| Ethics & bias theme | −8.1 pp | −3.6 pp; OR 0.915 (0.869–0.963) | — | — | — | −3.8 / −1.5 / −4.6 pp |
| Specialty range | MH 51.3% – Cardiology 16.8% | MH 50.3% – Cardiology 16.1% | AMP MH 46.7% – Cardiology 17.6%; OR 0.28 vs MI | — | — | MH 50.8% – Card. 17.1% / 50.8–16.9 / 51.3–17.0 |
| US vs China | 34.5% vs 16.2% | 34.2% vs 14.9% | OR 2.81 (2.26–3.48) | — | — | not computed (country) |
| East Asia vs North America | 18.5% vs 35.1% | 17.7% vs 34.9% | OR 0.44 (0.38–0.51); AMP 19.3% vs 33.9% | — | — | 18.7 vs 35.2 / 19.5 vs 35.2 / 19.0 vs 35.3 |
| Reviews (critical / favourable) | 24.9% / 73.1% | 24.3% / 73.6% | OR 0.47 (0.41–0.54); AMP 21.5% vs RA 35.4% | — | — | 25.7 / 26.6 / 25.3 (critical) |
| FDA ρ | −0.65 (P=.004) | −0.61 (P=.007) | not modelled (ecological) | — | — | −0.63 / −0.59 / −0.65 |

## New discrepancies (Batch 2b)

1. **Stance prompt mismatch.** Supplementary Note 2 and the Methods' Advocacy definition describe v2, not the v1 prompt that produced every stance label (see above).
2. **B3 consistency.** Only 38.7% of production Advocacy records meet the B3 "strong endorsement" construct.
3. **B3 incomplete.** Seven B3 records stayed FAILED because the resubmission was refused for API credit. Resubmitting them would cost under USD 0.01 once credit is added.
4. **B2 FAILED.** Three B2 records stayed FAILED after one resubmission.
5. **Proportional odds** fails for most covariates (27/32 terms), mainly at the Advocacy cut point.
6. **Lexicon directions.** For regulation and ethics/bias, the lexicon trend direction disagrees with the LLM theme trend.
7. **Stray file.** `revision_r1/outputs/poll_round1.log` (untracked) is the error log of a first polling attempt that failed because of a shell word-splitting bug. It is left in place and not committed.

## Checks

- **Checksums.** `output/` in the worktree (189 files) and in the main checkout (174 files) match the pre-run manifests. Post-run manifests: `outputs/checksums/*_post_batch2b.sha256`.
- **Repository.** No tracked file outside `revision_r1/` was modified.
- **API.** API calls were made only in B2 and B3. The key was read from the main checkout's `.env` and never printed or written.
- **NCBI.** The `email` parameter was passed to NCBI through stdin, so it never appeared in command arguments.
- **Push.** Nothing has been pushed.

## Commits (Batch 2b)

| Commit | Contents |
|---|---|
| `f6f8c6d` | B0 plan |
| `3fdfadb` | B2/B3 scripts and submission; B1 re-run |
| `e682743` | B4 |
| `62a812a` | B5 |
| `0f5443f` | B6 |
| `1dd03e5` | B7; B2 batch results |
| `f5d33f0` | B2 analysis |
| `b3e3d16` | B3 |
| (final) | Report, protocol note, checksums |
