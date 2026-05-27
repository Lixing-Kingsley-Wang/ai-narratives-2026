# Session 3 — Three drill-downs from manual review of Session 2

**Date:** 2026-05-26
**Branch:** `analysis-session-2` (no separate branch — these are Session 2 follow-ups)
**Canonical classification:** v1 (Sensitivity A, κ=0.789).
**Deferred:** finer-grained specialty taxonomy (Option A + Option C) — to be revisited post-Commentary per the note in `session2_summary.md`.

## Executive summary

Three targeted drill-downs from Kingsley's manual review of Session 2:

1. **Advocacy 2026 vs 2021 collapse anatomy.** 17 surviving 2026 Advocacy records listed. Pub-type, specialty, geography mix shift. Detailed prophecy-panel triage is a separate manual task.
2. **East Asia low critical rate diagnosis.** Composition explains only 8% of the gap. The 92% residual is real regional voice / publication-norm difference. Within-East-Asia anglophone gradient (HK/Singapore > China) hints at conclusion-style norms.
3. **Reviews-positivity mechanism.** Temporal mix rejected (2% explained). Systematic Reviews are MORE critical than narrative Reviews. The mechanism is **theme emphasis**: reviews emphasize regulation/ethics (look up to strategy); research articles emphasize hallucination/concrete failures (look down to operations). The 3 exception specialties (MH, Radiology, Medical Education) confirm the mechanism via sample titles.

Two interpretation briefs written for upstream Opus chat consumption.

---

## Detailed findings

### S3.1 — Advocacy 2026 vs 2021 (n=17 vs n=31)

Full listings in [advocacy_2021_vs_2026.md](advocacy_2021_vs_2026.md) plus per-year record CSVs ([advocacy_2021_records.csv](advocacy_2021_records.csv), [advocacy_2026_records.csv](advocacy_2026_records.csv)). Headline structural shifts:

**Specialty:**

| Specialty | 2021 | 2026 |
|---|---|---|
| Medical Informatics / Digital Health | 12 (39%) | **9 (53%)** |
| Oncology | 5 (16%) | 0 (0%) |
| Surgery | 1 (3%) | 1 (6%) |
| Dermatology | 2 (6%) | 1 (6%) |
| Nursing | 1 (3%) | 1 (6%) |
| Dentistry | 0 | **2 (12%)** |
| Medical Education | 2 (6%) | 0 |
| Pediatrics | 0 | 1 (6%) |
| Internal Medicine | 0 | 1 (6%) |
| Multidisciplinary | 0 | 1 (6%) |
| Radiology | 2 (6%) | 0 |
| Cardiology | 1 (3%) | 0 |
| Neurology | 2 (6%) | 0 |
| Ophthalmology | 1 (3%) | 0 |
| Ob/Gyn | 1 (3%) | 0 |
| Pathology | 1 (3%) | 0 |

**Pub type:**

| Pub type | 2021 | 2026 |
|---|---|---|
| Review | 16 (52%) | **11 (65%)** |
| Research Article | 13 (42%) | 5 (29%) |
| Editorial / Letter | 2 (6%) | 1 (6%) |

**Region:**

| Region | 2021 | 2026 |
|---|---|---|
| North America | 10 (32%) | **9 (53%)** |
| East Asia | 4 (13%) | 4 (24%) |
| Other regions | 17 (55%) | 4 (24%) |

**Predictive claim rate:** 90% (2021) → 94% (2026). Forward-looking is the dominant signature in surviving Advocacy.

