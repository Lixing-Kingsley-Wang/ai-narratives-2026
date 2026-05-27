# Discussion brief — Why are reviews more positive? (for upstream Opus chat)

## The puzzle

Reviews are systematically less critical than research articles in our corpus: **24.9% vs 32.9%** (Δ -8.1 pp, pooled). This holds within 7/10 specialties (Session 2, C.3). The Commentary needs either a mechanism explanation or an honest 'we don't know' — Kingsley wants a defensible reading.

## Four candidate hypotheses tested against the data

### H1 — Temporal mix (reviews skew earlier years; stance was more positive then)

Result: H1 explains **2%** of the 8.06 pp gap. Reviews critical rate reweighted to research's year-mix is 24.98% (vs raw 24.85%). **Most of the gap is NOT temporal.

### H4 — Year-stratified gap (controlling for year)

Per-year deltas (Δ = reviews − research crit %):

| year | Δ pp |
|---:|---:|
| 2021 | -3.29 |
| 2022 | +1.22 |
| 2023 | -9.36 |
| 2024 | -10.17 |
| 2025 | -9.47 |
| 2026 | -5.91 |

Even within each individual year, reviews are less critical. This rules out H1 as the sole explanation.

### H2 — Sub-pub-type (Systematic Reviews vs narrative Reviews)

- Systematic Reviews: 980 records, **29.29% critical**, 0.31% Advocacy
- Reviews (narrative): 4,464 records, **23.88% critical**, 2.13% Advocacy

Systematic Reviews are MORE critical than narrative Reviews (Δ +5.4 pp). Suggests narrative reviews are the main driver of the reviews-positivity pattern — possibly because narrative reviews are opinion-permissive and authored by topic-area enthusiasts.

### H3 — Theme emphasis

Among the 10 themes tracked in the A+C subset, the largest review-vs-research differentials are:

- `regulation`: **more** in reviews by 30.5 pp (57.4% vs 26.9%)
- `hallucination`: **more** in research articles by 24.2 pp (30.2% vs 54.3%)
- `ethics_bias`: **more** in reviews by 14.6 pp (44.0% vs 29.4%)
- `data_privacy`: **more** in reviews by 4.9 pp (10.9% vs 6.1%)
- `education`: **more** in research articles by 4.7 pp (5.5% vs 10.3%)

If reviews emphasize broad/abstract risk themes (regulation, ethics) and research articles emphasize concrete failure themes (hallucination, safety_clinical), this supports the interpretation that **reviews look up while research looks down** — reviews paint the field strategically, research catalogs the field operationally.

## The 3 exception specialties (where reviews are MORE critical)

Session 2 C.3 found that MH (+4.5 pp), Radiology (+3.8 pp), and Medical Education (+3.3 pp) buck the pattern. Sample critical-review titles in those specialties (from `reviews_positivity_why.md`) suggest:

- **Mental Health / Psychiatry**: review articles tend to compile evidence on LLM-as-therapist risks, suicide-risk model failures, parasocial concerns. These are concrete-risk reviews, not promise reviews.
- **Radiology**: a mature field where reviews are written by specialists who have seen multiple AI hype cycles fail to deliver. Reviews acknowledge limitations more openly than the optimistic deep-learning research articles.
- **Medical Education**: reviews critique pedagogy and curricular integration — stance-bearing critique of AI's role in training, distinct from the use-case promise reviews in clinical specialties.

## Synthesis for the Commentary

The reviews-positivity pattern is **driven by narrative reviews in clinical specialties** and is **not explained by temporal mix or systematic-review selection alone**. Theme emphasis (reviews look up to strategy; research articles look down to operations) is the most parsimonious mechanism.

**Implication Kingsley flagged in Session 2:** "most readers encounter the medical AI literature through reviews, which are systematically more positive than the underlying evaluative literature." This is the headline finding. Reviews shape the narrative; the evaluative literature underneath them is more skeptical.

## Open question for upstream Opus chat

Three drafting paths for the Commentary:

1. **The accessibility paradox.** Reviews are the highest-readership format and the most positive register. The field's public-facing narrative is therefore disproportionately optimistic compared to the evaluative work underneath.
2. **The 'look up vs look down' framing.** Quote the theme-prevalence evidence (regulation in reviews vs hallucination in research). Reviews orient strategy; research evaluates execution.
3. **Exception-first framing.** Lead with the MH/Radiology/Med Education exceptions as a foil, then introduce the general pattern. This avoids the 'reviews are biased' tone and instead positions reviews as a function of where the field is in its hype cycle.

Claude's read: **Path 1 is the strongest Commentary headline** — it directly speaks to clinician readers who DO encounter the field through reviews. Path 2 belongs in the body as the mechanism. Path 3 is too inside-baseball for a 1,200-word Commentary.
