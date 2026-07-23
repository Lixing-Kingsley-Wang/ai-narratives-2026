# Q7 — Gate-independent re-measurement: failure_mode × model_type

**Session 5 (analysis-session-5).** Classifier `q7_failuremode_v1`, model
`claude-sonnet-4-6`, temperature 0. Scope: critical papers only (stance ∈
{Alarm, Caution}), **n = 5,161** (916 Alarm + 4,245 Caution); 2 FAILED dropped →
**n = 5,159** for analysis. Each paper scored on two independent axes from the
**mechanism described**, not from whether brand names (GPT/ChatGPT) appear:

- **failure_mode** ∈ {confabulation, misclassification, both, none_or_unclear}
- **model_type** ∈ {generative, discriminative, both, unclear}

Conventions: v1 canonical, FAILED dropped, pub_year 2021–2026, seed = 42,
bootstrap n = 1,000 percentile 95% CI (reused `robustness.bootstrap_ci`).

---

## Headline (lead findings)

1. **The old "hallucination" theme gate is heterogeneous and its rise is partly a
   composition shift, not pure growth in fabrication concern.** Inside the gated
   set (2,226 papers, abstract-present), **misclassification is the majority every
   single year** (70–90% pre-2023, still 56–77% post-2023). Confabulation-involved
   papers are 0–2% of the gate in 2021–22 and rise to only ~21–23% from 2023 on.
   So the ~+30 pp rise of the "hallucination" theme across sessions 1–3 is
   **partly a shift in what the gate is made of** (more genuine fabrication enters
   a gate that was previously dominated by accuracy-failure papers), not a clean
   fabrication surge.

2. **The adoption→criticality gradient (S4-1) is NOT explained by generative
   technology.** Spearman(critical_rate, FDA_adoption) = **−0.647** (p = 0.004)
   over 18 specialties — the S4-1 gradient reproduces. Controlling for
   generative-share via **partial Spearman barely moves it: −0.647** (p = 0.005),
   i.e. **0% attenuation**. And critical_rate vs generative-share is **flat**
   (ρ = −0.011, p = 0.96). The data therefore support a **FAMILIARITY / adoption**
   reading of the gradient, **not a technology-driven** one — and this holds even
   though the chosen proxy is biased *toward* the technology reading (see caveat).

---

## Scope of the numbers below

**Parts 1–4 below now cite the canonical abstract-present run** (the 4,747 A+C
papers carrying an abstract; 412 title-only papers dropped as QC;
`q7_phase3_analyses.py --abstract-only`, figures with the `_abstractonly` suffix).
The full-corpus (title-inclusive, n=5,159) run was the earlier default; dropping
the title-only papers does not move any conclusion:

| metric | full A+C (5,159) | **abstract-present (4,747)** |
|---|--:|--:|
| gate composition: misclassification-dominant every year | yes (55–78%) | **yes (56–90%)** |
| gate recall for confabulation | 90.5% | **89.7%** |
| trend: confab-broad ρ(year) / gen-share ρ(year) | +0.94 / +0.94 | **+0.94 / +0.94** |
| Spearman(critical_rate, FDA) | −0.647 | **−0.647** |
| partial(critical_rate, FDA \| gen-share) | −0.648 | **−0.647** |
| Spearman(critical_rate, gen-share) | −0.026 | **−0.011** |
| divergence: generative-not-confab / confab-not-generative | 39.0% / 1 | **39.1% / 1** |

---

## Part 1 — Gate audit (heterogeneity + leakage)

`output/figures/q7_gate_composition_abstractonly.png` · n gated = 2,226 (abstract-present)

**failure_mode composition WITHIN the old "hallucination" gate (% by year).**
Percentages are **column-normalized within each year**: the denominator for a
given year is *all hallucination-gated papers published that year* (each column
sums to 100%). E.g. 2021 gated total = 56 (0 confab + 39 misc + 0 both + 17
none), so misclassification = 39/56 = 69.6%.

| failure_mode | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|--:|--:|--:|--:|--:|--:|
| confabulation | 0.0 | 1.6 | 10.7 | 11.8 | 9.1 | 12.2 |
| misclassification | **69.6** | **90.2** | **56.3** | **61.4** | **65.6** | **65.0** |
| both | 0.0 | 0.0 | 5.1 | 11.6 | 11.6 | 9.5 |
| none_or_unclear | 30.4 | 8.2 | 27.9 | 15.2 | 13.8 | 13.3 |
| *(year gated n)* | *56* | *61* | *215* | *560* | *883* | *451* |

Confab-involved (confab+both) inside the gate: 0% → 2% → 16% → 23% → 21% → 22%.
Misclassification-involved stays 56–90% throughout. **The gate conflates "AI got
it wrong" with "AI made it up."**

**Gate-recall check** — confab-involved papers the old gate did **not** flag:
51 papers missed (mostly recent: 5/9/19/18 in 2023–2026). Overall gate **recall
for confabulation = 446/497 = 89.7%** — recall is decent; the gate's problem is
**precision** (only ~20% of gated papers are actually fabrication).

---

## Part 2 — Gate-independent trend (all A+C)

