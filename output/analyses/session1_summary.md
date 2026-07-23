# Session 1 — secondary analyses with v1/v2 robustness

**Date:** 2026-05-21
**Branch:** `analysis-session-1`
**Canonical classification:** v1 (Sensitivity A, κ=0.789).
**Robustness comparator:** v2 (`classified_medical_Q1Q2_v2_pre_predclaim_fix.csv`, 16,759 rows).
**Bootstrap:** n=1000, seed=42, percentile 95% CI throughout.
**Filter:** dropped 10 FAILED rows from v1 and 4 from v2; restricted to pub_year 2021–2026.

## Executive summary

Three headline findings, all v1-canonical:

1. **Critical stance (Alarm+Caution) rose +7.25 pp**: 25.4% (2021) → 32.6% (2026). Alarm alone tripled (2.7% → 6.8% by 2024). Advocacy collapsed (2.9% → 0.6%, ρ=-1.0). Robust to v2 — every major trend direction holds in v2.
2. **Opinion pieces (Editorial + Commentary + Letter) are markedly more critical than Research Articles** — 41.8% vs 32.9% critical (Δ +8.9 pp). χ²=430.5, p≈7×10⁻⁹². Robust to v2 (same magnitude, p≈1×10⁻⁷⁴).
3. **Thematic shift post-ChatGPT: away from abstract governance, toward concrete LLM operational risks.** Hallucination/errors rose +30.9 pp (23.7 → 54.6%); Patient safety +11.0 pp; Regulation fell -22.0 pp; Replacement fears collapsed monotonically (-3.3 pp, ρ=-1.0).

## Detailed findings

### Finding 1 — Temporal stance trend (v1, 5-stance)

| Stance | 2021 % | 2026 % | Δ (pp) | Spearman ρ | p | v2 direction |
|---|---:|---:|---:|---:|---:|---|
| Alarm | 2.7 | 6.2 | +3.5 | +0.771 | 0.072 | same (+0.771) |
| Caution | 22.7 | 26.4 | +3.8 | +0.771 | 0.072 | same (+0.714) |
| Neutral | 7.3 | 4.3 | -3.0 | -0.886 | 0.019 | same (-0.943) |
| Cautious Optimism | 64.3 | 62.4 | -1.9 | -0.486 | 0.329 | opposite (+0.486) |
| Advocacy | 2.9 | 0.6 | -2.3 | **-1.000** | <0.001 | same (-0.714) |
| **Critical (A+C)** | **25.4** | **32.6** | **+7.25** | +0.771 | 0.072 | same (+0.714) |

**v2 robustness verdict:** 13/30 cells "robust" (<3 pp diff), 17/30 "sensitive" — but the sensitivity is driven entirely by v2's systematic reclassification of borderline cases as Neutral, not by direction flips. All trend directions are preserved except Cautious Optimism (which is flat in both and not statistically significant either way).

Spearman p-values are limited by n=6 yearly observations (minimum p≈0.067 for perfect monotonic). The narrower 95% bootstrap CIs in the per-year per-stance tables are the more powerful statement.

**Caveats:**
- **2026 is partial-year** (Jan–April per upstream brief) — but the file contains 2,691 records dated 2026, which is higher than expected for 4 months. Worth verifying that `pub_year` reflects publication date rather than index date.
- **2024 dip in Alarm** (6.84 → 5.68% in 2025) may be the PubMed publication-lag artefact Dan's earlier notes flagged ("late-2024 papers appear as 2025 in PubMed metadata").

### Finding 2 — Publication-type stratification (v1, 5-bucket)

| Pub type | n (v1) | Alarm % | Caution % | Neutral % | CautOpt % | Advocacy % | Critical % |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research Article | 10,315 | 7.75 | 25.17 | 5.60 | 60.70 | 0.79 | 32.91 |
| Editorial | 404 | 3.22 | 35.15 | 9.41 | 46.04 | 6.19 | 38.37 |
| Review | 5,444 | 1.08 | 23.77 | 2.02 | 71.33 | 1.80 | 24.85 |
| Commentary | 104 | 8.65 | 45.19 | 6.73 | 37.50 | 1.92 | 53.85 |
| Letter | 480 | 7.50 | 34.58 | 21.67 | 30.21 | 6.04 | 42.08 |

**Chi-square (Opinion = Ed+Com+Let vs Research Article, v1):** χ² = 430.5, dof = 4, **p ≈ 7×10⁻⁹²**. Critical: opinion **41.8%** vs research **32.9%** (Δ +8.9 pp).
**Same on v2:** χ² = 350.9, p ≈ 1×10⁻⁷⁴. Critical: opinion **36.2%** vs research **27.6%** (Δ +8.6 pp). **Direction, magnitude, and significance all preserved.**

