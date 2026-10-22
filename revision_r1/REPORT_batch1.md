# JMIR #109710 — Major revision R1, Batch 1 report

Branch `jmir-r1-major-revision` (from `31ed027`). Numbers only; no interpretation, no manuscript edits, no LLM calls, nothing pushed.

**Setup notes (T0)**

- Worktree was clean at start. The main checkout (`~/Documents/科研/ai-narratives-2026`, branch `prompt-revision-v2`) has its own uncommitted changes; it was only read, never modified.
- Gitignored inputs (`classified_medical_Q1Q2.csv`, pre-prefilter corpus, pilot files, logs) were read from the main checkout's `output/`. The pilot and classified files there are byte-identical to their last committed versions (`31ed027^`).
- Inputs: the four submitted files were not in `revision_r1/inputs/`, so I copied them from `~/Documents/科研/Manuscripts/AI Review Dan/` (manuscript `Final Manuscript Submission LW jmir.docx`, md5 identical to `~/Downloads/109710-1557887-1-SM.docx`, plus Multimedia Appendices 1–3 dated 18 Aug). `revision_r1/inputs/` is in `.git/info/exclude`. **Peter: please confirm these are the submitted versions.**
- Python: the project venv (no `statsmodels`). The logistic regressions are written in plain numpy (IRLS), with Wald CIs and likelihood-ratio P.

---

## T1 · D1, X2 — Prefilter validation

Full output: [outputs/T1_prefilter_validation.md](outputs/T1_prefilter_validation.md)

- **Pilot provenance.** Same model string, system prompt and 300-character truncation in code. The script that wrote `pilot_200_full_haiku.csv` is not in any branch. **The sampling design is undocumented.** `make_pilot.py` would draw 50 records per year from 2021–2024, but the committed pilot spans 2021–2026 (16/29/29/42/60/24). That mix is close to the corpus year mix (χ²₅=2.57, P=.77), which fits a simple random sample, but no code or seed confirms it. **Blinding:** the coding workbook has no model-label column, and human labels did not change across the 50→100→200 steps (0/50, 0/100 changed). This fits blind coding but cannot prove it.
- **3×3 table.** Raw agreement 171/200 (85.5%) and κ 0.511 reproduce. **The κ CI does not reproduce:** I get 0.345–0.646; the manuscript reports 0.35–0.68.
- **Binary KEEP vs DROP** (n=200; bootstrap 95% CI):

| Metric | n/N | Estimate (95% CI) |
|---|---|---|
| Sensitivity (recall of KEEP) | 20/38 | 0.526 (0.370–0.676) |
| Specificity | 152/162 | 0.938 (0.898–0.970) |
| PPV (precision) | 20/30 | 0.667 (0.480–0.824) |
| NPV | 152/170 | 0.894 (0.848–0.937) |
| F1 | — | 0.588 (0.436–0.708) |
| Accuracy | 172/200 | 0.860 (0.815–0.905) |
| Cohen κ / Gwet AC1 / PABAK | — | 0.505 (0.331–0.646) / 0.805 (0.728–0.871) / 0.720 (0.630–0.810) |
| Human KEEP prevalence | 38/200 | 0.190 (0.135–0.240) |

- **Silent exclusions: 96 records** were defaulted to `application` by the failure branch: 87 on the synchronous path (first 2,500 records: 86 from 2021, 1 from 2020) and 9 on the batch path (2021: 1, 2024: 2, 2025: 6). The 9 batch records match the 9 failures in the batch log (8 errored plus 1 unaccounted). **No record has `type_confidence = High`**, so a `Low` value can only come from the fallback branch, and the stored confidence field carries no information.

## T2 · D2b (X1) — Stance per-class performance

Full output: [outputs/T2_stance_perclass.md](outputs/T2_stance_perclass.md)