`output/analyses/q7_ac_temporal_trend_abstractonly.csv`

> **Honest-framing note (verbatim):** The temporal rise in generative-share is
> partly expected because generative AI is new; it is not a standalone finding.
> The informative results are the failure_mode shift toward confabulation and the
> cross-sectional analysis below.

| year | n | confab-broad % [95% CI] | confab-strict % | generative-share % [95% CI] |
|---|--:|--:|--:|--:|
| 2021 | 245 | 0.0 [0.0–0.0] | 0.0 | 5.3 [2.9–8.2] |
| 2022 | 285 | 0.4 [0.0–1.1] | 0.4 | 2.5 [0.7–4.2] |
| 2023 | 543 | 7.2 [5.0–9.4] | 5.0 | 33.0 [29.3–37.0] |
| 2024 | 1076 | 13.0 [11.1–15.1] | 6.4 | 56.9 [53.8–59.9] |
| 2025 | 1757 | 11.4 [10.0–12.9] | 5.1 | 57.8 [55.5–60.2] |
| 2026 | 841 | 13.8 [11.5–16.2] | 8.0 | 62.8 [59.3–66.0] |

Spearman over years: confab-broad ρ = +0.943 (p = 0.005); generative-share
ρ = +0.943 (p = 0.005). Both rise, but confab plateaus in the low teens while
generative-share climbs to ~63%. (S5-1-b on A+C shows the same plateau:
confab-among-generative flat near 20–23%.)

---

## Part 3 — S4-1 disentanglement

`output/figures/q7_s41_disentangle_abstractonly.png`

Over the 18 specialties (generative-share computed on A+C critical papers,
abstract-present):

| relationship | ρ | p |
|---|--:|--:|
| Spearman(critical_rate, FDA_adoption) | **−0.647** | 0.004 |
| Spearman(critical_rate, generative_share) | −0.011 | 0.964 |
| Spearman(FDA_adoption, generative_share) | −0.028 | 0.913 |
| **PARTIAL(critical_rate, FDA | generative_share)** | **−0.647** | 0.005 |

**Attenuation |ρ|: 0.647 → 0.647 (≈ 0% reduction).** The FDA gradient survives
controlling for generative-share essentially untouched. **Interpretation: the
gradient is FAMILIARITY-driven, not technology-driven.** Specialties critical of
AI are not simply the ones exposed to more generative AI — generative-share
carries no cross-sectional signal for criticality here.

