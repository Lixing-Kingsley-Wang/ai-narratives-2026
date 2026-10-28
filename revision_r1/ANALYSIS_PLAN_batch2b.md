# Analysis plan: R1 Batch 2b (pre-specified)

JMIR #109710, major revision R1. This plan is committed **before** any B2–B6 computation or API call.

**Primary window.** 2021–2025. January–April 2026 appears only where stated.

**Common conventions.**

- Report n/N with every percentage and a 95% CI for every estimate.
- *P* values are exact and in JMIR format: no leading zero, and *P*<.001 at the floor.
- Seed 42 throughout. Per-cell seeds are deterministic, `42 + cell_index` in a fixed sort order, and never use `hash()`.
- Software: Python 3.12.3 in `revision_r1/.venv`, pinned in `revision_r1/requirements_r1.txt`; statsmodels 0.15.0.
- The project venv is not modified.

## Finding recorded before this plan (affects B3 framing; no change to B3)

**The prompt that produced the reported stance labels is not the one the manuscript prints.**

- **Labels came from v1.** Every reported stance label comes from the **v1** prompt, SHA-256 `b3949917…`. That prompt is identical in `classify_stance.py`, in `classify_stance_batch.py` at the production commit `9c79cd5`, and in `classify_stance_batch.py.v1_backup`.
- **v1's Advocacy definition is:** "Advocacy: strongly pro-AI. Emphasises transformative potential, minimal caveats."
- **The manuscript prints v2.** Supplementary Note 2 reproduces the **v2** prompt (current `classify_stance_batch.py`, 8,164 characters). The Methods sentence "Advocacy required both transformative language … and minimal or no acknowledged caveats" paraphrases v2's "ADVOCACY THRESHOLD".
- **B3 runs as written.** B3 is run exactly as specified; its prompt defines its own construct. The finding is reported in REPORT_batch2b and the B7 corrections list.

## B1 · Prefilter CIs with zero-event cells (D1, X2)

Implemented already as protocol **Amendment 3** in commit `c146e1b` (2026-10-28), before this plan. Script: `a4_prefilter_exact_ci.py`; the frozen scorer is untouched.

- **Method.** For each stratum-year cell with x human-KEEP out of n, the proportion is drawn from Beta(x+0.5, n−x+0.5), 10,000 draws, seed 42, and propagated through the design weights (N_cell / n_cell).
- **Estimands covered:**
  - 1−NPV per year and pooled, and the 2021–22 vs 2024–25 difference;
  - missed records;
  - PPV among retained records;
  - precision within EX-F;
  - population-weighted sensitivity, specificity, PPV, NPV, κ and AC1 for the production prefilter;
  - all three borderline variants.
- **Exact intervals.** Single cells also get exact Clopper–Pearson intervals.
- **Full-abstract 2×2.** It requires sub-cells (stratum × year × full-abstract label) with n=1–3, and on those the Jeffreys interval excludes the point estimate. This was recorded in Amendment 3, and the bootstrap interval is kept for that table.
- **B1 output.** The script is re-run into `outputs/B1/` with the old (bootstrap) and new (Jeffreys) CIs side by side. The point estimates do not change.

## B2 · Stance on the records recovered by the full-abstract re-run (D1, X2)

**Frame.** The 2,850 records (all years) with production label `application` and full-abstract label discourse or evaluative, from `outputs/A2/a2_fullabstract_labels.csv`.

**Classifier.** Script `b2_stance_recovered_batch.py`, a copy of `classify_stance_batch.py.v1_backup`, which is byte-identical to the production batch script at `9c79cd5`.

| Setting | Value |
|---|---|
| Model | `claude-sonnet-4-6` |
| API | Message Batches |
| Temperature | Not set |
| `max_tokens` | 120 |
| `system` | v1 `SYSTEM_PROMPT`; SHA-256 asserted equal to `classify_stance.py` and to `9c79cd5:classify_stance_batch.py` |
| User message | v1 `build_prompt`: `Title: …\nAbstract: <full abstract>` |

- **Failures.** Parsing follows v1 `parse_response`. Failures are FAILED, never defaulted, and are resubmitted once.
- **Cost gate.** Exact `count_tokens` on a 1,000-record random sample of the frame (`random.Random(42)`), extrapolated. Output is assumed to be 40 tokens per request. Sonnet 4.6 costs $3/$15 per MTok, with the 50% Batch discount. Ceiling USD 25; if the projection is higher, stop and ask.

**Corpora, 2021–2025:**

