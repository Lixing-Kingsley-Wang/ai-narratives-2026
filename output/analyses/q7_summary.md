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
   set (2,448 papers), **misclassification is the majority every single year**
   (69–78% pre-2023, still 55–75% post-2023). Confabulation-involved papers are
   0–1% of the gate in 2021–22 and rise to only ~21–23% from 2023 on. So the
   ~+30 pp rise of the "hallucination" theme across sessions 1–3 is **partly a
   shift in what the gate is made of** (more genuine fabrication enters a gate
   that was previously dominated by accuracy-failure papers), not a clean
   fabrication surge.

2. **The adoption→criticality gradient (S4-1) is NOT explained by generative
   technology.** Spearman(critical_rate, FDA_adoption) = **−0.647** (p = 0.004)
   over 18 specialties — the S4-1 gradient reproduces. Controlling for
   generative-share via **partial Spearman barely moves it: −0.648** (p = 0.005),
   i.e. **0% attenuation**. And critical_rate vs generative-share is **flat**
   (ρ = −0.026, p = 0.92). The data therefore support a **FAMILIARITY / adoption**
   reading of the gradient, **not a technology-driven** one — and this holds even
   though the chosen proxy is biased *toward* the technology reading (see caveat).

---

## Part 1 — Gate audit (heterogeneity + leakage)

`output/figures/q7_gate_composition.png`

**failure_mode composition WITHIN the old "hallucination" gate (% by year):**

| failure_mode | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|--:|--:|--:|--:|--:|--:|
| confabulation | 0.0 | 1.4 | 10.7 | 12.9 | 9.7 | 12.3 |
| misclassification | **68.8** | **78.1** | **50.4** | **56.0** | **63.8** | **62.8** |
| both | 0.0 | 0.0 | 4.6 | 10.4 | 11.1 | 9.4 |
| none_or_unclear | 31.2 | 20.5 | 34.4 | 20.8 | 15.3 | 15.4 |

Confab-involved (confab+both) inside the gate: 0% → 1% → 15% → 23% → 21% → 22%.
Misclassification-involved stays 55–78% throughout. **The gate conflates "AI got
it wrong" with "AI made it up."**

**Gate-recall check** — confab-involved papers the old gate did **not** flag:
51 papers missed (mostly recent: 5/9/19/18 in 2023–2026). Overall gate **recall
for confabulation = 488/539 = 90.5%** — recall is decent; the gate's problem is
**precision** (only ~20% of gated papers are actually fabrication).

---

## Part 2 — Gate-independent trend (all A+C)

`output/analyses/q7_ac_temporal_trend.csv`

> **Honest-framing note (verbatim):** The temporal rise in generative-share is
> partly expected because generative AI is new; it is not a standalone finding.
> The informative results are the failure_mode shift toward confabulation and the
> cross-sectional analysis below.

| year | n | confab-broad % [95% CI] | confab-strict % | generative-share % [95% CI] |
|---|--:|--:|--:|--:|
| 2021 | 270 | 0.0 [0.0–0.0] | 0.0 | 5.2 [3.0–7.8] |
| 2022 | 333 | 0.3 [0.0–0.9] | 0.3 | 2.1 [0.6–3.6] |
| 2023 | 623 | 7.2 [5.3–9.1] | 5.1 | 34.2 [30.7–37.7] |
| 2024 | 1227 | 12.8 [11.1–14.5] | 6.9 | 55.9 [53.1–58.7] |
| 2025 | 1828 | 11.7 [10.3–13.2] | 5.5 | 58.8 [56.5–60.9] |
| 2026 | 878 | 13.9 [11.7–16.2] | 8.1 | 63.3 [59.9–66.5] |

Spearman over years: confab-broad ρ = +0.943 (p = 0.005); generative-share
ρ = +0.943 (p = 0.005). Both rise, but confab plateaus in the low teens while
generative-share climbs to ~63%. (Alarm-only S5-1-b showed the same plateau more
sharply: confab-among-generative flat near 20%.)

---

## Part 3 — S4-1 disentanglement

`output/figures/q7_s41_disentangle.png`

Over the 18 specialties (generative-share computed on A+C critical papers):

| relationship | ρ | p |
|---|--:|--:|
| Spearman(critical_rate, FDA_adoption) | **−0.647** | 0.004 |
| Spearman(critical_rate, generative_share) | −0.026 | 0.919 |
| Spearman(FDA_adoption, generative_share) | −0.034 | 0.893 |
| **PARTIAL(critical_rate, FDA | generative_share)** | **−0.648** | 0.005 |

**Attenuation |ρ|: 0.647 → 0.648 (≈ 0% reduction).** The FDA gradient survives
controlling for generative-share essentially untouched. **Interpretation: the
gradient is FAMILIARITY-driven, not technology-driven.** Specialties critical of
AI are not simply the ones exposed to more generative AI — generative-share
carries no cross-sectional signal for criticality here.

