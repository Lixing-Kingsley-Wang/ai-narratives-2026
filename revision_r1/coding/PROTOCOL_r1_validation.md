# Protocol: R1 human-coding validation (theme classifier; prefilter audit)

JMIR #109710, major revision R1, Batch 2a. Addresses D2a (theme classifier) and D1/X2 (prefilter validation and false-negative audit).

This protocol is frozen by git commit **before** either coding workbook is released to the coder. Any later change is logged in §7 with the date and the reason.

**Two-stage freeze.** The A3 frames depend on the A2 re-run, which does not exist yet at the first freeze.

- **Freeze 1** commits this protocol together with:
  - all three sampling or labelling scripts (`a1_theme_sample.py`, `a2_prefilter_fullabstract_batch.py`, `a3_prefilter_sample.py`);
  - the A1 manifest, key and template.
- **Freeze 2** commits the A3 manifest and key after A2 finishes. They are produced by the A3 script exactly as frozen in Freeze 1, with no edits. Freeze 2 happens before the A3 workbook is released.

---

## 1. Coder and blinding (both instruments)

- **Coder.** One author (L.W.), who also coded the original validation samples.
- **What the workbook shows.** Only `row_id`, `title` and `abstract` (the full text). An empty abstract is shown as `[No abstract available. Code from the title.]`.
- **Where everything else lives.** PMID, year, journal, stance, model labels and stratum are only in a separate key CSV. Nothing of this appears in the workbook, not even in a hidden sheet. Each build script checks this: two visible sheets only, and no sampled PMID anywhere in the workbook text.
- **Row order.** Rows are shuffled across years and strata.
- **Instructions.** The coder must not open the key files, must not look papers up, and must code each paper independently.

## 2. Codebooks

- **Verbatim text.** Each codebook is the classifier's own `SYSTEM_PROMPT`, extracted programmatically. The build script parses the source file with `ast` (no retyping), then records the file path, the commit hash and the SHA-256 of the full prompt on the "Read me first" sheet.
  - Themes: `classify_themes_batch.py` @ `9c79cd5d0f5b0b3a364866ec57f9edf0f17998b2`, prompt SHA-256 `b1bf54eddab15ab05418d5a2eb52de425047d87998bed1dd34abc837448f9584`. The text shown runs from the first line through the `other` definition.
  - Prefilter: `prefilter_batch.py` @ `9c79cd5d0f5b0b3a364866ec57f9edf0f17998b2`, prompt SHA-256 `3fdfbbadbd5aeac5b49cb22ae53f4b51e96cb41c1c4f566eccf65dc7bd2071f4`. The text shown runs from the first line through the last CRITICAL RULE, including "When in doubt, classify as application."
- **Omitted.** Only each prompt's machine-format line (`Return ONLY valid JSON …` and, for the prefilter, `No preamble, no explanation.`).
- **Added.** Procedural instructions only (how to fill the sheet) and one transparency line about the classifier's truncated input.

## 3. A1: theme validation (D2a)

- **Frame.** Critical records (stance Alarm or Caution) dated 2021–2025 that carry a theme label in `output/analysis/thematic_alarm.csv`. Title-only records are included.

  | Year | Frame | Title-only |
  |---|---|---|
  | 2021 | 270 | 25 |
  | 2022 | 333 | 48 |
  | 2023 | 624 | 80 |
  | 2024 | 1,228 | 151 |
  | 2025 | 1,828 | 71 |
  | Total | 4,283 | 375 |

- **Sample.** 40 per year by simple random sampling within year, 200 in total.
  - Implementation: `numpy.random.default_rng(42)`. For each year in ascending order, sort the frame by integer PMID and draw `rng.choice(n, 40, replace=False)`.
  - Rows are then permuted with `rng.permutation(200)` and numbered `row_id` 1–200.
  - Sampling fractions are in `theme_sampling_manifest.csv`.
- **Coder input.**
  - One column per theme, in prompt order: replacement, hallucination, safety_clinical, ethics_bias, cognitive, education, regulation, existential, data_privacy, other.
  - Each cell takes `1` or blank. `n_themes` counts the ticks and turns red unless it is 1–3.
  - There is also a free-text `notes` column.