**Substantive patterns** (Claude's read; Kingsley to refine for the manuscript):

- **2026 Advocacy is dominated by drug-discovery / pharma-AI papers.** Of the 17: 5 are explicitly drug-discovery (Chemical Society Reviews "AI-powered nanomedicine", Cell systems "enzyme catalysis era of AI", Pharmacological Reviews "AI-driven drug discovery", Drug Development Research "Mathematical and AI Techniques in Modern Drug Discovery", ACS Central Science "From Prompt to Drug: Pharmaceutical Superintelligence"). Plus the Dental Clinics "ProSocial AI" series (n=2) and personalized medicine reviews. The surviving Advocacy is a methodology / drug-discovery / overview enclave.
- **Clinical-specialty Advocacy collapsed entirely.** Oncology (5→0), Cardiology (1→0), Neurology (2→0), Radiology (2→0), Ophthalmology (1→0), Ob/Gyn (1→0), Pathology (1→0). The "AI will transform [organ system]" claim has effectively been retired from clinical literature.
- **Geographic concentration in NA.** 2021 was spread across 8 regions including South/SE Asia (5) and Middle East (4); 2026 narrowed to 5 regions with US-dominated mix (9/17 in North America alone).
- **Pub type shifted toward narrative Reviews** (52% → 65%). Coupled with the H2 finding from S3.3 (narrative reviews are systematically more positive), this is a self-consistent picture: surviving Advocacy lives in the format-and-topic combination most permissive of optimistic framing.

**Interpretation seed** (for Kingsley):

> The Advocacy stance has not disappeared but has narrowed into a methodology / drug-discovery enclave. Clinical-specialty Advocacy — the "AI will transform organ-system X" claim — has effectively been retired. The 2026 Advocacy that remains is a forward-looking, North-America-concentrated, narrative-review-format genre dominated by pharma and personalized-medicine framings. This is consistent with the broader interpretation: medical AI discourse is absorbing AI into its measured-language conventions, while the unambiguous-optimism register migrates upstream to drug discovery (which has its own success vocabulary independent of clinical evaluation).

---

### S3.2 — East Asia low critical rate diagnosis

Full data: [discussion_east_asia.md](discussion_east_asia.md), [east_asia_diagnose_by_specialty.csv](east_asia_diagnose_by_specialty.csv), [east_asia_diagnose_by_country.csv](east_asia_diagnose_by_country.csv).

**Question:** the 18.5% East Asia critical rate (n=3,260) is half the NA+WEU rate (~35%). Three candidate explanations: (a) genuine voice divergence, (b) conclusion-style publication norms, (c) corpus composition (more methodology / less clinical).

**Diagnostic 1 — Within-specialty Δ:** East Asia − (NA+WEU) critical %, per major specialty.

| Specialty | n_EA | n_NA+WEU | EA % crit | NA+WEU % crit | Δ pp |
|---|---:|---:|---:|---:|---:|
| Medical Education | 188 | 507 | 18.1 | 41.0 | **-22.9** |
| Medical Informatics | 746 | 2,561 | 31.4 | 50.2 | **-18.8** |
| Surgery | 173 | 918 | 17.9 | 31.7 | -13.8 |
| Radiology | 568 | 1,188 | 12.2 | 24.7 | -12.5 |
| Ophthalmology | 200 | 353 | 11.0 | 22.9 | -11.9 |
| Oncology | 368 | 743 | 11.7 | 23.1 | -11.5 |
| Dentistry | 131 | 209 | 16.0 | 27.3 | -11.2 |
| Internal Medicine | 264 | 579 | 14.0 | 25.0 | -11.0 |
| Pathology | 91 | 299 | 13.2 | 23.4 | -10.2 |
| Cardiology | 112 | 397 | 15.2 | 18.1 | -3.0 |

**Every major specialty shows a negative Δ.** Even Cardiology (smallest, -3 pp). The gap is structural, not driven by which specialties East Asia publishes in.

**Diagnostic 2 — Per-country within East Asia:**

| Country | n | Critical % (95% CI) |
|---|---:|---|
| Hong Kong | 95 | 31.6 (21.1–41.0) |
| Singapore | 179 | 26.8 (20.7–33.5) |
| Taiwan | 169 | 21.3 (15.4–27.2) |
| South Korea | 487 | 20.3 (16.6–24.2) |
| Japan | 424 | 19.6 (15.8–23.6) |
| **China** | **1,903** | **16.1 (14.5–17.8)** |

A clean anglophone-publishing gradient: Hong Kong (31.6%) and Singapore (26.8%) — both anglophone, both with strong Western publishing acculturation — sit closest to the NA+WEU baseline. China at the other end (16.1%, with n=1,903 driving the regional bucket).

**Diagnostic 3 — Mix-adjustment:** if East Asia's per-specialty critical rates are reweighted by the NA+WEU specialty mix:
- Raw EA: 18.53%
- Mix-adjusted EA: 19.89%
- Raw NA+WEU: 35.10%
- **Composition explains 8% of the 16.57 pp gap. 92% is residual.**

**Conclusion: option (c) corpus composition is rejected. The gap is genuine voice or conclusion-style norm difference.** The HK/Singapore vs China gradient is consistent with (b) — but cannot exclude (a) without outside data on individual paper sentiment in alternative populations.

**Manuscript suggestion (in `discussion_east_asia.md`):** Path 2 — empirically anchored, methodologically honest, opens a research direction. "East Asian publications show a markedly lower critical-stance rate which persists after adjusting for specialty mix. The within-region anglophone-publishing gradient hints at conclusion-style publication norms but cannot exclude genuine voice differences. Future qualitative work is needed."

---

### S3.3 — Why are reviews more positive than research articles?

Full data: [discussion_reviews_positivity.md](discussion_reviews_positivity.md), [reviews_positivity_why.md](reviews_positivity_why.md), [reviews_pubtype_year.csv](reviews_pubtype_year.csv), [reviews_themes.csv](reviews_themes.csv).

**Question:** Session 1 found Reviews 24.85% critical vs Research 32.91% (Δ = -8.06 pp). The "look-up paradox" mentioned by Kingsley — clinicians read reviews more than research articles, so the field's public-facing narrative is more positive than its evaluative substrate. **Why?**

**H1 — Temporal mix (reviews skew earlier, more positive era).** REJECTED.

| year | rev n | rev share | rev crit% | res n | res share | res crit% | Δ pp |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2021 | 448 | 8.2% | 22.77 | 545 | 5.3% | 26.06 | -3.29 |
| 2022 | 517 | 9.5% | 24.56 | 724 | 7.0% | 23.34 | +1.22 |
| 2023 | 684 | 12.6% | 23.83 | 1,151 | 11.2% | 33.19 | -9.36 |
| 2024 | 1,087 | 20.0% | 25.57 | 2,297 | 22.3% | 35.74 | -10.17 |
| 2025 | 1,875 | 34.4% | 24.00 | 3,839 | 37.2% | 33.47 | -9.47 |
| 2026 | 833 | 15.3% | 27.97 | 1,759 | 17.1% | 33.88 | -5.91 |

Reweighting reviews to research's year-mix moves the reviews critical rate by only +0.13 pp. **H1 explains 2% of the 8.06 pp gap.** The gap holds in every year except 2022 (where it's a small +1.22 pp inversion).

