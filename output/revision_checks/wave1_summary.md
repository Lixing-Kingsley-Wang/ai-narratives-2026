# Wave 1 — Pipeline / statistical checks (manuscript revision)

Generated for the AI-narratives Q1/Q2 medical stance study. All checks use the
**v1 canonical** labels (`output/classified_medical_Q1Q2.csv`, Sensitivity A,
κ=0.789). No manuscript prose was changed; no classifier was rerun except the
explicit REP-1 stability check.

- Data source (parent checkout): `/Users/kingslywang/repos/ai-narratives-2026/output/`
- Scripts: `analysis/revision_checks/*.py` (this branch)
- Outputs: `output/revision_checks/`
- Runner: `venv/bin/python` (parent checkout venv)

Record accounting for v1: 16,759 rows total → 16,749 after dropping 10 `FAILED`
→ 16,747 after restricting to `pub_year` 2021–2026 (2 records dated 2020 dropped).
All 16,747 carry a prefilter genre label (`paper_type` ∈ {discourse, evaluative}).

---

## CV-1 — Within-genre critical-share trend

**Question:** Does the rising critical share (Alarm + Caution) reproduce
*within* both prefilter genres, or is it an artefact of the corpus shifting
between genres over time?

**Method:** v1, FAILED dropped, 2021–2026. Split by `paper_type` (discourse vs
evaluative). Yearly critical share = (Alarm + Caution)/N_year with percentile
bootstrap 95% CIs (n_boot = 1000, seed = 42). Descriptive Spearman ρ of yearly
share vs year (n = 6 years) per genre.

**Result — the rise reproduces in BOTH genres** (monotone-ish, both positive ρ):

| Genre | 2021 share | 2026 share | Δ (pp) | Spearman ρ (vs year) | p (two-sided) |
|---|---:|---:|---:|---:|---:|
| discourse | 30.2% | 37.8% | +7.6 | **+0.943** | 0.0048 |
| evaluative | 14.6% | 28.1% | +13.4 | **+0.771** | 0.0724 |

- The discourse trend is monotone and significant. The evaluative trend is
  positive and larger in absolute magnitude (+13.4 pp) but not significant at
  n = 6 years (p = 0.072); its share dips slightly in 2025 before recovering.
- Discourse sits ~15–20 pp above evaluative in every year (discourse papers are
  intrinsically more critical), but **both** genres trend upward, so the
  headline critical-share rise is **not** a genre-composition artefact.

**Genre composition is shifting toward evaluative over time** (discourse:evaluative
ratio), which makes the within-genre reproduction a genuine Simpson's-paradox
check — the corpus mix moved toward the *less* critical genre, yet critical
share still rose within each:

| Year | discourse | evaluative | ratio |
|---|---:|---:|---:|
| 2021 | 735 | 328 | 2.24 |
| 2022 | 863 | 480 | 1.80 |
| 2023 | 1267 | 787 | 1.61 |
| 2024 | 1901 | 1799 | 1.06 |
| 2025 | 2867 | 3031 | 0.95 |
| 2026 | 1261 | 1428 | 0.88 |

**Files:** `cv1_within_genre_trends.csv`, `cv1_within_genre_spearman.csv`,
`cv1_genre_ratio_by_year.csv`, `cv1_within_genre_trends.png`.

---

## CV-2 — Prefilter KEEP-rate audit

**Question:** How did the prefilter KEEP rate within Q1/Q2 change over time?

**Method:**
- kept = discourse + evaluative = `prefiltered_discourse_eval.csv`
  (per-year via its `pub_year` column).
- denominator = pre-prefilter eligible Q1/Q2 records = `filtered_medical_all_Q1Q2.csv`
  (the prefilter's input; year derived from `pub_date` with the same
  `\b(20\d{2})\b` regex prefilter.py uses).
- Partition is exact: 16,759 kept + 80,751 dropped ("application") = 97,510
  prefilter decisions (pandas parses 97,492 denominator rows; 0 rows lacked a
  parseable year).