**Within-opinion ordering:** Commentary (54%) > Letter (42%) > Editorial (38%).
**Reviews are the most positive** corpus (24.9% critical) — evidence-syntheses bias toward "where AI works".
**Commentary n=104 is small** — wide CI; report sample size explicitly.

### Finding 3 — Theme prevalence over time (v1 A+C subset, n=5,161)

| Theme | Overall % | 2021 % | 2026 % | Δ (pp) | Spearman ρ | p |
|---|---:|---:|---:|---:|---:|---:|
| Patient safety | 65.3 | 59.3 | 70.3 | **+11.0** | +0.886 | 0.019 |
| **Hallucination / errors** | 47.5 | 23.7 | 54.6 | **+30.85** | +0.886 | 0.019 |
| Governance / regulation | 36.5 | 54.8 | 32.8 | **-22.01** | -0.886 | 0.019 |
| Ethics & bias | 33.6 | 36.7 | 28.6 | -8.08 | -0.886 | 0.019 |
| Medical education | 8.8 | 3.7 | 9.7 | +5.98 | +0.829 | 0.042 |
| Data privacy | 7.3 | 8.9 | 6.2 | -2.74 | -0.771 | 0.072 |
| Cognitive offloading | 6.1 | 7.8 | 6.7 | -1.06 | -0.086 | 0.872 |
| Existential threat | 5.0 | 6.7 | 5.2 | -1.43 | -0.371 | 0.469 |
| Replacement fears | 3.8 | 6.3 | 3.0 | -3.34 | **-1.000** | <0.001 |
| Other | 2.1 | 4.8 | 1.9 | -2.88 | -0.829 | 0.042 |

**Specific Q&A from the brief:**
- *"Did hallucination rise post-ChatGPT?"* **Yes — emphatically.** From 23.7% to 54.6%, the single largest theme shift.
- *"Did regulation decline?"* **Yes.** Down 22 pp; cleanly anti-correlated with hallucination's rise.

**Interpretation (for discussion):** post-ChatGPT, critical AI discourse in medical journals shifted from speculative-governance framings (regulation, ethics-broadly, replacement, existential) toward **concrete operational concerns about LLM behavior** (hallucination, patient safety). The pivot is sharp and starts in 2023.

**Robustness:** v2 has no thematic classification; **v1-only, robustness not assessed** (per brief).

## Anything unexpected / needing your judgment

1. **2026 record count (2,691) is high for a 4-month partial year.** Worth verifying whether the `pub_year` field is publication date or index date in the upstream pipeline before this number gets reported externally.
2. **Cautious Optimism trend disagrees on direction between v1 and v2** (v1: -0.486, v2: +0.486). Neither is statistically significant, but the disagreement is worth a note in the methods section about v1 vs v2 sensitivity. This is the only direction flip in the whole session.
3. **Spearman power is low at n=6 yearly points** (best possible p≈0.067 for perfect monotonic). For the temporal-stance and theme analyses, quarterly aggregation would give more power if you want narrower significance claims for the Commentary. The bootstrap CIs already give tight per-cell uncertainty (~±0.5 pp on Alarm), which may be sufficient.
4. **Commentary n=104** is the smallest pub-type cell — its 53.9% critical estimate has the widest CI. Worth flagging when this number appears in the Commentary.
5. **The hallucination/regulation antithesis (theme 3 finding) is potentially THE most compelling story** for the Lancet Digital Health Commentary — concrete narrative shift, large effect size, clean statistics, p<0.05 despite small n. Worth highlighting in the abstract.

## Files produced

**Module:**
- [analysis/robustness.py](../../analysis/robustness.py) — reusable loader, bootstrap_ci, dual_analysis, robustness_verdict

**Run scripts:**
- [analysis/run_temporal_stance.py](../../analysis/run_temporal_stance.py)
- [analysis/run_pubtype_stance.py](../../analysis/run_pubtype_stance.py)
- [analysis/run_theme_prevalence.py](../../analysis/run_theme_prevalence.py)

**Figures (300 dpi):**
- [output/figures/temporal_stance.png](../figures/temporal_stance.png)
- [output/figures/pubtype_stance.png](../figures/pubtype_stance.png)
- [output/figures/theme_prevalence.png](../figures/theme_prevalence.png)

**Data:**
- `output/analyses/temporal_stance_v1.csv`, `_v2.csv`, `_robustness.md`, `_trends.csv`
- `output/analyses/pubtype_stance_v1.csv`, `_v2.csv`, `_robustness.md`, `pubtype_chi_square.md`
- `output/analyses/theme_prevalence_v1.csv`, `_trends.csv`, `_summary.md`