- **Table S18 (a) and (b) reproduce exactly**, as do the S18(c) counts.
- Per-class F1, in-scope set (n=225): Alarm 0.82 (0.70–0.90), Caution 0.61 (0.49–0.71), Neutral 0.54 (0.32–0.71), Cautious Optimism 0.68 (0.59–0.76), Advocacy 0.68 (0.51–0.81). Macro-F1 0.67 (0.59–0.73); 0.67 (0.62–0.73) on all 300.
- **Advocacy vs not** (n=225): sensitivity 17/24 = 0.708 (0.500–0.889); PPV 17/26 = 0.654 (0.464–0.833); κ 0.640.
- **Critical vs not** (n=225): sensitivity 76/94 = 0.809; PPV 76/90 = 0.844; κ 0.706.
- **3-class view** (n=225): 180/225 agreement (80.0%), κ 0.648.
- **Non-adjacent disagreements** (≥2 steps): 28/225 and 32/300. All are Caution↔Cautious Optimism, Alarm↔Cautious Optimism, or Neutral→Advocacy (4/300). None are 4 steps apart.
- **Sampling design confirmed** (`export_validation.py`): fixed targets 40/60/70/100/30 by model stance, drawn only from abstract-present records. Sampling fractions: Alarm 4.74%, Caution 1.54%, Neutral 11.02%, Cautious Optimism 0.98%, Advocacy 16.85%.
- **Corrected prevalence, 2021–2025** (primary: all 300; assumes P(human | model) is constant across years):

| Outcome | 2021 observed | 2021 corrected | 2025 observed | 2025 corrected | Δ corrected (95% CI) |
|---|---|---|---|---|---|
| Advocacy | 2.92% | 6.16% (3.13–9.65) | 1.12% | 5.13% (2.33–8.41) | −1.03 pp (−1.79 to −0.42) |
| Critical | 25.40% | 26.99% (21.82–32.64) | 30.99% | 31.36% (26.25–36.75) | +4.37 pp (2.61 to 5.99) |

  With the in-scope 225 as the validation set, the Advocacy Δ is −1.19 pp (−2.02 to −0.48). Abstract-present-only rows are in the csv.
- Advocacy review list: 37 records (17 both, 7 human only, 13 model only) in [T2_advocacy_records_for_review.csv](outputs/T2_advocacy_records_for_review.csv).

## T3 · X4a — Mechanism confusion matrices

Full output: [outputs/T3_mechanism_confusion.md](outputs/T3_mechanism_confusion.md)

- **Reproduced:** failure-mode κ 0.574, AC1 0.600, raw agreement 69.4%, κ/κ_max 0.761; model-type κ 0.843, raw agreement 90.7%, κ/κ_max 0.857.
- **Two values match only through double rounding:** failure-mode κ_max = 0.7549 (manuscript 0.76) and model-type AC1 = 0.8847 (manuscript 0.89).
- Per-class F1, failure mode: confabulation 0.47 (0.21–0.67), misclassification 0.69, both 0.63, none/unclear 0.82.
- Per-class F1, model type: generative 0.98, discriminative 0.85, both 0.75 (n=4), unclear 0.77.
- **Direction of fabrication disagreements:** the model said fabrication when the human did not in 20/108 cases; the reverse happened 1/108 (exact McNemar P<.001). Prevalence of fabrication labels: model 42/108, human 23/108.
- A draft Table S19 in S18 style is included.

## T4 · D3, X3 — Temporal re-analysis, 2021–2025

Full output: [outputs/T4_temporal_2021_2025.md](outputs/T4_temporal_2021_2025.md); figures in `figures/*_r1_draft.{png,pdf}`; captions with exact P values in [outputs/T4_figure_captions.md](outputs/T4_figure_captions.md).

- **Bootstrap check:** my bootstrap reproduces the original stance-year and theme-year CIs exactly (max difference ~1e-14).
- **Stance trends**, 2021→2025, n = 14,058 (Spearman exact P and logistic OR per year):

| Outcome | 2021 → 2025 | Spearman ρ (exact P) | OR per year (95% CI) | P |
|---|---|---|---|---|
| Critical | 25.4% (270/1,063) → 31.0% (1,828/5,898) | +0.80 (.133) | 1.077 (1.046–1.108) | <.001 |
| Advocacy | 2.9% (31/1,063) → 1.1% (66/5,898) | −1.00 (.017, the minimum attainable) | 0.793 (0.721–0.872) | <.001 |

  Alarm: OR 1.202. Caution: OR 1.038 (P=.016). Neutral: OR 0.810. Cautious Optimism: OR 0.999 (P=.96).