**Dermatology (explicit):** critical_rate = 36.5% (rank #2 overall),
FDA_devices = **0**, generative_share (A+C) = **40.7%** (below-median),
n_critical = 91. Dermatology's high criticality is **not** explained by high
generative exposure — consistent with the familiarity reading (high-criticality
specialty with low clinical AI adoption).

> **Endogeneity caveat (verbatim):** generative-share is computed on critical
> papers only → endogenous to criticality, tends to OVER-attenuate (bias toward
> technology reading). Treat as suggestive; a full-discourse covariate is the
> robustness upgrade.

Note this caveat *strengthens* the conclusion here: even a proxy biased toward
finding technology-driven attenuation found **none**, so the familiarity reading
is robust to that bias.

---

## Part 4 — Divergence (the two axes are independent)

- **generative but NOT confabulation: 1,858 papers (39.1% of abstract-present
  A+C).** The large mass: most critical generative-AI papers test LLMs for
  **accuracy / bias / judgement**, not fabrication. Examples: "How well does an AI
  chatbot answer clinical questions" (misclassification); "Performance of ChatGPT
  on Chinese national medical licensing examinations" (misclassification); "LLMs
  for surgical informed consent: an ethical perspective" (none_or_unclear).
- **confabulation but NOT generative: 1 paper (0.02%).** The lone case —
  *"The Current Status of AI-accelerated MRI Techniques in Clinical Use"* — a
  **discriminative** image-reconstruction model that "hallucinates" invented or
  disappearing lesions. A genuine edge case proving fabrication is *almost* but
  not *entirely* a generative phenomenon (confabulation is ~99% generative in
  the full contingency).

The asymmetry (1,858 vs 1) is the point: **generative ≠ confabulation.** Knowing a
paper is about generative AI tells you almost nothing about whether it raises a
fabrication concern — the two axes carry independent information, which is exactly
what the old single "hallucination" gate collapsed.

---

## Part 5 — Validation (κ measured + adjudicated)

Blind set of 120 papers (stratified pub_year × failure_mode, model labels hidden)
coded by one human rater in `q7_validation_coding.xlsx`; the 46 human–model
disagreements were then adjudicated in a second considered pass with the model's
rationale visible (`q7_adjudication.xlsx`). Validation is computed on the
**108 papers that carry an abstract** (12 title-only papers excluded as a QC
step — both raters had only a title and code unreliably from it). Final per-axis
agreement (`q7_kappa.py --adjudicated --require-abstract`; full report
`q7_kappa_report_adjudicated_abstractonly.md`):

| axis | Cohen's κ | Gwet AC1 | raw agreement | κ/κ_max | strength |
|---|--:|--:|--:|--:|---|
| **model_type** | **+0.953** | +0.965 | 97.2% | 0.97 | almost perfect |
| **failure_mode** | **+0.796** | +0.805 | 85.2% | 0.93 | substantial |

Per-category one-vs-rest κ is now uniformly strong, including the formerly weak
`confabulation` category (κ 0.37 → **0.75**). Both axes are validated to
publication-grade agreement.

How we got there (sensitivity, `q7_kappa_compare.py`):

| condition | failure_mode κ | model_type κ | full report (with matrices) |
|---|--:|--:|---|
| blind, all 120 | 0.541 | 0.798 | `q7_kappa_report.md` |
| blind, abstract-only (108) | 0.574 | 0.843 | `q7_kappa_report_abstractonly.md` |
| adjudicated, all 120 | 0.744 | 0.932 | *(numbers via q7_kappa_compare.py)* |
| **adjudicated, abstract-only (108)** | **0.796** | **0.953** | `q7_kappa_report_adjudicated_abstractonly.md` |

> Note: the **blind / abstract-only (n=108)** full report
> (`q7_kappa_report_abstractonly.md`, with confusion matrices, per-category κ, and
> all coefficients) was added later in commit S5-9 — it was initially omitted; the
> first pass only produced the blind-120 and the adjudicated-abstract-only
> reports. Numbers are unchanged from the sensitivity table above.

Adjudication was the dominant lever (+0.20 on failure_mode); the abstract QC
added +0.05. Title-only papers were disproportionately disagreement-prone (7 of
12 fell in the original 46 disagreements). 18 residual disagreements remain after
adjudication (the rater held against the model) — agreement is genuine, not
forced.

**Bias direction still favours the headline:** the residual disagreement is the
rater being *more conservative about claiming fabrication* than the classifier,
so the true confab-share is if anything below the classifier's ~20% plateau —
consistent with "fabrication concern did not scale with LLM uptake." Absolute
confab figures remain best read as classifier-measured upper bounds.

---

## Decision owed to Dan

The Q7 axes were designed to **de-conflate** the original "hallucination" theme.
Two options:

1. **Supplementary analysis** (recommended default) — present Q7 as a
   commentary-supplement that *reinterprets* the hallucination-theme rise
   (composition shift + accuracy-vs-fabrication split + technology-vs-familiarity
   disentanglement), leaving sessions 1–3 theme numbers intact.
2. **Replace the hallucination theme gate** with the mechanism-based
   failure_mode axis — more honest, but **changes the session 1–3 theme numbers**
   (the "+30 pp hallucination rise" headline would be restated as a smaller,
   plateauing confabulation trend plus a separate generative-technology turnover).

This is a manuscript-framing call for Dan, not a data question. The data support
either; option 2 is the more defensible scientific claim but has downstream cost
on already-circulated figures.

---

### Caveats (carry-forward)

- Critical-only scope (A+C); not the full discourse. A full-corpus generative
  covariate is the robustness upgrade for Part 3.
- Per-specialty n is small for several specialties in the Alarm-only S5-1
  analyses (flagged in `q7_alarm_by_specialty.csv`); the A+C disentanglement
  (Part 3) uses all 18.
- Validation (adjudicated, abstract-present n=108): failure_mode κ = 0.80
  (substantial), model_type κ = 0.95 (almost perfect). Absolute confab-share
  figures remain best read as classifier-measured upper bounds (Part 5).
- A `task_type` axis (diagnostic/text-generation/etc.) was discussed as a
  possible third axis; not yet implemented.

### Artifacts

**Canonical package = full-abstract (abstract-present) + A+C scope.** See
`q7_session5_package.md` for the curated manifest. The Alarm-only and full-corpus
(title-inclusive) variants remain in git history but are superseded.

| file | what |
|---|---|
| `output/analyses/q7_session5_package.md` | **manifest of the full-abstract package** |
| `output/analyses/q7_classified_ac.csv` | 5,161 critical papers, both axes (base table) |
| `output/analyses/q7_ac_temporal_trend_abstractonly.csv` | Part 2 trend + CI (A+C, abstract-present) |
| `output/analyses/q7_ac_by_specialty_abstractonly.csv` | S5-1-a specialty table (A+C, abstract-present) |
| `output/analyses/q7_ac_temporal_shares_abstractonly.csv` | S5-1-b plateau table (A+C, abstract-present) |
| `output/analyses/q7_validation_coding.xlsx` | 120-paper coded set |
| `output/analyses/q7_adjudication.xlsx` | 46 disagreements, adjudicated |
| `output/analyses/q7_kappa_report_adjudicated_abstractonly.md` | final κ report |
| `output/figures/q7_ac_temporal_abstractonly.png` | Phase 1 temporal (A+C) |
| `output/figures/q7_gate_composition_abstractonly.png` | Part 1 gate audit |
| `output/figures/q7_s41_disentangle_abstractonly.png` | Part 3 disentanglement |
| `output/figures/q7_ac_failuremode_by_specialty_abstractonly.png` | S5-1-a specialty (A+C) |
| `output/figures/q7_ac_confab_plateau_abstractonly.png` | S5-1-b plateau (A+C) |