| Corpus | Definition |
|---|---|
| (a) Production | The T4 analytic set: valid stance, year 2021–2025 |
| (b) Augmented | (a) plus the recovered records with a valid stance |
| (c) Precision-weighted augmented | (b), with each recovered record weighted by the EX-F human-KEEP precision of its year (A3 primary, Amendment 2: 2021 0.733, 2022 0.800, 2023 0.667, 2024 0.733, 2025 0.933). Production records get weight 1. |
| (d) Full-abstract | Every record whose full-abstract label is discourse or evaluative, with a stance label: production v1 stance if retained, B2 stance if recovered. This drops the 1,841 records that production retained but the re-run labels `application`. |

**Per corpus:**

- annual distribution of all 5 stances, plus critical and favourable;
- critical and Advocacy shares with n/N and bootstrap 95% CI. The CI uses 1000 joint row-level resamples, seed 42; for (c) the shares are weighted and the weighted share is recomputed on each resample;
- Spearman ρ over 5 annual points with exact permutation *P*;
- record-level logistic OR per year (year centred), with Wald CI and *P*. For (c) this is a frequency-weighted GLM with HC0 robust SEs.

**Also:**

- stance distribution of the recovered records vs the retained records, overall and by year, as n/N;
- a movement table showing each trend estimate from (a) to (d).

## B3 · Symmetric endorsement re-classification (X1, D2b)

**Frame.**

- All records from 2021 to April 2026 (valid stance) with production stance Cautious Optimism or Advocacy (expected 10,749).
- Plus any model-favourable record in the 300-record stance validation set that is not already in that frame (for example, dated 2020).

**Classifier.** Script `b3_endorsement_batch.py`.

| Setting | Value |
|---|---|
| Model | `claude-sonnet-4-6` |
| API | Message Batches |
| Temperature | **0** (explicit) |
| `max_tokens` | 30 |
| User message | `Title: …\nAbstract: <full abstract>` (v1 input format; title only if the abstract is empty) |
| System prompt | As below, read from `revision_r1/scripts/b3_prompt.txt`; SHA-256 `27d28077cd7485fddcdfe4f0da3f4a3c13ad36a310bcd23f1544a5a89db50cf6`, asserted at runtime |

- **Parsing.** `{"strong_endorsement": "yes"|"no"}`. Anything else is FAILED, resubmitted once.
- **Cost gate.** As in B2; ceiling USD 25.
- **Combined ceiling.** B2 + B3 ≤ USD 50.

System prompt (verbatim):

```
You are classifying medical journal abstracts that discuss or evaluate artificial intelligence (AI). Every abstract you see has already been judged broadly favourable toward AI. Decide whether the authors' own conclusion is a STRONG ENDORSEMENT of AI.

STRONG ENDORSEMENT = "yes" when the authors' evaluative conclusion is strongly positive about AI's benefit, performance, or readiness for use, with minimal or no acknowledged caveats. The wording does not matter: transformative language such as "revolutionize" or "paradigm shift" is NOT required. A plainly worded report that AI matched or outperformed clinicians counts as "yes" if the conclusion endorses AI with minimal or no acknowledged caveats.

STRONG ENDORSEMENT = "no" when the conclusion acknowledges substantive caveats, limitations, risks, or open challenges (for example, the need for further validation before clinical use, human oversight, bias, specific failure modes, or limited generalizability), or when the abstract reaches no evaluative conclusion about AI.

Judge the authors' own evaluative commitment in their discussion and conclusion, not the sentiment of the background framing.

Return ONLY valid JSON: {"strong_endorsement": "yes"} or {"strong_endorsement": "no"}
```

**Analyses.**

1. **Symmetric scale.** Alarm / Caution / Neutral / Cautious Optimism (flag = no) / Strong endorsement (flag = yes, whatever the production label). The critical side is unchanged. Report the distribution overall and by year (2021–2025 and Jan–Apr 2026).
2. **Trend, 2021–2025.**
   - Annual prevalence of Strong endorsement, using **all** analytic records in the year (T4 denominators) as the denominator. Report n/N and a bootstrap CI.
   - Spearman ρ with exact *P*, and the logistic OR per year.
   - Shown side by side with the Advocacy trend from T4.
3. **Consistency.** The share of production Advocacy records flagged yes, and the share of production Cautious Optimism records flagged yes, overall and by year, as n/N with a Clopper–Pearson CI.
4. **Agreement with the existing human labels.** On the model-favourable validation records:
   - a 2×2 of human Advocacy vs flag = yes;
   - sensitivity, PPV and Cohen κ, with bootstrap CIs (1000 resamples, seed 42);
   - the distribution of human labels among flag = yes records.
   - Reported for all model-favourable validation records, and for the in-scope subset (T2 layer A).