- **Within-genre critical share** (Table S3 domain): discourse 30.2→35.4% (ρ +0.90, P=.083; OR 1.06); evaluative 14.6→26.8% (ρ +0.80, P=.133; OR 1.21). Discourse:evaluative ratio 2.24→0.95.
- **Themes, Δ 2021→2025:** safety +5.7 pp, errors +27.4, regulation −23.1, ethics −3.6 (old window: +11.0, +30.9, −22.0, −8.1).
- **Mechanism:** generative share 5.3→57.8% (OR 2.03); fabrication share 0→11.4% (OR 1.55); fabrication among generative OR 0.98 (P=.76).
- **Keep rate:** 9.5→20.4% (ρ +1.00, P=.017).
- **Q3 critical share:** 23.0→28.1% (ρ +0.80, P=.133; OR 1.09, P=.092).
- **Endpoint table:** every domain, old (2021→2026) next to new (2021→2025): [T4_endpoint_comparison.csv](outputs/T4_endpoint_comparison.csv).
- **2026:** a separate descriptive table (no trend statistics): [T4_2026_descriptive.csv](outputs/T4_2026_descriptive.csv).
- **Figure changes:**
  - Nothing from 2026 appears in any figure.
  - Figure 1a is redrawn as points with CI whiskers instead of single-variable bars, because JMIR does not allow simple bar graphs.
  - Exact values are printed on every panel, and asterisks are replaced by exact P values in the captions.
  - The Figure 2 inset is kept: the 2021–2023 counts (56/61/215) are still dwarfed by 2025 (883).

## T5 · E12, E4, E13 — Claims ledger

Full output: [outputs/T5_claims_ledger.md](outputs/T5_claims_ledger.md) and [T5_claims_ledger.csv](outputs/T5_claims_ledger.csv). Cross-sectional results for both windows side by side: [T5_crosssectional_both_windows.md](outputs/T5_crosssectional_both_windows.md).

- **81 statements** (Abstract, Results, captions):
  - 66 reproduce and 5 partially.
  - 1 does not reproduce (R29 / A08 fabrication share).
  - 3 were not re-checked: the v2 direction, the "5 drug discovery" manual reading, and the plotting convention in the Figure 3 caption.
  - 6 are method or reference lines, not results.
- **Missing CI or n/N** (heuristic flag): 32 sentences have a percentage without a CI and 34 have a percentage without n/N.
- **Discussion numbers:** 8 sentences carry result numbers (19 contain any digit, including years and citation numbers). None of them compares a number directly with a published estimate (list in section 4 of the ledger).

## T6 · E14 (E10) — Missing data

Full output: [outputs/T6_missing_data.md](outputs/T6_missing_data.md) (stage table, losses by year, title-only counts per stage, nested flow list for a JARS flowchart)

| Stage | Loss |
|---|---|
| Duplicates | 129,557 → 116,117 (13,440) |
| Conference / preprint | 4,106 |
| SJR unmatched | 7,922 (see the Q4 issue below) |
| Cover-date cutoff | 1,134, all 2026 |
| Prefilter `application` | 80,733 (96 of them failure defaults) |
| Stance FAILED | 10 |
| Dated 2020 | 2 |
| Mechanism FAILED | 2 |
| Title-only records in the critical set | 412 |
| Specialty FAILED | 13 |
| Theme batch error, defaulted to `['other']` | 1 (51 records have `other` as their only theme) |

- **Country (Figure 4 resolver):** 1,628/16,747 unresolved (9.7%), so 90.3% resolved, as reported.
- **Region file:** 593 records are Unknown. The two resolvers differ; see the discrepancy list.
- **Title-only share:** 6.0% (1,003/16,759) among retained records vs 0.6% (465/80,733) among application records.
- **Publication type:** no unmapped types.

## T7 · D6 — SJR quartile feasibility

Full output: [outputs/T7_sjr_quartile.md](outputs/T7_sjr_quartile.md)

- **The SJR files contain per-category quartiles (`Categories`) and `Areas`.** `sjr_filter.py` uses neither.
- **Three candidate definitions of "medicine-related"** are proposed; none is chosen. Records whose Q1/Q2 status rests only on a non-medical category (Q3/Q4 in all medical categories, or no medical category at all):

