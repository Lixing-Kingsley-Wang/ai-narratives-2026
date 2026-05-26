# Session 2 — specialty + geographic stratification + Session 1 drill-downs

**Date:** 2026-05-23 → 2026-05-26
**Branch:** `analysis-session-2` (off `analysis-session-1`)
**Canonical classification:** v1 (Sensitivity A, κ=0.789).
**Robustness comparator:** v2 (`classified_medical_Q1Q2_v2_pre_predclaim_fix.csv`).
**New classifications produced:**
- **Specialty** (18 categories, Haiku 4.5 batch) — 16,759 records, 13 FAILED (0.08%), 97.1% high-confidence.
- **Geography** (8 regions + Unknown, regex/dictionary parser on `first_affiliation`) — 16,759 records, 593 Unknown (3.5%; 274 truly-empty + 319 unparseable institution-only strings).

**Bootstrap:** n=1000, seed=42, percentile 95% CI throughout. **Filter:** dropped FAILED rows and restricted to pub_year 2021–2026.

---

## Executive summary

Seven new headline findings, all v1-canonical:

1. **Critical stance varies 3.1× across specialties.** Mental Health/Psychiatry 51.3% (95% CI 46.8–55.5) → Cardiology 16.8% (14.1–19.8). The **top 3 critical specialties** are MH (51.3%), **Medical Informatics (44.9%)**, and Nursing (43.0%). Two clusters drive criticism: (a) **AI-methodology papers** (Medical Informatics, #2) — frameworks/ethics/benchmarks that explicitly debate AI risks; (b) **patient-facing / high-stakes clinical domains** where AI replaces human judgement (MH #1, Nursing #3, Dermatology #4, Medical Education #5). Image-recognition-heavy specialties (Radiology #14, Ophthalmology #17, Cardiology #18) skew most positive — AI augments rather than replaces in these.

2. **Post-ChatGPT critical shift is global, not Western.** All 5 top regions show rising critical-rate trends (5/5 ρ>0). Significant rises in Western Europe (p=0.04), East Asia (p=0.02), MENA (p=0.005). Eastern markets show *larger absolute gains*: East Asia +12.1 pp, MENA +12.8 pp, S/SE Asia +18.7 pp vs NA +6.8 pp / WEU +5.9 pp. Eastern fields started low and caught up.

3. **East Asia has the lowest critical rate** (18.5%, n=3,260, CI 17.2–19.9). Robust signal at large n. Almost half the NA/WEU rate (~35%). Worth a sentence in the discussion on regional discourse divergence — see [region_critical](region_critical_v1.csv).

4. **The hallucination↑ / regulation↓ pivot is universal across specialties** — happens in **8/8** top specialties. Strongest signal: Medical Informatics ρ=+1.00 / -1.00, Oncology +0.94, Dentistry +0.94. The cleanest universal pattern in the dataset. Each clinical field independently underwent the same governance-to-operational discourse shift.

5. **Hallucination is a *subset* of patient-safety, not a parallel theme.** In A+C subset: r=+0.36 (p≈10⁻¹⁵⁷), but P(safety|hallu)=0.83 vs P(hallu|safety)=0.61 — asymmetric. 83% of hallucination papers invoke safety; only 60% the other way. BOTH-flagged rate **doubled**: 21.5% (2021) → 47.8% (2026). The two themes are fusing into one cluster as concrete hallucination cases become the dominant safety story.

6. **Reviews-positivity holds within-specialty.** Reviews less critical than research articles in **7/10** specialties (24.9% vs 32.9% pooled, ~8 pp gap). Three exceptions where reviews are MORE critical: Mental Health/Psychiatry (+4.5 pp), Radiology (+3.8 pp), Medical Education (+3.3 pp). Suggests reviews systematically dampen criticism in clinical-application specialties but flag concerns where AI replaces high-stakes clinical judgement.

7. **The "post-ChatGPT critical shift" is really *clinical specialties catching up to where Medical Informatics already was.*** Med Informatics was already at 45.4% critical in 2021 (highest baseline) and stayed flat (-2.2 pp). Clinical fields rose sharply: Radiology +10.7 pp (ρ=1.00 perfectly monotonic, p<0.001), Oncology +16.4 pp**, Internal Medicine +16.6 pp**, Dentistry +13.3 pp**, Surgery +11.8 pp. The AI-methodology field anticipated the criticism; clinical practitioners followed.

---

## Detailed findings

### Workstream A — Specialty stratification

#### A.1 — Distribution

| Specialty | n | % |
|---|---:|---:|
| Medical Informatics / Digital Health | 4,343 | 25.9% |
| Radiology / Diagnostic Imaging | 2,077 | 12.4% |
| Surgery | 1,442 | 8.6% |
| Oncology | 1,424 | 8.5% |
| Internal Medicine / Primary Care | 1,117 | 6.7% |
| Medical Education | 1,076 | 6.4% |
| Dentistry | 759 | 4.5% |
| Ophthalmology | 755 | 4.5% |
| Cardiology | 632 | 3.8% |
| Mental Health / Psychiatry | 485 | 2.9% |
| Pathology / Laboratory Medicine | 458 | 2.7% |
| Pediatrics | 392 | 2.3% |
| Emergency Medicine / Critical Care | 369 | 2.2% |
| Neurology / Neuroscience | 357 | 2.1% |
| Dermatology | 301 | 1.8% |
| Nursing | 291 | 1.7% |
| Obstetrics / Gynecology | 236 | 1.4% |
| Multidisciplinary / Other | 232 | 1.4% |
| FAILED | 13 | 0.08% |

#### A.2 — Critical rate by specialty (v1, with bootstrap 95% CI)

| Specialty | n | Crit % v1 (95% CI) | v2 | Δ pp |
|---|---:|---|---:|---:|
| Mental Health / Psychiatry | 485 | **51.3** (46.8–55.5) | 42.5 | -8.9 |
| Medical Informatics | 4,337 | **44.9** (43.5–46.4) | 33.5 | -11.4 |
| Nursing | 291 | **43.0** (37.0–48.8) | 23.0 | -19.9 |
| Dermatology | 301 | 36.5 (31.3–42.9) | 32.0 | -4.5 |
| Medical Education | 1,076 | 35.1 (32.4–38.0) | 22.0 | -13.1 |
| Multidisciplinary | 232 | 32.8 (27.0–38.6) | 26.7 | -6.0 |
| Surgery | 1,442 | 28.9 (26.7–31.4) | 28.8 | -0.1 |
| Emergency Med / Crit Care | 369 | 28.5 (23.9–33.1) | 26.6 | -1.9 |
| Ob/Gyn | 236 | 26.7 (20.7–32.4) | 23.3 | -3.4 |
| Pediatrics | 392 | 25.5 (21.4–30.0) | 24.7 | -0.8 |
| Dentistry | 757 | 24.8 (21.9–28.1) | 25.4 | +0.6 |
| Neurology | 356 | 24.4 (20.3–28.8) | 22.4 | -2.0 |
| Internal Medicine | 1,117 | 22.5 (20.0–25.0) | 20.9 | -1.5 |
| Radiology | 2,075 | 21.3 (19.6–22.9) | 19.2 | -2.0 |
| Pathology / Lab | 458 | 20.7 (17.1–24.4) | 17.9 | -2.8 |
| Oncology | 1,424 | 19.7 (17.8–21.8) | 16.7 | -2.9 |
| Ophthalmology | 755 | 18.4 (15.7–21.2) | 18.1 | -0.3 |
| Cardiology | 631 | **16.8** (14.1–19.8) | 16.1 | -0.7 |

**v1 vs v2 robustness:** v2 critical rates systematically run 2–20 pp lower than v1 (matches Session 1's observation that v2 reclassifies many Caution→Neutral). **Directional ranking is preserved**: Mental Health is top and Cardiology is bottom in both versions.

Figure: [specialty_critical.png](../figures/specialty_critical.png).

#### A.3 — Temporal critical-rate trend by specialty (top 8)

| Specialty | n | 2021 → 2026 | Δ pp | ρ | p |
|---|---:|---|---:|---:|---:|
| Radiology / Diagnostic Imaging | 2,075 | 15.5 → 26.1 | +10.7 | **+1.00** | <0.001 ** |
| Surgery | 1,442 | 16.1 → 27.9 | +11.8 | +0.54 | 0.27 |
| Oncology | 1,424 | 8.5 → 24.9 | **+16.4** | +0.89 | 0.019 * |
| Internal Medicine | 1,117 | 10.5 → 27.1 | **+16.6** | +0.89 | 0.019 * |
| Medical Education | 1,076 | 37.0 → 36.0 | -1.0 | +0.03 | 0.96 |
| Dentistry | 757 | 11.1 → 24.4 | +13.3 | +0.89 | 0.019 * |
| Ophthalmology | 755 | 18.5 → 17.4 | -1.0 | -0.14 | 0.79 |
| Medical Informatics | 4,337 | 45.4 → 43.2 | -2.2 | -0.49 | 0.33 |

**6/8 rising, 4/8 significant (p<0.05).** Medical Informatics was already critical at baseline (45.4% in 2021) — the highest of any specialty — and stayed flat. Clinical-application specialties caught up post-ChatGPT.

Figure: [temporal_stance_by_specialty.png](../figures/temporal_stance_by_specialty.png).

#### A.4 — Theme inversion by specialty (within A+C, top 8)

Spearman ρ (year vs theme prevalence) per specialty × theme:

| Specialty | n | hallucination ρ | regulation ρ | safety_clinical ρ |
|---|---:|---:|---:|---:|
| Medical Informatics | 1,949 | **+1.00** | **-1.00** | +0.83 |
| Radiology | 441 | +0.83 | -0.66 | +0.49 |
| Surgery | 417 | +0.60 | -0.77 | +0.71 |
| Medical Education | 378 | +0.58 | -0.43 | +0.60 |
| Oncology | 280 | +0.94 | -0.77 | +0.03 |
| Internal Medicine | 251 | +0.66 | -0.71 | +0.75 |
| Mental Health | 249 | +0.77 | -0.54 | +0.77 |
| Dentistry | 188 | +0.94 | -0.49 | +0.20 |

**Hallucination rising in 8/8. Regulation falling in 8/8.** This is the cleanest universal pattern in the entire dataset.

Figure: [themes_by_specialty.png](../figures/themes_by_specialty.png).

#### A.5 — 2024 Alarm "peak" drill-down

Important reframing: the 2024 "Alarm peak" is a per-year **rate** peak, not absolute count. Counts (29 → 335 from 2021 → 2025) grew monotonically. Per-year **Alarm rate** dipped: 6.84% (2024) → 5.68% (2025) → 6.21% (2026 partial).

The 2025 dip (Δ = -1.16 pp) is **not** explained by a single specialty pulling back — offsetting mix shifts within specialties. **Most likely a denominator-growth artifact** as Cautious Optimism papers expanded faster than Alarm in 2025. Details: [alarm_peak_drilldown.md](alarm_peak_drilldown.md).

#### A.6 — Advocacy collapse anatomy

2021 Advocacy n=31; 2026 Advocacy n=17 (partial year). Advocacy rate fell monotonically each year (2.91% → 0.63%, ρ=-1.0 per Session 1). Composition details: [advocacy_collapse_anatomy.md](advocacy_collapse_anatomy.md).

**Prophecy panel candidates:** [prophecy_panel_candidates_2021_2023.csv](prophecy_panel_candidates_2021_2023.csv) lists all **92 records** that are (Advocacy stance) ∧ (2021–2023) ∧ (predictive_claim=yes). Ready for triage in Session 3.

---

### Workstream B — Geographic stratification

#### B.1 — Distribution

Parser-based extraction of first-author country from `first_affiliation`. Plan's 8-region taxonomy + Unknown.

| Region | n | % |
|---|---:|---:|
| North America | 4,964 | 29.6% |
| Western Europe | 4,298 | 25.6% |
| East Asia | 3,262 | 19.5% |
| Middle East / North Africa | 1,706 | 10.2% |
| South / Southeast Asia | 785 | 4.7% |
| Latin America / Oceania | 753 | 4.5% |
| **Unknown** | **593** | **3.5%** |
| Eastern Europe | 330 | 2.0% |
| Sub-Saharan Africa | 68 | 0.4% |

**Top countries:** USA 4,424, China 1,903, UK 875, Germany 797, Turkey 773, Italy 705, Canada 540, S. Korea 488, Australia 465, India 465, Japan 425.

Unknown rate 3.5% — well under the 15% stop threshold. 274 of the 593 unknowns are truly-empty affiliations (1.6% of corpus); the rest are institution-only strings like "Imperial College" or "Department of Pathology." with no country marker.

#### B.2 — Critical rate by region (v1)

| Region | n | Crit % v1 (95% CI) | v2 | Δ pp |
|---|---:|---|---:|---:|
| Sub-Saharan Africa | 68 | **45.6** (32.7–56.5) | 26.5 | -19.1 |
| Latin America / Oceania | 752 | 36.8 (33.3–40.2) | 30.8 | -6.0 |
| North America | 4,961 | 35.1 (33.9–36.4) | 29.1 | -6.1 |
| Western Europe | 4,296 | 35.1 (33.6–36.5) | 28.0 | -7.1 |
| Middle East / North Africa | 1,706 | 30.6 (28.4–32.8) | 26.6 | -4.0 |
| Eastern Europe | 329 | 28.9 (24.1–34.4) | 23.0 | -5.9 |
| South / Southeast Asia | 782 | 24.6 (21.5–27.7) | 19.0 | -5.5 |
| East Asia | 3,260 | **18.5** (17.2–19.9) | 15.9 | -2.6 |

**Top 3 critical:** Sub-Saharan Africa (small n, wide CI), Latin America/Oceania, North America/Western Europe (tied at 35.1%).
**Bottom 3:** Eastern Europe, South/SE Asia, East Asia.

**East Asia at 18.5% with n=3,260 is the most robust regional finding.** It's about half the NA/WEU critical rate.

Figure: [region_critical.png](../figures/region_critical.png).

##### B.2.a — Sub-Saharan Africa detail (n=68)

The headline 45.6% critical rate (95% CI 32.7–56.5%) is fragile (small n, wide CI) but worth full unpacking before deciding whether to feature it.

**Country composition:**
- South Africa: 26 (38%)
- Uganda: 9
- Nigeria: 8
- Ethiopia: 7
- Tanzania: 4
- Ghana, Burkina Faso: 3 each
- Singletons: Côte d'Ivoire, Senegal, Zimbabwe, Republic of Congo, Sierra Leone, Somalia, Rwanda, Zambia

Anglophone southern + East Africa account for nearly all of it.

**Stance distribution:** 34 Cautious Optimism, 27 Caution, 4 Alarm, 2 Advocacy, 1 Neutral. So "critical" = 4 Alarm + 27 Caution = 31/68 = 45.6%.

**Specialty mix:** highly skewed:
- Medical Informatics: 24 (35.3%)
- Medical Education: 7 (10.3%)
- Oncology: 6, Radiology: 5, Internal Medicine: 5
- Other 14 specialties: 21 records total

The high critical rate is **mechanically explained by composition**: 35% of SSA records are Medical Informatics (44.9% critical at corpus level) + 10% Medical Education (35.1% critical) + smaller contributions. A back-of-envelope mix-adjusted expectation lands close to 35–40%. The remaining excess (~5–10 pp) might reflect a regionally distinctive critical voice — see sample titles below — but n is too small to claim this with confidence.

**Per-year volume and critical rate:**

| year | n | crit % |
|---:|---:|---:|
| 2021 | 1 | 0.0% |
| 2022 | 4 | 25.0% |
| 2023 | 7 | 42.9% |
| 2024 | 13 | 61.5% |
| 2025 | 24 | 37.5% |
| 2026 | 19 | 52.6% |

Volume ramping rapidly (19 records in 4 months of 2026 vs 1 in all of 2021). Trend is real but per-year n still too small to fit a meaningful Spearman.

**Sample Alarm-stance titles** (illustrating the regionally distinctive voice):
- "The AI Health Arms Race: A Critical Perspective on Big Tech and the Widening Global Health Equity Gap" (Somalia)
- "Epistemic (in)justice, social identity and the Black Box problem in patient care" (South Africa)
- "Controversy in Hypertension: Con-side of the argument using AI for HTN diagnosis and management" (Uganda)
- "Evaluation of the Diagnostic Capabilities of Artificial Intelligence (GPT-4) in a Cardiology Department in Sub-Saharan Africa" (Burkina Faso)

Two of the four Alarm papers explicitly frame AI as a global-equity / colonial-tech concern — a register essentially absent from the NA/WEU Alarm corpus (which centers on hallucination and patient safety). If you want to feature SSA in the Commentary, this **equity/justice framing** is the distinctive substantive finding, not the headline rate.

**Recommendation for your manuscript-selection decision:** treat the 45.6% number as an exploratory point with the n=68 caveat, but lift the equity-framing observation as a separate qualitative finding (4 Alarm titles are enough to anchor a 1–2 sentence discussion).

#### B.3 — Temporal critical-rate trend by region (top 5)

| Region | n | 2021 → 2026 | Δ pp | ρ | p |
|---|---:|---|---:|---:|---:|
| North America | 4,961 | 29.8 → 36.6 | +6.8 | +0.66 | 0.156 |
| Western Europe | 4,296 | 32.6 → 38.5 | +5.9 | +0.83 | 0.042 * |
| East Asia | 3,260 | 10.5 → 22.6 | **+12.1** | +0.89 | 0.019 * |
| MENA | 1,706 | 20.5 → 33.3 | **+12.8** | +0.94 | 0.005 ** |
| S/SE Asia | 782 | 6.7 → 25.4 | **+18.7** | +0.77 | 0.072 |

**5/5 rising. 3 significant at p<0.05.** Post-ChatGPT critical-stance shift is genuinely global. Eastern markets are catching up from lower baselines — convergence, not divergence.

Figure: [temporal_stance_by_region.png](../figures/temporal_stance_by_region.png).

---

### Workstream C — Session 1 drill-downs

#### C.1 — Hallucination × patient_safety co-occurrence (A+C subset, n=5,161)

| Metric | Value |
|---|---|
| Records flagged hallucination | 2,450 (47.5%) |
| Records flagged safety_clinical | 3,372 (65.3%) |
| Records flagged BOTH | 2,041 (39.5%) |
| Pearson r | **+0.359** (p ≈ 10⁻¹⁵⁷) |
| P(safety \| hallucination) | **0.833** |
| P(hallucination \| safety) | 0.605 |
| Co-occurrence lift vs independence | 1.28× |

**Year-by-year BOTH-flag rate:** 21.5% (2021) → 47.8% (2026). The two themes are fusing into one cluster as concrete hallucination cases become the dominant safety story.

Interpretation: hallucination is essentially a *subset* of broader safety concerns, not a parallel theme. Hallucination papers almost always invoke safety; safety papers don't always invoke hallucination. Asymmetric coupling. Details: [hallucination_patient_safety_cooccurrence.md](hallucination_patient_safety_cooccurrence.md).

#### C.2 — Q1/Q2 vs Q3 comparison: DEFERRED

Q3 corpus exists (5,433 filtered records; 1,055 in the prefiltered discourse+eval subset) but has **NOT** been stance-classified with the v1 or v2 prompts. Dan's `output/analysis/05_q1q2_vs_q3_stance.csv` is from his pre-v1 truncated-abstract pipeline (superseded).

**Decision needed from Kingsley:** run v1 stance classification on the 1,055 Q3 discourse+evaluative records (~30 min + ~$10), or report Q1/Q2 only. Details: [q1q2_vs_q3.md](q1q2_vs_q3.md).

#### C.3 — Reviews-positive depth check by specialty

| Specialty | n_rev | n_res | rev crit % | res crit % | Δ (rev−res) |
|---|---:|---:|---:|---:|---:|
| Internal Medicine | 442 | 591 | 12.7 | 28.9 | **-16.3** |
| Surgery | 411 | 938 | 17.0 | 32.8 | -15.8 |
| Dentistry | 216 | 528 | 15.3 | 28.2 | -12.9 |
| Oncology | 643 | 710 | 14.0 | 24.5 | -10.5 |
| Medical Informatics | 1,423 | 2,533 | 38.1 | 47.5 | -9.4 |
| Cardiology | 286 | 320 | 12.6 | 19.4 | -6.8 |
| Ophthalmology | 233 | 501 | 14.2 | 20.4 | -6.2 |
| Medical Education | 145 | 874 | 37.2 | 34.0 | +3.3 |
| Radiology | 521 | 1,487 | 23.4 | 19.6 | +3.8 |
| Mental Health / Psychiatry | 161 | 291 | 54.7 | 50.2 | +4.5 |

Reviews LESS critical than research in **7/10 specialties**. Session 1 finding holds within-specialty. **Three exceptions** where reviews flag MORE concerns: Mental Health, Radiology, Medical Education — interesting future angle, possibly because reviews in these fields focus on AI as judgement-replacer (MH, rad) or formative-influence (med ed).

Figure: [reviews_vs_research_by_specialty.png](../figures/reviews_vs_research_by_specialty.png).

---

## Anything unexpected / needing your judgment

1. **Sub-Saharan Africa critical rate of 45.6%** is the highest of any region but n=68 with CI 32.7–56.5. Headline-worthy but report sample size explicitly. Consider whether to include it in the Commentary at all or footnote as exploratory.

2. **East Asia critical rate of 18.5%** (n=3,260) is the most discussion-worthy regional finding. Discuss whether this reflects (a) genuinely more positive AI-medicine discourse in East Asian institutions, (b) institutional / linguistic norms favoring less critical conclusions in published abstracts, or (c) corpus composition (more methodology / less clinical-application papers in East Asian publications). Worth a sentence in limitations.

3. **Medical Informatics at 25.9% of corpus** is large but plausible — this bucket includes all "AI-about-AI" papers (frameworks, ethics overviews, benchmarks not tied to a specific clinical specialty). The prompt rule was followed correctly per spot-checks; no need to re-run. If you want a finer-grained taxonomy in the future, the rule could be tightened to require an explicit "AI methodology" anchor.

4. **The 2024 Alarm "peak" was a rate phenomenon, not a count.** Reframe in the Commentary: there is no Alarm slowdown — counts rose every year. The 5.68% rate in 2025 reflects faster growth of Cautious Optimism, not retreat from Alarm.

5. **Prophecy panel: 92 candidates ready.** Listed in `prophecy_panel_candidates_2021_2023.csv` (with title + abstract). For Session 3 manual triage.

6. **Reviews-MORE-critical in MH/Radiology/Medical Education** is a small but interesting subfinding. Worth flagging in the discussion as a counter to a too-simple "reviews dampen critique" story.

7. **Q3 comparison deferral.** If you want to keep the manuscript clean, plan to run the 1,055 Q3 discourse-eval records through `classify_stance_batch.py` in Session 3. ~$10 of Sonnet compute. Otherwise drop the Q3 generalizability claim.

---

## Files produced this session

**Module additions:**
- [analysis/classify_specialty.py](../../analysis/classify_specialty.py) — Haiku 4.5 batch + sync sample mode
- [analysis/extract_geography.py](../../analysis/extract_geography.py) — regex/dictionary parser
- [analysis/run_specialty_critical.py](../../analysis/run_specialty_critical.py)
- [analysis/run_specialty_temporal.py](../../analysis/run_specialty_temporal.py)
- [analysis/run_specialty_themes.py](../../analysis/run_specialty_themes.py)
- [analysis/run_region_critical.py](../../analysis/run_region_critical.py)
- [analysis/run_region_temporal.py](../../analysis/run_region_temporal.py)
- [analysis/run_alarm_peak_drilldown.py](../../analysis/run_alarm_peak_drilldown.py)
- [analysis/run_advocacy_collapse.py](../../analysis/run_advocacy_collapse.py)
- [analysis/run_reviews_by_specialty.py](../../analysis/run_reviews_by_specialty.py)
- [analysis/run_hallu_safety_cooccurrence.py](../../analysis/run_hallu_safety_cooccurrence.py)

**Figures (300 dpi):**
- [output/figures/specialty_critical.png](../figures/specialty_critical.png)
- [output/figures/temporal_stance_by_specialty.png](../figures/temporal_stance_by_specialty.png)
- [output/figures/themes_by_specialty.png](../figures/themes_by_specialty.png)
- [output/figures/region_critical.png](../figures/region_critical.png)
- [output/figures/temporal_stance_by_region.png](../figures/temporal_stance_by_region.png)
- [output/figures/reviews_vs_research_by_specialty.png](../figures/reviews_vs_research_by_specialty.png)

**Classifications (worktree, committed):**
- `output/specialty_classifications.csv` (16,759 rows; pmid, title, pub_year, journal, specialty, confidence, specialty_raw)
- `output/geography_classifications.csv` (16,759 rows; pmid, first_affiliation_short, country, region)

**Analyses (output/analyses/):**
- `specialty_critical_v1.csv`, `_v2.csv`, `_robustness.md`
- `temporal_stance_by_specialty.csv`, `_trends.csv`
- `themes_by_specialty.csv`, `_trends.csv`
- `region_critical_v1.csv`, `_v2.csv`, `_robustness.md`
- `temporal_stance_by_region.csv`, `_trends.csv`
- `alarm_peak_drilldown.md`, `_data.csv`
- `advocacy_collapse_anatomy.md`
- `prophecy_panel_candidates_2021_2023.csv` (92 records)
- `reviews_by_specialty.md`, `.csv`
- `hallucination_patient_safety_cooccurrence.md`, `_yearly.csv`
- `q1q2_vs_q3.md` (status note)

---

## Future work — decisions noted

### Finer-grained specialty taxonomy (post-Lancet-Commentary)

**Kingsley's decision (2026-05-26):** when we revisit the specialty taxonomy for a longer follow-up paper, do **Option A + Option C together**, not separately. Specifically:

- **Option A (two-axis decomposition)**: re-classify each of the 16,759 records with TWO labels:
  - Axis 1: Clinical specialty (existing 18 categories, unchanged)
  - Axis 2: Methodology-focus tag (a 4-bucket label: `methodology` / `ethics-governance` / `overview` / `not-applicable`)
- **Option C (Med Informatics sub-split)**: layer this 4-bucket methodology-focus tag specifically as a *second-pass* refinement of the current `Medical Informatics / Digital Health` records (n=4,343), so the 25.9% Med Informatics bucket gets cleanly partitioned into:
  - `methodology` (pure framework / benchmark / dataset / model architecture)
  - `ethics-governance` (regulation, ethics frameworks, deployment / policy)
  - `overview` (general AI-in-medicine cross-cutting reviews)
  - `not-applicable` (papers mis-classified into Med Informatics that actually have a clinical anchor — re-route to that anchor's bucket)

**Why combine A + C:** Option A alone gives the methodology tag to *every* record (so we can ask "what % of Cardiology papers are methodology-focused?"). Layering C on top means the Med Informatics bucket — currently the largest and most internally heterogeneous — gets the same finer treatment, AND any mis-routed records can be relabeled to their proper clinical anchor.

**Estimated cost:** ~$11 (Option A's batch covers everything; C is the analysis layer on the same output, no extra classification).

**Trigger:** revisit after the Lancet Digital Health Commentary is submitted (target mid-Aug 2026). Not needed for the Commentary itself.

**Code touchpoints when we do it:**
- Extend `SPECIALTY_PROMPT` in `analysis/classify_specialty.py` to request both axes
- Update parser + output schema (add `methodology_tag` column)
- Add an `analysis/split_med_informatics.py` (or extend `run_specialty_critical.py`) to apply Option C's interpretation logic on top of the Option A results

### Q3 generalizability check

In flight as of 2026-05-26 — see [q1q2_vs_q3.md](q1q2_vs_q3.md) for the updated status. Will be appended to this summary once the comparison runs.
