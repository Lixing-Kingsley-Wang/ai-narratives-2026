# Analysis plan · Batch 2d (JMIR #109710, R1)

Written and committed on 2026-10-31, **before** any D2 or D3 computation and before the D1 recomputation. D2 and D3
are **post hoc** analyses (decided after the Batch 2b and 2c results were seen, 2026-10-31); every output carries
that label and date. No LLM API calls; no data fetches; only files that already exist.

## D1 · Journal cluster-robust CIs for every unadjusted record-level OR per year

- **Model.** For each series: logistic regression of the binary outcome on publication year (continuous; centred on
  the mean year of the series' records), fitted by maximum likelihood (statsmodels GLM, binomial, logit link), with
  `cov_type="cluster"` and groups = journal. The point estimate is the same maximum-likelihood estimate as the
  Batch 2c Wald fit (`r1_common.logit_trend`); only the SE, the 95% CI (normal, ±1.959964 SE on the log scale)
  and the two-sided Wald *P* change.
- **Journal identifier.** Exactly as B4: `sjr_filter.ALIAS_PATCH.get(sjr_filter.normalise(journal), sjr_filter.normalise(journal))`,
  imported from `sjr_filter.py` (not retyped); `pd.factorize` of that string gives the groups. Expected: 2278 clusters
  in the 14,058-record analytic corpus. For record sets outside the analytic corpus (eligible records for the keep
  rate; Q3 arm; B2 recovered records) the same function is applied to the record's journal field, and the cluster count
  is reported.
- **Series.** Every series that has an unadjusted OR per year in `NUMBERS_BOOK_R1.csv`, each on the record set and
  outcome Batch 2c used: the five stances, critical, favourable; critical within discourse and within evaluative; the
  ten themes among critical records; the four B6 lexicon series; the mechanism series (four gated failure-mode
  components, fabrication-involved among gated, generative share, fabrication share among all abstract-present critical
  records and among generative-model records); the prefilter keep rate (eligible records 2021-2025); B3 strong
  endorsement and its upper bound; B2 corpora (a)-(d) for critical and Advocacy (corpus (c): frequency weights = audit
  precision by year, as in B2, now with journal clustering instead of HC0); B5 full corpus and D1-D3 for critical,
  Advocacy and the four headline themes; the Q3 arm (critical and the five stances).
- **Not changed.** Adjusted ORs (B4: already journal-clustered), Spearman ρ and exact *P*, and every proportion CI.
- **Checks.** Point ORs must equal Batch 2c to the printed precision (3 decimals); the maximum absolute difference is
  reported, and any printed difference is listed. The unadjusted year OR for critical must reproduce B4's unadjusted
  cluster-robust estimate (1.077, 1.038-1.116).
- **Flags.** Every OR whose *P* moves across .05 in either direction, or whose 95% CI changes between excluding and
  including 1.
- **Outputs.** `final/NUMBERS_BOOK_R1_v2.{md,csv}` (same IDs; OR rows carry the new CI and *P*; composite rows that
  quote an OR are rewritten); `final/NUMBERS_DIFF_v1_v2.csv`; `_v2` copies of Table 2, Table 3 and every MA3 unit or
  figure caption that prints a changed OR. Batch 2c files are not modified.

## D2 · Post hoc source decomposition of the B6 lexicon trends

- **Population.** Critical records (Alarm or Caution) dated 2021-2025 (n=4283), built exactly as `b6_terms.py`
  Analysis 1 (title and abstract from `classified_medical_Q1Q2.csv`; author keywords and MeSH from
  `outputs/B6/b6_mesh_keywords.csv`).
- **Lexicons and matching.** `b6_terms.LEX`, `b6_terms.term_regex` and `b6_terms.mesh_list`, imported, not retyped. A
  text source matches when `term_regex(terms)` finds a match; MeSH matches when any listed descriptor equals a record
  descriptor.
- **Rows per lexicon theme:**
  - (a) All sources: text = title + " " + abstract + " " + keywords (keywords joined with " ; "), or MeSH. Must
    reproduce `B6_lexicon_annual.csv` exactly (k and n per year).
  - (b) Title + abstract: text = title + " " + abstract.
  - (c) Keywords or MeSH only: (keyword text match or MeSH match) and not (b).
  - (d) Classifier input: title + " " + the first 400 characters of the abstract (what the theme classifier read).
  - (e) Later abstract only: a match in abstract characters 401 onward (abstract[400:]) and no match in (d).
- **Term rows.** For (b) text, each lexicon term separately, plus the phrase "human oversight" (`term_regex(["human oversight"])`).
- **Statistics.** Annual share 2021-2025 with n/N and the 95% percentile bootstrap CI (`r1_common.boot_group_share`:
  joint row resample, 1000, seed 42); OR per year with the D1 journal cluster-robust CI and *P*. Median abstract length
  (characters, abstract-present and all) by year.
- **Expected values** supplied by Peter from an exploratory read-only run (regulation, 2021→2025): (a) 24.8, 22.5, 20.8,
  19.5, 29.9; (b) 23.7, 22.5, 20.5, 18.8, 29.3; (c) 1.1, 0.0, 0.3, 0.7, 0.7; (d) 8.1, 7.8, 6.2, 5.9, 7.5; (e) 15.6,
  14.7, 14.3, 12.9, 21.6; "oversight" 3.0, 2.1, 2.2, 2.1, 9.3; "human oversight" 0.4, 0.3, 0.5, 0.7, 3.2; median
  abstract length 1426 (2021) and 1766 (2025). Mismatches are reported; nothing is tuned to match.
- **Outputs.** `final/ma/new_tables/MA3_lexicon_decomposition.{md,docx}`; numbers-book rows `RES-LEXD-*` in the v2 book.
  `ma_order.yaml` is not changed.

## D3 · Post hoc period-specific misclassification correction

- **Data.** The 300 stance-validation records and human/model labels from `t2_stance_perclass.load_validation()`; the
  primary set is all 300 (human codes as in T2; not-codable records coded Neutral), as in the pre-specified T2
  correction. Corpus: the 14,058 analytic records 2021-2025 (all records, as the T2 primary row).
- **Periods.** 2021-2023 and 2024-2025 by the validation record's publication year. Records dated 2026 (and any dated
  2020) are excluded from period estimates; their number is reported.