**H2 — Sub-pub-type within Review umbrella.** Important inversion of intuition:

| Sub-type | n | Critical % | Alarm % | Caution % | CautOpt % | Advocacy % |
|---|---:|---:|---:|---:|---:|---:|
| Systematic Review | 980 | **29.29** | 3.0 | 26.3 | 68.2 | 0.3 |
| Review (narrative) | 4,464 | **23.88** | 0.7 | 23.2 | 72.0 | **2.1** |

**Systematic Reviews are MORE critical** (+5.4 pp) than narrative Reviews. The Advocacy gap is dramatic — narrative Reviews have 7× the Advocacy rate (2.1% vs 0.3%). **Narrative reviews drive the positivity pattern.** Systematic reviews behave closer to research articles.

**H3 — Theme emphasis (within A+C subset, reviews vs research):**

| theme | rev % | res % | Δ pp |
|---|---:|---:|---:|
| **regulation** | 57.43 | 26.95 | **+30.48** |
| ethics_bias | 43.98 | 29.40 | **+14.58** |
| data_privacy | 10.94 | 6.07 | +4.87 |
| safety_clinical | 65.78 | 64.74 | +1.04 |
| other | 3.25 | 1.74 | +1.51 |
| replacement | 2.66 | 3.86 | -1.20 |
| existential | 3.92 | 5.13 | -1.21 |
| cognitive | 4.43 | 6.57 | -2.13 |
| education | 5.54 | 10.28 | -4.74 |
| **hallucination** | 30.16 | 54.34 | **-24.19** |

**The mechanism is theme emphasis, cleanly.** Reviews emphasize abstract / governance themes (regulation +30.5 pp, ethics +14.6 pp); research articles emphasize concrete-failure themes (hallucination -24.2 pp). **Reviews look up to strategy; research looks down to operations.**

This is the clearest single-finding of S3.3 and arguably the most quotable finding for the Commentary.

**Exception specialties** (MH, Radiology, Medical Education — where reviews are MORE critical than research): sample titles confirm the mechanism:

- **MH reviews** (sample): "Exploring the application boundaries of LLMs in mental health"; "Real concerns, artificial intelligence: Reality testing for psychiatrists"; "From everyday life predictions to suicide prevention: Clinical and ethical considerations in suicide predictive analytic tools"; "Responsible AI integration framework for psychiatric guidelines". → Compile concrete risk evidence, not promise evidence.
- **Radiology reviews** (sample): "Understanding Biases and Disparities in Radiology AI Datasets"; "Implementation of Clinical AI in Radiology: Who Decides and How?"; "Cognitive Bias in Radiological Interpretation Using AI"; "Diagnostic Imaging: collaborative asset or looming replacement?" → Mature field; reviews acknowledge deployment friction and dataset issues openly.
- **Medical Education reviews** (sample): "Harnessing LLMs in medical education: promise and pitfalls"; "Twelve tips for addressing ethical concerns"; "Academic integrity and AI: is ChatGPT hype, hero or heresy?"; "Impact of generative AI on health professional education". → Critique-of-pedagogy, not promise-of-pedagogy.

**Synthesis for the Commentary (in `discussion_reviews_positivity.md`):** "The accessibility paradox" — reviews are the highest-readership format and the most positive register. The field's public-facing narrative is therefore disproportionately optimistic compared to the evaluative work underneath. The mechanism is **theme emphasis** (reviews look up to regulation/ethics; research articles look down to hallucination/safety) plus **narrative-review selection bias** (narrative reviews are more positive than systematic reviews by 5.4 pp).

---

## Files produced this session

**Scripts:**
- [analysis/run_advocacy_2021_vs_2026.py](../../analysis/run_advocacy_2021_vs_2026.py)
- [analysis/run_east_asia_diagnose.py](../../analysis/run_east_asia_diagnose.py)
- [analysis/run_reviews_positivity_why.py](../../analysis/run_reviews_positivity_why.py)

**Data:**
- `output/analyses/advocacy_2021_vs_2026.md`
- `output/analyses/advocacy_2021_records.csv`, `advocacy_2026_records.csv`
- `output/analyses/east_asia_diagnose_by_specialty.csv`
- `output/analyses/east_asia_diagnose_by_country.csv`
- `output/analyses/reviews_pubtype_year.csv`
- `output/analyses/reviews_themes.csv`
- `output/analyses/reviews_positivity_why.md`

**Discussion briefs (for upstream Opus chat):**
- `output/analyses/discussion_east_asia.md`
- `output/analyses/discussion_reviews_positivity.md`

---

## Anything unexpected / for Kingsley to note

1. **Systematic Reviews are MORE critical than narrative Reviews.** Inversion of intuition. Worth a sentence in the manuscript Methods or Discussion about how sub-pub-type matters.

2. **Drug-discovery is the surviving Advocacy beach-head.** 5 of 17 surviving 2026 Advocacy records are pharma-AI / drug-discovery reviews. Not a fluke — drug discovery has its own success vocabulary (binding affinity prediction, ADMET, in silico screening) that lets confident claims persist where clinical evaluation has retired them. Mentioning in passing in the Commentary differentiates "AI in medicine" from "AI in drug discovery" and is more honest.

3. **The HK/Singapore-vs-China gradient within East Asia.** Not just a Western-vs-East story. Anglophone publishing acculturation seems to track critical-rate. Worth a sentence in the East Asia limitations paragraph.

4. **The "look up vs look down" theme finding is publication-quality.** +30.5 pp regulation in reviews vs +24.2 pp hallucination in research is a strikingly clean differential. Strong candidate for a Commentary figure.

5. **Finer-grained taxonomy is still deferred per the note in session2_summary.md** (Option A + Option C combined, post-Commentary).

---

## Where Session 3 leaves the project

- Sessions 1, 2, 2.5 (Q3 fixup), 3 complete. All analyses on the manuscript critical path are done.
- Kingsley's manual to-do (no Claude session needed):
  - Synthesize Session 1, 2, 2.5, 3 summaries upstream with Opus 4.7
  - Prophecy panel triage on 92 candidates in `prophecy_panel_candidates_2021_2023.csv`
  - Title curation (your own scheme)
- Likely next Claude session: manuscript drafting (abstract + main text + figure captions) for Lancet Digital Health Commentary, target mid-Aug 2026.
- Optional post-Commentary Claude session: finer-grained taxonomy (Option A + C) for a longer follow-up paper.