5. **Secondary: misclassification-corrected prevalence.** Uses the Batch 1 T2 estimator, with strata = model stance × flag, i.e. (Alarm), (Caution), (Neutral), (CO, no), (CO, yes), (Advocacy, no), (Advocacy, yes).
   - Target: human Advocacy, the only human reference label available.
   - P(human Advocacy | stratum) is estimated from all 300 validation records.
   - Annual 2021–2025 prevalence, with a bootstrap that resamples validation records within strata and corpus records jointly (1000 resamples, seed 42).
   - Cells with fewer than 10 validation records are marked.

## B4 · Multivariable regression (D4a, X3, D3)

**Data.** The 2021–2025 analytic records, n = 14,058.

**Variables.**

| Variable | Definition |
|---|---|
| Outcome (primary) | Critical = Alarm or Caution |
| Year | Continuous, centred on the sample mean |
| Genre | `paper_type`: discourse / evaluative |
| Publication type | 5 categories, `simplify_pubtype_5` |
| Specialty | 18 categories plus "Unassigned" (FAILED) |
| Region | `geography_classifications.csv` (Table S9 file), with Unknown as its own level |
| Cluster | Normalised journal title: `sjr_filter.normalise`, then `ALIAS_PATCH` |

- **Reference level** for each factor: its most frequent category in the data. The levels are stated in the output.
- **Primary model.** Logistic GLM with cluster-robust (journal) covariance from statsmodels `cov_type="cluster"`.
- **Every model reports:** n, events and clusters; adjusted ORs with 95% CIs and *P* next to unadjusted ORs (single-covariate logit, same clustering); and average marginal predicted probabilities by year (2021…2025), specialty, region and publication type.
  - An average marginal predicted probability for a level sets that covariate to the level for every record and averages the predicted probabilities.
  - Its CI uses the delta method with the cluster-robust covariance.
- **Secondary models.**
  1. **Ordinal proportional-odds** (statsmodels `OrderedModel`, logit link) over Alarm < Caution < Neutral < Cautious Optimism < Advocacy, same covariates, cluster-robust covariance. If cluster-robust covariance is unavailable for this model class, report model-based SEs and say so.
     - **Proportional-odds check:** run four binary logits, one for each cut point (≤ k vs > k), same covariates and clustering.
     - A covariate's assumption is flagged as failing when the ordinal coefficient lies outside the 95% CI of at least one cut-point coefficient, or when the cut-point coefficients differ in sign. Both sides are reported.
  2. **Logistic for Advocacy** vs not, same covariates. Specialty levels with fewer than 5 Advocacy events are collapsed into "Other"; the same rule applies to region and publication type if needed. All collapsing is reported.
- **Sensitivity models** (critical outcome).
  1. Year as a categorical variable (reference 2021).
  2. Adding Jan–Apr 2026 as its own year level (categorical year).
  3. Journal fixed effects. Restricted to journals with at least 10 records in 2021–2025 and variation in the outcome; continuous year; cluster-robust by journal. Report the number of journals and records.
  4. Country in place of region. Countries with at least 100 records are kept and the rest pooled as "Other". Country comes from the Table S7 resolver `resolve_country`; unresolved is its own level. Report the adjusted United States vs China contrast (OR and CI).
- **Excluded covariates:** model type (defined only for critical records) and FDA cleared-device count (an 18-unit ecological variable). This is stated in the output.

## B5 · SJR medical-category sensitivity (D6)

**Corpora.** Restricted corpora come from the Batch 1 T7 record-level quartiles (`outputs/T7_record_level_quartiles.csv`). A record is kept when its journal-year is Q1/Q2 in at least one category in the definition's category set:

| Definition | Role | Category set |
|---|---|---|
| **D1** | Primary | Medicine area |
| D2 | Bound | D1 without "Medicine (miscellaneous)" |
| D3 | Bound | Broad health sciences |

This is a restriction only; nothing is re-classified.

**Recomputed on each corpus, next to the full corpus:**

- overall stance distribution (2021–Apr 2026, and 2021–2025);
- 2021–2025 critical and Advocacy trends: annual shares, Spearman ρ with exact *P*, and OR per year;
- the four headline theme trends: patient safety, hallucination/errors, regulation, ethics & bias;
- critical rate by specialty and the FDA ρ, using the 18 categories, categories with at least 30 records, and the same FDA counts as Table S17;
- critical rate by region;
- critical rate by publication type.