- **Strata.** Model stance only (Alarm, Caution, Neutral, Cautious Optimism, Advocacy), as in T2 (not the B3 stance x
  flag strata).
- **(1) Conversion rates.** For each stratum x period: n, P(human Advocacy | stratum) and P(human critical = Alarm or
  Caution | stratum), with exact Clopper-Pearson 95% CIs; Fisher exact test (two-sided) of period difference within each
  stratum, per outcome.
- **(2) Advocacy accuracy by period.** Model-Advocacy precision P(human Advocacy | model Advocacy) and human-Advocacy
  recall P(model Advocacy | human Advocacy), by period, for all 300 and for the in-scope 225 (T2 layer A), with
  Clopper-Pearson CIs.
- **(3) Period-specific corrected prevalence.** For year y in period g: corrected_y = Σ_c share_y(model = c) ×
  P_g(human target | c), for target = Advocacy and critical; 2021-2023 rates applied to 2021-2023, 2024-2025 rates to
  2024-2025. Point estimates use the observed rates. CI: 1000 bootstrap draws, `numpy.random.default_rng(42)`; in each
  draw, validation records are resampled with replacement within stratum x period, except that a cell with zero events
  or with all records positive for the target gets its rate from a Jeffreys draw Beta(k+½, n−k+½) (as in Amendment 3);
  corpus records are resampled jointly (whole 2021-2025 set). Report annual values 2021-2025 and Δ 2025 − 2021 with
  95% percentile CIs. Every stratum x period cell with fewer than 10 validation records is marked.
- **(4) Comparison.** Side by side with the pre-specified constant-rate T2 values (primary: all 300; all records):
  Advocacy 6.16% → 5.13% (Δ −1.03 percentage points); critical 26.99% → 31.36% (Δ +4.37). As a code check, the
  constant-rate estimator re-implemented here must reproduce these point values.
- **Outputs.** `final/ma/new_tables/MA3_period_correction.{md,docx}`; rows `VAL-ST-PER-*` in the v2 book.

## Reporting

`revision_r1/REPORT_batch2d.md`: this plan's commit hash; D1 changed-row count, flag list and `_v2` paths; D2
reproduction check, mismatches and the table; D3 tables, side-by-side comparison and the count of cells with fewer than
10 records; `output/` checksums; no API calls; nothing pushed. Chat reports aggregates only.
