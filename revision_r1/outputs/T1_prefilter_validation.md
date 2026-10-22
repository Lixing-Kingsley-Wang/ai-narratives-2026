# T1 · Prefilter validation metrics (D1, X2)

Script: `revision_r1/scripts/t1_prefilter_validation.py`. Inputs are the committed pilot files (`output/pilot_200_full_haiku.csv`, `output/pilot_200.xlsx`; byte-identical to the last committed versions at `31ed027^`) and the production prefilter outputs.

## 1. Pilot provenance

| Question | Finding | Evidence |
|---|---|---|
| Same model? | Probably yes, not verifiable. The only pilot path in the code is `prefilter.py pilot` (model `claude-haiku-4-5-20251001`, same constant as `prefilter_batch.py`), but the script that wrote the pilot Haiku labels is not in the repository (row below). | `prefilter.py:19,106-112`; `prefilter_batch.py:34` |
| Same prompt? | Yes: `SYSTEM_PROMPT` and `build_prompt` are byte-identical in `prefilter.py` and `prefilter_batch.py`. | diff of the two blocks = identical |
| Same truncation (title + first 300 chars)? | Yes in code (`abstract[:300]` in both files). | `prefilter.py:51`; `prefilter_batch.py:71` |
| Same API path? | Pilot: unknown (the only pilot path in code is synchronous `prefilter.py`). Production was **mixed**, not Batch-only as Methods states: the first 2,500 records were run synchronously (`prefilter.py`, 3 retries) and the remaining 94,992 through one Message Batch. | `output/prefilter.log`; `output/prefilter_batch_submit.log` |
| Script that wrote `pilot_200_full_haiku.csv` | **Not found** in any branch. `prefilter.py pilot` writes `pilot_prefiltered_*.csv`, not a `haiku_label` column. The merge step is undocumented. | `git grep haiku_label` over all refs: no hit |
| Pilot labels vs production labels for the same PMIDs | 200/200 pilot PMIDs are in the production corpus; pilot Haiku label = production Haiku label for 197/200 (two independent T=1.0 inferences). Title and abstract text identical to the corpus for 200/200. | table below |
| Human coder blind to model labels? | Consistent with blinding but **not provable from files**. The coding workbook `pilot_200.xlsx` has columns ['my_label', 'pmid', 'year', 'pub_date', 'title', 'abstract', 'journal', 'first_author', 'doi', 'sjr_quartile', 'journal_abbr', 'pub_type', 'first_affiliation'] (no model label). Model labels were generated in steps (50 → 100 → 200, file times 11:27, 11:55, 13:57 on 2026-05-09). Human labels did not change between those steps: 2/50 and 10/100 changed vs the final file; 0/200 differ between the xlsx and the final csv. Model labels changed in 0/50 and 0/100. | file comparison |
| Sampling | **Undocumented.** The committed `make_pilot.py` would draw 50 per year from 2021–2024 only (unseeded `random.sample`), but the committed pilot has 2021–2026 records in proportions close to the corpus year mix (χ² goodness of fit vs corpus mix, df=5: χ²=2.57, P=0.77). So `make_pilot.py` did not produce this file as committed. The distribution is consistent with a simple random sample of the 97,492, but no code or seed confirms it. | `make_pilot.py:16-19`; table below |

Publication-year distribution of the 200 pilot records (`year` field):

| Year | n |
|---|---|
| 2021 | 16 |
| 2022 | 29 |
| 2023 | 29 |
| 2024 | 42 |
| 2025 | 60 |
| 2026 | 24 |

Pilot year mix vs corpus year mix (expected n under simple random sampling of 200):

| year | pilot_n | expected_n_if_SRS | corpus_n |
|---|---|---|---|
| 2021 | 16 | 23.0 | 11191 |
| 2022 | 29 | 27.0 | 13136 |
| 2023 | 29 | 29.0 | 14128 |
| 2024 | 42 | 39.8 | 19372 |
| 2025 | 60 | 59.3 | 28873 |
| 2026 | 24 | 22.1 | 10757 |

Pilot Haiku label (rows) vs production Haiku label (columns), same PMIDs:

| pilot label | application | discourse | evaluative |
|---|---|---|---|
| application | 168 | 0 | 2 |
| discourse | 1 | 18 | 0 |
| evaluative | 0 | 0 | 11 |

**Implication for NPV (rule 4):** the sampling design is not documented. If the pilot was a simple random sample of the 97,492 eligible records (consistent with its year mix, unconfirmed), NPV can be applied to the excluded records; with n=170 model-DROP records the estimate is imprecise. This must be stated as an assumption, not a design property.

## 2. 3×3 confusion matrix (human rows, model columns), n=200

|  | model:discourse | model:evaluative | model:application | row_total |
|---|---|---|---|---|
| human:discourse | 14 | 1 | 7 | 22 |
| human:evaluative | 0 | 5 | 11 | 16 |
| human:application | 5 | 5 | 152 | 162 |
| col_total | 19 | 11 | 170 | 200 |

- Raw agreement 171/200 = 85.5%. Cohen κ (3-class, unweighted) = 0.511 (95% CI 0.345–0.646). Manuscript: 85.5%, κ 0.51 (0.35–0.68). Raw agreement and point κ reproduce; the CI does **not** (the code that produced 0.347–0.676 is not in any branch, so the bootstrap scheme cannot be checked). → discrepancy list.
- Per-class recall (human class correctly labelled by model): discourse 14/22 = 63.6%, evaluative 5/16 = 31.2%, application 152/162 = 93.8%

## 3. Binary KEEP (discourse + evaluative) vs DROP (application)

|  | model:KEEP | model:DROP | row_total |
|---|---|---|---|
| human:KEEP | 20 | 18 | 38 |
| human:DROP | 10 | 152 | 162 |
| col_total | 30 | 170 | 200 |