| Definition | Analytic set (n = 16,747) | Eligible set (n = 97,492) |
|---|---|---|
| D1 Medicine area | 2,781 (16.6%; 519 journals) | 26,456 (27.1%) |
| D2 D1 without "Medicine (misc.)" | 4,607 (27.5%) | 37,483 (38.5%) |
| D3 broad health sciences | 1,546 (9.2%; 217 journals) | 21,308 (21.9%) |

  Top 20 journals for each definition are listed in the output; the largest is Scientific Reports, which is Multidisciplinary only.
- **Side finding:** the 7,922 "unmatched" records are really three groups: 5,092 titles not in SJR at all, 1,494 titles listed without a quartile, and 1,336 titles that are **Q4**.

## T8 · X5 — Review subtypes

Full output: [outputs/T8_review_subtype.md](outputs/T8_review_subtype.md)

- **The rule** is `analysis/robustness.py::simplify_pubtype_7` (lines 49–68), quoted verbatim in the output. It uses only PubMed Publication Type substrings, in precedence order Editorial > Letter > Systematic Review > Review > Comment > News > Research Article.
- **"Narrative"** is a residual category: it includes **342 records tagged only `Scoping Review`**, which the substring test catches.
- **Meta-Analysis** has no rule of its own. Of 286 meta-analyses, 262 also carry `Systematic Review`, 10 go to narrative Review, and 14 go to Research Article.
- **Table S11 (980 / 4,464) reproduces exactly.**

## T9 · D3, D4a, D5, D1/X2 — Data inventory

Full output: [outputs/T9_data_inventory.md](outputs/T9_data_inventory.md)

- **Dates:**
  - Stored fields: `PubDate/Year` + `Month`, falling back to `MedlineDate`. ArticleDate and Day are not stored.
  - **When the month is missing, the parser fills in "Jan".** January is 16–19% of each year (8.3% expected if months were uniform).
  - Quarterly counts for 2021–2025 range from 232 to 1,791 per quarter.
- **Journals:**
  - No NLM ID or ISSN is stored. ISSN can be recovered from the SJR files.
  - 2,462 journals in the analytic set: median 2 records per journal, 845 journals with a single record, 49 with ≥50.
- **MeSH, keywords and author affiliations:** none are stored, and the raw XML was not saved. Only the first author's first affiliation exists. Getting the rest requires an E-utilities re-fetch.
- **Excluded application records:**
  - 80,733 records, of which 80,268 have a full abstract stored locally (untruncated).
  - Estimated re-run on title + full abstract with Haiku 4.5 via the Batch API: ~63 M input tokens and ~2 M output tokens, about **$37** (standard pricing ~$73). This is a heuristic estimate, not an exact token count; no API call was made.
- **Specialty labels** exist only for the 16,759 retained records (confirmed).

---

## Discrepancy list

Numbers I could not reproduce:

1. **Prefilter κ CI** (Methods): 0.35–0.68 reported vs 0.345–0.646 recomputed (bootstrap, 1000 resamples, seed 42). The original computation is not in the repository.
2. **"Fabrication-involved papers … roughly 21–23% from 2023 onward"** (Abstract, Results R29): the gated share is 15.8% in 2023, then 23.4% / 20.6% / 21.7% in 2024–2026.
3. **Table S9 and Results R46–R47 region n's:**

   | Region | Reported n | Recomputed n |
   |---|---|---|
   | North America | 4,964 | 4,961 |
   | Western Europe | 4,298 | 4,296 |
   | East Asia | 3,262 | 3,260 |
   | Eastern Europe | 330 | 329 |
   | Latin America / Oceania | 753 | 752 |
   | South/Southeast Asia | 785 | 782 |

   The reported n's sum to 16,759, i.e. they count records before the stance-FAILED and 2020 exclusions. The percentages and CIs are computed on the 16,747 records and reproduce.
4. **Commentary critical rate** (Table S10, Results): 56/104 = 53.85%, which rounds to 53.8%. The manuscript's 53.9% is the sum of the rounded Alarm (8.7) and Caution (45.2) values.
5. **Failure-mode κ_max** 0.7549 (reported 0.76) and **model-type AC1** 0.8847 (reported 0.89): both are double-rounding effects.
6. **Table S3 CIs cannot be reproduced by design:** `cv1_within_genre.py` seeds each cell with `42 + hash((genre, year)) % 10000`, and Python salts string hashes per process. The point estimates and ρ do reproduce.
7. **Table S1 P values** are scipy's asymptotic t-approximation for every row except Advocacy, while the Figure 1 caption says "exact two-sided permutation":

   | Row | Table S1 P | Exact permutation P |
   |---|---|---|
   | Alarm, Caution, Critical | .072 | .103 |
   | Neutral | .019 | .033 |
   | Cautious Optimism | .329 | .356 |
   | Advocacy | .003 | .003 (exact) |

   The asterisks in Figure 1a happen to be consistent with the exact P values.