- **Files.**

  | File | Contents |
  |---|---|
  | `theme_validation_TEMPLATE.xlsx` | Workbook given to the coder |
  | `theme_key.csv` | row_id, pmid, year, journal, stance, model_themes, abstract_present |
  | `theme_sampling_manifest.csv` | Frame size, sample size and sampling fraction per year |
  | Completed file | Returned as `theme_validation_COMPLETED.xlsx` |

## 4. A2: full-abstract prefilter re-run (stage 1 of the audit; D1, X2)

- **Population.** All 97,492 eligible post-cutoff Q1/Q2 records (`filtered_medical_all_Q1Q2.csv`): 80,733 production `application` and 16,759 retained.
- **Script.** `a2_prefilter_fullabstract_batch.py`, a copy of `prefilter_batch.py` (diff: `outputs/A2/a2_diff_vs_prefilter_batch.patch`). Classification changes in only two ways:
  1. Title plus the full abstract is sent, with no truncation (title only when the abstract is empty).
  2. Any failure becomes `FAILED`, never `application`. Failures are a non-succeeded result, an empty response, a JSON parse failure, or a `paper_type` outside {discourse, evaluative, application}. FAILED records are resubmitted once.
- **Unchanged.**
  - Model `claude-haiku-4-5-20251001`.
  - `SYSTEM_PROMPT`, byte-identical to the original (SHA-256 asserted at runtime).
  - `max_tokens` 120; temperature not set; Message Batches API.
  - Confidence normalisation.
- **Cost gate.**
  - Before submission, input tokens are counted exactly with `messages.count_tokens` on 1,000 records (Python `random.Random(42).sample` of PMIDs sorted as integers) and extrapolated.
  - Output is assumed to be 40 tokens per request. Pricing is $1/$5 per MTok with the 50% Batch discount.
  - If the projected cost exceeds USD 60, the script refuses to submit.
- **Outputs** (in `outputs/A2/`):
  - raw responses, `raw_round{1,2}.jsonl.gz`;
  - `a2_fullabstract_labels.csv` with columns pmid, year, label_production, label_fullabstract, type_confidence, failed, fail_reason and round.

## 5. A3: prefilter-audit workbook (D1, X2)

**Strata.** Years 2021–2025 only. Year is the first `20xx` in `pub_date`, the same as the production `pub_year`.

| Stratum | Definition | Per year | Total |
|---|---|---|---|
| EX-F | production = application; full-abstract = discourse or evaluative | 15 | 75 |
| EX-S | production = application; full-abstract = application | 45 | 225 |
| RET | production = discourse or evaluative | 10 | 50 |
| PILOT | records from the 200-record prefilter pilot (any year), for intra-rater reliability | — | 20 |

**Rules.**

- Pilot PMIDs are excluded from EX-F, EX-S and RET.
- Records with a full-abstract label of FAILED enter no frame; their count is reported.
- A stratum-year with fewer records than its target is taken in full and reported.

**Sampling.** `numpy.random.default_rng(42)`.

1. For each stratum in the order EX-F, EX-S, RET, and each year from 2021 to 2025, sort the frame by integer PMID and draw `rng.choice(n, min(target, n), replace=False)`.
2. Then draw PILOT: sort the pilot by integer PMID and draw `rng.choice(200, 20, replace=False)`.
3. Shuffle all 370 rows with `rng.permutation(370)` and number them `row_id`.

**Coder input.**

- `human_label`: drop-down of {discourse, evaluative, application}.
- `borderline`: Y or blank. Mark Y when torn, or when the "when in doubt" rule was applied.
- `notes`: free text.

**Files.**

| File | Contents |
|---|---|
| `prefilter_audit_TEMPLATE.xlsx` | Workbook given to the coder |
| `prefilter_key.csv` | row_id, pmid, year, journal, stratum, label_production, label_fullabstract, and pilot_my_label (PILOT rows only) |
| `prefilter_sampling_manifest.csv` | Frame size, target, sample size, sampling fraction and below-target flag for every stratum-year |
| `prefilter_sampling_notes.txt` | FAILED count |

## 6. Estimands and analysis plan (A4 scripts)

**Common rules.**

- KEEP means discourse or evaluative.
- Bootstrap: 1000 resamples, seed 42, percentile 95% CIs, resampling coded records **within design cells** (year for A1; stratum × year for A3).
- **Weights** for a record in cell c: w = N_c / n_c, where N_c is the frame size and n_c the number of coded records in that cell.
- **Unusable rows.** A row with no human label (A3), or with zero ticked themes (A1), is excluded and counted. Rows with more than 3 ticked themes are kept as coded and counted.
- No real labels are scored until coding is complete. Both scripts are tested only on synthetic, randomly filled copies of the templates.