**Removals.** The number of records removed under each definition, by year.

## B6 · MeSH and keyword triangulation (D5)

**Re-fetch.**

- Endpoint: NCBI E-utilities `efetch.fcgi`, `db=pubmed`, `retmode=xml`.
- Records: the 16,759 retained PMIDs, in batches of 200, at most 3 requests per second (no NCBI API key is configured).
- Parameters: `tool=ai_narratives_study`; `email` from the main checkout's `.env` (as `fetch_pubmed_medical.py` does).
- Raw XML is stored gzipped under `outputs/B6/raw/`.
- Parsed table: PMID → MeSH descriptors (with `MajorTopicYN`) and author keywords (`KeywordList/Keyword`).
- Completeness by year: the share of records with at least one MeSH descriptor, and the share with at least one author keyword.

**Analysis 1 · Pre-specified lexicon trends.** Critical records only, 2021–2025. A record matches a theme if any lexicon term matches its title, abstract or author keywords, or any listed MeSH descriptor is among its MeSH descriptors.

- Text matching is case-insensitive.
- A plain term matches whole words; a multi-word term matches the phrase with whole-word boundaries.
- `*` is a prefix wildcard: it matches the word start followed by any letters.
- MeSH matching is exact on the descriptor name.

Lexicons (verbatim):

| Theme | Lexicon |
|---|---|
| Errors and hallucination | hallucinat*, confabulat*, fabricat*, inaccura*, misinformation, error*, incorrect, factual* ; MeSH: Diagnostic Errors, Medical Errors |
| Patient safety | patient safety, safety, harm*, adverse ; MeSH: Patient Safety, Patient Harm |
| Regulation | regulat*, governance, oversight, liability, legislat*, policy, policies, accountab* ; MeSH: Government Regulation, Legislation as Topic, Health Policy |
| Ethics and bias | ethic*, bias*, fairness, equit*, discriminat*, justice ; MeSH: Ethics, Medical; Bias |

- **MeSH parsing note.** In the ethics row, "MeSH: Ethics, Medical; Bias" is read as two descriptors: "Ethics, Medical" and "Bias".
- **Per theme:** annual share with n/N and bootstrap CI (joint resample, seed 42), Spearman ρ with exact *P*, and the logistic OR per year, shown next to the direction of the LLM theme trend from T4.

**Analysis 2 · Emerging terms.**

- Terms are author keywords plus MeSH descriptor names, lower-cased, with whitespace collapsed and duplicates removed within a record.
- Records: all retained records from 2021–2025.
- Comparison: 2024–2025 vs 2021–2022, using the weighted log-odds ratio with an informative Dirichlet prior (Monroe, Colaresi & Quinn 2008).
  - Counts are document frequencies.
  - The prior is α_w = α0 × df_w(background) / Σ df(background), with background = all 16,759 retained records and α0 = 1,000.
  - z = δ̂ / √σ̂².
- A term qualifies only if it appears in at least 20 records across the two compared groups.
- Report the top 30 terms in each direction, with z, counts and group sizes.

**Analysis 3 · Terms that separate stance.**

- Same method: critical (Alarm or Caution) vs favourable (Cautious Optimism or Advocacy), 2021–2025, with the same background prior.
- Report the top 30 terms in each direction.

**Not done:** co-occurrence or collaboration networks, and CiteSpace / VOSviewer / Bibliometrix.

**Figure.** One draft dot plot of z-scores for Analyses 2 and 3, with exact values printed. It must not be a simple bar graph and must use no asterisks. Output as `figures/B6_terms_r1_draft.{png,pdf}`.

## B7 · Numeric corrections (E13, D8)

`outputs/B7_corrections.md` lists old value → corrected value → source for every Batch 1 discrepancy that changes a printed number. At minimum:

1. Table S1 exact permutation *P* for every row, for 2021–2026 and for 2021–2025.
2. Table S3 regenerated with deterministic per-cell seeds (`42 + cell_index`, cells sorted by genre then year) for both windows.
3. Table S9 and Results region n's on the 16,747 denominator.
4. Commentary critical rate: 56/104 = 53.8%.
5. Q1/Q2 share: 98,626/112,011 = 88.05%, correctly rounded to 88.1%.
6. Fabrication-involved share by year.
7. Failure-mode κ_max and model-type AC1 to 3 decimals.
8. Any other printed number that changes, including the stance-prompt finding above, which changes no number but changes the text of Supplementary Note 2 and the Methods.