**Dermatology (explicit):** critical_rate = 36.5% (rank #2 overall),
FDA_devices = **0**, generative_share (A+C) = **40.0%** (below-median),
n_critical = 110. Dermatology's high criticality is **not** explained by high
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

- **generative but NOT confabulation: 2,013 papers (39.0% of A+C).** The large
  mass: most critical generative-AI papers test LLMs for **accuracy / bias /
  judgement**, not fabrication. Examples: "How well does an AI chatbot answer
  clinical questions" (misclassification); "Performance of ChatGPT on Chinese
  national medical licensing examinations" (misclassification); "LLMs for
  surgical informed consent: an ethical perspective" (none_or_unclear).
- **confabulation but NOT generative: 1 paper (0.04%).** The lone case —
  *"The Current Status of AI-accelerated MRI Techniques in Clinical Use"* — a
  **discriminative** image-reconstruction model that "hallucinates" invented or
  disappearing lesions. A genuine edge case proving fabrication is *almost* but
  not *entirely* a generative phenomenon (confabulation is 99.0% generative in
  the full contingency).

The asymmetry (2,013 vs 1) is the point: **generative ≠ confabulation.** Knowing a
paper is about generative AI tells you almost nothing about whether it raises a
fabrication concern — the two axes carry independent information, which is exactly
what the old single "hallucination" gate collapsed.

---

## Part 5 — Validation (κ measured: 120/120 coded)

Blind set of **120 papers** (stratified pub_year × failure_mode, model labels
hidden) coded by one human rater in `q7_validation_coding.xlsx`. Per-axis Cohen's
κ vs the classifier (`q7_kappa.py`; full report `q7_kappa_report.md`,
disagreements `q7_validation_disagreements.csv`):

| axis | Cohen's κ | raw agreement | strength (Landis–Koch) |
|---|--:|--:|---|
| **model_type** | **+0.798** | 87.5% | substantial / near-perfect |
| **failure_mode** | **+0.541** | 67.5% | moderate |

**model_type is reliable** (κ = 0.80). The generative/discriminative call —
which underpins the generative-share trend (Part 2), the S4-1 disentanglement
(Part 3), and the S5-1 specialty analyses — is well validated. Generative
detection is near-perfect (62/64 human-generative papers agreed).

**failure_mode is moderate** (κ = 0.54). Disagreement (46/120 rows differ on at
least one axis) concentrates at two boundaries: (a) the human coded 18 papers as
`none_or_unclear` that the model assigned a concrete mechanism (8 confab, 10
misc) — i.e. **the model is more willing to read a mechanism into thin
abstracts**; and (b) the `both` bucket is fuzzy (the model assigns `both`/
`confabulation` more readily than the human on misclassification papers). The
human is systematically **more conservative about claiming fabrication** than the
classifier.

**Direction of the bias matters for the headline:** because the model
*over*-assigns confabulation relative to a stricter human standard, the true
confab-share is, if anything, **lower** than the classifier's already-low ~20%
plateau. The κ disagreement therefore **strengthens** the core conclusion
("fabrication concern did not scale with LLM uptake") rather than threatening it.
It does mean the absolute confab-share numbers should be reported as
classifier-measured upper bounds, not precise point estimates.

Recommended robustness upgrade before publication: adjudicate the 46
disagreements (or add a second rater) to tighten failure_mode κ, since the
fabrication trend is a named result.

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
- failure_mode κ = 0.54 (moderate); model_type κ = 0.80 (substantial). Absolute
  confab-share figures are classifier-measured upper bounds; adjudicating the 46
  disagreements is the recommended robustness upgrade (Part 5).
- A `task_type` axis (diagnostic/text-generation/etc.) was discussed as a
  possible third axis; not yet implemented.

### Artifacts

| file | what |
|---|---|
| `output/analyses/q7_classified_ac.csv` | 5,161 critical papers, both axes |
| `output/analyses/q7_classified_alarm.csv` | Alarm subset (916) |
| `output/analyses/q7_classified_cautious.csv` | Caution subset (4,245) |
| `output/analyses/q7_ac_temporal_trend.csv` | Part 2 trend + CI |
| `output/analyses/q7_alarm_by_specialty.csv` | S5-1-a specialty table |
| `output/analyses/q7_alarm_temporal_shares.csv` | S5-1-b plateau table |
| `output/analyses/q7_validation_blind.csv` | 120-paper blind set (κ pending) |
| `output/figures/q7_gate_composition.png` | Part 1 |
| `output/figures/q7_s41_disentangle.png` | Part 3 |
| `output/figures/q7_alarm_confab_plateau.png` | S5-1-b |
| `output/figures/q7_alarm_failuremode_by_specialty.png` | S5-1-a |
| `output/figures/q7_alarm_temporal.png` | Phase 1 |