### 6.1 Theme classifier (`a4_score_theme.py`)

Model themes come from `theme_key.csv`; human themes are the ticks in the completed workbook. Comparisons are set-based, per record.

1. **Per theme**, for each of the 10 themes: TP = in both sets, FP = model only, FN = human only. Report precision = TP/(TP+FP), recall = TP/(TP+FN), F1, and support (number of human-positive records). A theme with fewer than 10 human-positive records (unweighted) is flagged "insufficient support".
2. **Overall:**
   - micro-F1 = 2ΣTP / (2ΣTP + ΣFP + ΣFN);
   - macro-F1 = mean of the per-theme F1 over themes where F1 is defined;
   - exact-match ratio (model set = human set);
   - Hamming loss = mean over records of |symmetric difference| / 10;
   - mean Jaccard = mean of |∩| / |∪|.
3. Every metric is reported **unweighted** and **weighted to the frame**, where weighted counts are Σw over records. Each gets a bootstrap CI.
4. Repeated by year band: 2021–2022, 2023, and 2024–2025.
5. The distribution of the number of themes per record, human vs model, unweighted and weighted.

### 6.2 Prefilter (`a4_score_prefilter.py`)

Let p_sy be the human KEEP proportion among coded records in stratum s, year y, and N_sy the frame size.

1. **False negatives among excluded records.**
   - Estimated missed AI-engaged records in year y: M_y = N_EX-F,y × p_EX-F,y + N_EX-S,y × p_EX-S,y.
   - Rate per year: 1 − NPV_y = M_y / (N_EX-F,y + N_EX-S,y).
   - Pooled over 2021–2025, and compared between 2021–2022 and 2024–2025 (difference with bootstrap CI).
   - Logistic test of year (continuous, centred) on human KEEP within EX-F ∪ EX-S. Primary: unweighted, with stratum as a covariate, Wald 95% CI and P. Secondary: design-weighted, with a bootstrap CI for the OR.
2. **Estimated number of missed AI-engaged records:** M_y by year and in total (ΣM_y), with bootstrap CIs.
3. **PPV among retained records:** p_RET,y by year; pooled with weights N_RET,y.
4. **Population-weighted 2×2 for the production prefilter.**
   - TP = Σ_y N_RET,y × p_RET,y; FP = Σ_y N_RET,y × (1 − p_RET,y); FN = Σ_y M_y; TN = Σ_y (N_EX,y − M_y).
   - Report sensitivity, specificity, PPV, NPV, Cohen κ and Gwet AC1 on these weighted counts, each with a bootstrap CI.
   - Secondary: the same weighted 2×2 for the full-abstract classifier, with each record classified by its own full-abstract label.
5. **Precision of the full-abstract re-run:** the human KEEP rate within EX-F, by year and pooled with weights N_EX-F,y.
6. **Intra-rater agreement:** on the 20 PILOT rows, % agreement and Cohen κ against the original pilot `my_label`, for 3 classes and for KEEP/DROP.
7. **Sensitivity analyses:** rerun items 1–5 twice, once with borderline = Y treated as application and once with borderline = Y treated as KEEP.
8. **3-class confusion:** human label against the production label, and human label against the full-abstract label, for the coded sample. Both are shown unweighted and weighted.

**Scope of extrapolation.** Frames exclude FAILED records and the 200 pilot PMIDs. Estimates therefore refer to the frame population; the excluded counts are reported alongside.

## 7. Deviations from classifier text

- **None substantive.** The workbooks reproduce the classifier prompt text verbatim. The only omissions are the machine output-format lines listed in §2.
- **Procedural additions.** Both are procedural and add no decision rule beyond the classifier text:
  - the theme sheet's "use `other` only when no listed theme fits" restates the classifier's own `other` definition ("critical concern not fitting above");
  - the prefilter sheet's `borderline` flag records uncertainty and does not change the label.

## 8. Change log

- 2026-10-23: Freeze 1.
- 2026-10-23: Freeze 2 — A3 manifest, key and template generated by the Freeze-1 `a3_prefilter_sample.py` (unchanged) after A2 finalize; no stratum-year below target; 0 FAILED records.