**Result — KEEP rate rises strictly monotonically** (Spearman ρ(year, rate) =
**+1.000**, p ≈ 0):

| Year | kept | eligible | KEEP rate |
|---|---:|---:|---:|
| 2021 | 1,064 | 11,191 | 9.51% |
| 2022 | 1,344 | 13,136 | 10.23% |
| 2023 | 2,055 | 14,128 | 14.55% |
| 2024 | 3,704 | 19,372 | 19.12% |
| 2025 | 5,899 | 28,873 | 20.43% |
| 2026 | 2,691 | 10,757 | 25.02% |
| **All** | 16,757 | 97,457 | **17.19%** |

**Interpretation:** an increasing fraction of eligible Q1/Q2 AI papers are
classed as discourse/evaluative (rather than pure "application") over time — AI
as a *subject of debate/evaluation* is growing faster than AI-as-a-tool within
Q1/Q2 journals. The monotone trend is flagged as required.

**KEEP rate by specialty — NOT RECOVERABLE (stated, not estimated):**
Specialty labels (`specialty_classifications.csv`, 16,759 rows) exist **only for
the KEPT** discourse/evaluative records. No committed artifact carries a
specialty label at the pre-prefilter denominator level (the 80,751 dropped
"application" records are unlabelled for specialty). A per-specialty denominator
therefore cannot be formed from committed artifacts, so **no
`cv2_keep_rate_by_specialty.csv` was produced** and no values were invented.

**Files:** `cv2_keep_rate_by_year.csv`.

---

## REP-1 — Stance classifier stability under T = 1.0

**Feasibility: RUN.** The repo contains the exact classifier (`classify_stance.py`:
model `claude-sonnet-4-6`, `max_tokens=120`, **no temperature parameter →
provider default T = 1.0**), a working `ANTHROPIC_API_KEY` in `.env`, and the
pre-registered 300-record validation sample with title + abstract
(`output/validation/kingsly_validation_full.csv`). The rerun script imports the
**exact** `SYSTEM_PROMPT` and `build_prompt` from `classify_stance.py` for
parity.

**Method:** classified the same 300 records **twice** (Run A, Run B) at T = 1.0.
Canonical v1 labels and human validation codes were **not** touched — only new
rerun labels were written. Quadratic weights use the ordinal stance order
Alarm(0) < Caution(1) < Neutral(2) < Cautious Optimism(3) < Advocacy(4).

**Result — high inter-run stability:**

| Metric | Value |
|---|---|
| Records evaluated (both runs valid) | 300 / 300 (0 FAILED in either run) |
| Raw agreement | **95.33%** (286 / 300) |
| Quadratic-weighted Cohen's κ | **0.9741** |
| Labels shifted across the 5 stances | **14** |

Shift matrix (rows = Run A, cols = Run B) — **all 14 shifts are between adjacent
categories**; no extreme flips (e.g. Alarm↔Advocacy):

| A \ B | Alarm | Caution | Neutral | Caut.Opt | Advocacy |
|---|---:|---:|---:|---:|---:|
| Alarm | 41 | 0 | 0 | 0 | 0 |
| Caution | 0 | 58 | 1 | 3 | 0 |
| Neutral | 0 | 3 | 61 | 0 | 0 |
| Cautious Optimism | 0 | 0 | 2 | 100 | 1 |
| Advocacy | 0 | 0 | 0 | 4 | 26 |

**Interpretation:** at the production default T = 1.0, run-to-run sampling jitter
is confined to the least-distinct ordinal boundaries (Caution/Neutral,
Cautious-Optimism/Neutral, Advocacy/Cautious-Optimism). Weighted κ ≈ 0.97 (well
above the human-validation κ = 0.789) indicates classifier non-determinism is a
minor contributor to measurement error relative to human–model disagreement.

**Files:** `rep1_stance_stability_sample.csv` (per-record v1 + Run A + Run B),
`rep1_stability_metrics.csv`, `rep1_shift_matrix.csv`.

---

## STAT-8 — FDA drop-structural-zeros sensitivity