Percentile bootstrap 95% CI, 1000 resamples of the 200 records, seed 42. Positive class = KEEP.

| metric | n/N | point | ci_lo | ci_hi | n_boot_valid |
|---|---|---|---|---|---|
| sensitivity | 20/38 | 0.526 | 0.370 | 0.676 | 1000 |
| specificity | 152/162 | 0.938 | 0.898 | 0.970 | 1000 |
| PPV | 20/30 | 0.667 | 0.480 | 0.824 | 1000 |
| NPV | 152/170 | 0.894 | 0.848 | 0.937 | 1000 |
| F1 |  | 0.588 | 0.436 | 0.708 | 1000 |
| accuracy | 172/200 | 0.860 | 0.815 | 0.905 | 1000 |
| kappa |  | 0.505 | 0.331 | 0.646 | 1000 |
| AC1 |  | 0.805 | 0.728 | 0.871 | 1000 |
| PABAK |  | 0.720 | 0.630 | 0.810 | 1000 |
| prevalence_human | 38/200 | 0.190 | 0.135 | 0.240 | 1000 |

Descriptive, by pilot year (small n; no CIs):

| year | n | human_KEEP | model_KEEP | TP | FN | FP | TN | sensitivity | specificity |
|---|---|---|---|---|---|---|---|---|---|
| 2021 | 16 | 5 | 3 | 2 | 3 | 1 | 10 | 0.400 | 0.909 |
| 2022 | 29 | 1 | 2 | 1 | 0 | 1 | 27 | 1.000 | 0.964 |
| 2023 | 29 | 7 | 3 | 2 | 5 | 1 | 21 | 0.286 | 0.955 |
| 2024 | 42 | 7 | 6 | 4 | 3 | 2 | 33 | 0.571 | 0.943 |
| 2025 | 60 | 14 | 14 | 9 | 5 | 5 | 41 | 0.643 | 0.891 |
| 2026 | 24 | 4 | 2 | 2 | 2 | 0 | 20 | 0.500 | 1.000 |

Human-coded KEEP vs **production** label for the same PMIDs (sensitivity of the label actually used in the corpus):

|  | prod:discourse | prod:evaluative | prod:application |
|---|---|---|---|
| human:discourse | 13 | 1 | 8 |
| human:evaluative | 0 | 6 | 10 |
| human:application | 5 | 6 | 151 |

## 4. Silent exclusions (default to `application`)

Rule (Supplementary Note 3): non-succeeded batch result, empty response, or JSON parse failure → `paper_type=application`, `type_confidence=Low`. Raw responses were not stored, so the fallback records **cannot be identified individually** from the committed outputs.

- Synchronous path (`prefilter.py`): 2,500 records; failures after 3 retries also default to application/Low. No per-record error log survives (`output/prefilter.log` shows progress lines only).
- Batch path (`prefilter_batch.py`): 94,992 records submitted in one batch. Final batch status: succeeded=94,983, errored=8. 1 further request(s) are not counted as succeeded or errored in the logged line (canceled/expired are not printed). So **9 batch-level failures** (errored + unaccounted) defaulted to application. Empty-response and parse-failure fallbacks were not logged (`n_err` print line is absent from the logs) and cannot be counted.
- Upper bound by year: every fallback record has `type_confidence=Low`, but the model can also return Low itself. Counts of `application` + `Low` by year:

| pub_year | application_total | application_conf_Low | retained_conf_Low |
|---|---|---|---|
| 2018 | 1 | 0 | 0 |
| 2020 | 32 | 1 | 0 |
| 2021 | 10127 | 87 | 0 |
| 2022 | 11792 | 0 | 0 |
| 2023 | 12073 | 0 | 0 |
| 2024 | 15668 | 2 | 0 |
| 2025 | 22974 | 6 | 0 |
| 2026 | 8066 | 0 | 0 |
| All | 80733 | 96 | 0 |

Confidence label × paper_type in production outputs (all 97,492):

| paper_type | Low | Medium |
|---|---|---|
| application | 96 | 80637 |
| discourse | 0 | 8899 |
| evaluative | 0 | 7860 |

**Inference: all 96 `Low` records are fallbacks.** No record carries `High` (0 of 97,492): the parser keeps only the exact strings High/Medium/Low and forces anything else to Medium, so the model's own confidence values were evidently never the exact string `High` or `Low` (most likely lower-case). A `Low` therefore arises only from the fallback branch. Cross-check: of the 96 `Low` records, 9 were written by the batch path, which equals the 9 batch-level failures in the log; the rest came from the synchronous first 2,500 records. Silent exclusions by year and path:

| pub_year | batch (prefilter_batch.py) | synchronous (prefilter.py) | All |
|---|---|---|---|
| 2020 | 0 | 1 | 1 |
| 2021 | 1 | 86 | 87 |
| 2024 | 2 | 0 | 2 |
| 2025 | 6 | 0 | 6 |
| All | 9 | 87 | 96 |

Side finding: the stored `type_confidence` carries no information (Medium for every successful call).

## Output files

- [T1_confusion_3x3.csv](T1_confusion_3x3.csv)
- [T1_confusion_2x2.csv](T1_confusion_2x2.csv)
- [T1_binary_keep_drop_metrics.csv](T1_binary_keep_drop_metrics.csv)
- [T1_binary_by_pilot_year.csv](T1_binary_by_pilot_year.csv)
- [T1_silent_exclusion_upper_bound_by_year.csv](T1_silent_exclusion_upper_bound_by_year.csv)
- [T1_fallback_Low_by_year_and_path.csv](T1_fallback_Low_by_year_and_path.csv)