8. **Q1/Q2 share of eligible records:** the manuscript says 88.0%; 98,626/112,011 = 88.05%, and `sjr.log` prints 88.1%.

Places where the code disagrees with the Methods text:

9. **Prefilter API:** Methods says Batch API. In fact the first 2,500 records ran on the synchronous `prefilter.py` (with 3 retries), and only the remaining 94,992 ran through one Message Batch.
10. **Prefilter silent defaults:** 96 records were set to `application` by the failure branch (T1). Methods describes the rule but not the count. Also, `type_confidence` is never `High`, so the stored confidence values carry no information.
11. **Pilot sampling:** Methods does not state the design. The committed `make_pilot.py` (50 per year, 2021–2024, unseeded) does not match the committed pilot file (2021–2026).
12. **SJR "unmatched" includes Q4:** `sjr_filter.py` sends Q4 (1,336 records) and no-quartile titles (1,494) to "unmatched". Methods calls all 7,922 unmatched.
13. **Geography:** Methods says country was resolved by substring lookup (90.3% resolved) and "grouped into eight regions". In the code, regions (Table S9) come from a different resolver, `geography_classifications.csv`, which leaves only 593 records (3.5%) unknown. The country map (Figure 4, Table S7) uses `run_country_critical_map.resolve_country`, which leaves 1,628 unresolved.
14. **Review subtypes:** Methods gives no rule. "Narrative" in the code is any PubMed `Review` (substring match, including Scoping Review) that lacks a `Systematic Review` tag. Meta-analyses without a Systematic Review tag become Research Article (14) or narrative Review (10).
15. **Stance validation pool:** `export_validation.py` drew only from records with a non-empty abstract. Methods says "300 records stratified by assigned stance" without mentioning this.
16. **Human codebook:** `output/validation/coding_instructions.txt` gives the human coder shorter Neutral, Cautious Optimism and Advocacy definitions than the classifier prompt in Supplementary Note 2. For example, the human Advocacy definition does not require transformative language together with minimal caveats. This is flagged for Peter's review only.
17. **Internal doc only:** `METHODS_SOURCE_OF_TRUTH.md` reports 130,181 monthly records and 14,064 duplicates. `fetch.log` and the manuscript both give 129,557 and 13,440.
18. **Generative share for specialty correlations:** computed among abstract-present critical records (this reproduces ρ −0.011). Methods does not state the restriction.
19. **Month field:** missing PubDate months default to "Jan" (`fetch_pubmed_medical.py:180`). This is not described anywhere and matters for any quarterly analysis (D3).

## Checksum confirmation

Pre- and post-run SHA-256 manifests are in `outputs/checksums/`.

- **Worktree `output/` (189 files):** unchanged.
- **Main checkout `output/` (174 files):** unchanged.
- **Figure files outside `output/`:** none exist in the repository, so there was nothing else to check.
- **Tracked files outside `revision_r1/`:** none modified (`git diff 31ed027 -- . ':(exclude)revision_r1'` is empty).

## Commits on `jmir-r1-major-revision` (not pushed)

| Commit | Task |
|---|---|
| `00c286a` | T0 setup, pre-run checksums |
| `7455f48` | T1 prefilter validation |
| `58dddd5` | T2 stance per-class and corrected prevalence |
| `18a945b` | T3 mechanism confusion matrices |
| `23aa829` | T4 temporal 2021–2025 and draft figures |
| `f722159` | T5 claims ledger and cross-sectional (both windows) |
| `efda7bf` | T6 missing-data accounting |
| `c3b803a` | T7 SJR quartile feasibility |
| `3f12412` | T8 review subtypes |
| `6beb33b` | T9 data inventory |
| (final) | Batch 1 report and post-run checksums |

Nothing was pushed. Note that `revision_r1/outputs/` contains PMIDs and titles (Advocacy review list, T7 journal lists). It is committed on this local branch only; keep that in mind before any push.