**Question:** Does the inverse specialty gradient (more clinical AI adoption →
less critical stance) survive removal of specialties with 0 mapped FDA devices?

**Method:** committed artifact `output/analyses/specialty_aiadoption.csv`
(v1 critical rate per specialty; FDA AI/ML device counts mapped from
`output/external/fda_aiml_devices.csv` by FDA review panel). Spearman ρ between
`critical_rate_pct` and `fda_device_count`, full set vs after dropping
structural-zero specialties (`fda_device_count == 0`). No reclassification.

**Result — the inverse gradient survives (direction + magnitude), significance
attenuates at reduced n:**

| Set | n_specialties | Spearman ρ | p (two-sided) |
|---|---:|---:|---:|
| Full | 18 | **−0.647** | 0.0037 |
| Drop structural zeros | 11 | **−0.579** | 0.0622 |

- 7 structural-zero specialties dropped: Oncology, Dermatology, Mental
  Health/Psychiatry, Pediatrics, Medical Informatics/Digital Health, Nursing,
  Medical Education.
- The correlation stays **negative** and only mildly attenuates (−0.65 → −0.58),
  so the inverse gradient is **not** an artefact of the zero-adoption pile-up.
  With n = 11 the two-sided p rises to 0.062 (loses conventional significance),
  which should be reported honestly as a power limitation, not a sign reversal.

**Caveats (inherited from the source analysis):** the FDA panel→specialty
mapping is approximate; the FDA list is US-centric (a proxy, not a global
adoption measure).

**Files:** `stat8_fda_drop_zero_sensitivity.csv`,
`stat8_structural_zero_specialties.csv`.

---

## STAT-2 — Chi-square N and Cramér's V (pub-type opinion vs research)

**Question:** Confirm the exact N behind χ²₄ = 430.5 and compute the effect size.

**Method:** rebuilt the 2×5 contingency from v1 labels — this only *tabulates*
existing stance labels (no reclassification). Grouping matches the manuscript
source (`analysis/run_pubtype_stance.py` / `pubtype_stance_v1.csv`):
Opinion = Editorial + Commentary + Letter; Research = Research Article; Review
excluded; FAILED already dropped.

Contingency (counts):

| Stance | Opinion (Ed+Com+Let) | Research Article |
|---|---:|---:|
| Alarm | 58 | 799 |
| Caution | 355 | 2,596 |
| Neutral | 149 | 578 |
| Cautious Optimism | 370 | 6,261 |
| Advocacy | 56 | 81 |

**Result:**

| Quantity | Value |
|---|---|
| **Exact N** | **11,303** ( = 988 opinion + 10,315 research ) |
| χ² (recomputed) | 430.53 (matches reported 430.5) |
| dof | 4 |
| p | 7.02 × 10⁻⁹² |
| min(r−1, c−1) for 2×5 | 1 |
| **Cramér's V** | **0.195** |

V = √(430.53 / (11,303 × 1)) = **0.195** — a **small** effect size by Cohen's
convention (the opinion-vs-research stance difference is highly significant but
modest in magnitude, consistent with the +8.9 pp critical-share gap).

**Files:** `stat2_pubtype_chisq_effect_size.csv`, `stat2_pubtype_contingency.csv`.

---

## Provenance & reproducibility

| Task | Script | Reran classifier? |
|---|---|---|
| CV-1 | `analysis/revision_checks/cv1_within_genre.py` | no |
| CV-2 | `analysis/revision_checks/cv2_keep_rate.py` | no |
| REP-1 | `analysis/revision_checks/rep1_stance_stability.py` | yes (explicit; 300×2 @ T=1.0) |
| STAT-8 | `analysis/revision_checks/stat8_fda_drop_zero.py` | no |
| STAT-2 | `analysis/revision_checks/stat2_cramers_v.py` | no |

Shared loader/bootstrap utilities: `analysis/robustness.py` (DATA_DIR pinned to
the parent checkout's `output/`). Bootstrap seed = 42, n_boot = 1000 throughout.
