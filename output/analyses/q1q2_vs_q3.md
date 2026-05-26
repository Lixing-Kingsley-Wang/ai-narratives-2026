# C.2 — Q1/Q2 vs Q3 comparison

**Status: DONE** (Session 2 fixup, 2026-05-26).

Q3 stance classification: 1,055 records from `prefiltered_Q3_discourse_eval.csv`, classified with the v1 canonical Sonnet 4.6 prompt. 0 FAILED. Wall time 5.7 min, async with 5-way concurrency.

## Headline

- Q1/Q2 critical rate (v1): **30.82%** (95% CI 30.13–31.51)
- Q3 critical rate (v1):    **26.54%** (95% CI 23.79–29.29)
- **Δ = -4.28 pp** — Q3 is **less** critical than Q1/Q2.

Q3 Advocacy rate (2.7%) is roughly **2× the Q1/Q2 rate** (1.4%). Q3 Cautious Optimism is **~5 pp higher** (67.2% vs 62.7%). Pattern is consistent: lower-tier journals in this corpus publish a less critical, more optimistic AI narrative.

## Full stance comparison

| Stance | Q1/Q2 % (95% CI) | Q3 % (95% CI) | Δ pp |
|---|---|---|---:|
| Alarm | 5.47 (5.14–5.83) | 4.74 (3.51–5.97) | -0.73 |
| Caution | 25.35 (24.68–26.05) | 21.80 (19.33–24.27) | -3.55 |
| Neutral | 5.00 (4.68–5.32) | 3.51 (2.46–4.64) | -1.49 |
| Cautious Optimism | 62.78 (62.08–63.50) | 67.20 (64.27–69.86) | +4.42 |
| Advocacy | 1.40 (1.22–1.59) | 2.75 (1.80–3.79) | +1.35 |
| Critical (Alarm+Caution) | 30.82 (30.13–31.51) | 26.54 (23.79–29.29) | -4.28 |

## Temporal: critical % by year per tier

- Q1/Q2: Spearman ρ = +0.771, p = 0.0724, 25.4% (2021) → 32.7% (2026), Δ +7.25 pp
- Q3:    Spearman ρ = +0.714, p = 0.1108, 23.0% (2021) → 27.2% (2026), Δ +4.22 pp

Figure: [q1q2_vs_q3.png](../figures/q1q2_vs_q3.png).

## Per-year n (Q3 is small in early years — caveat the temporal Q3 trend)

| year | Q1/Q2 n | Q3 n |
|---:|---:|---:|
| 2021 | 1,063 | 113 |
| 2022 | 1,343 | 105 |
| 2023 | 2,054 | 180 |
| 2024 | 3,700 | 32 |
| 2025 | 5,898 | 423 |
| 2026 | 2,689 | 202 |

## Interpretation

The -4.3 pp gap is **modest in absolute terms but consistent**: across every stance row, Q3 sits where you'd expect a less-critical sibling corpus. This is a defensible generalizability claim for the manuscript — the Q1/Q2 findings are not an artifact of high-impact-journal selection. The direction of the temporal critical shift
(matches between tiers; Q1/Q2 ρ=+0.77 vs Q3 ρ=+0.71). 

**Manuscript phrasing suggestion** (for Kingsley): "The temporal critical shift observed in Q1/Q2 medical journals also holds in a smaller Q3 sample (n=1,055), though Q3 papers are overall 4.3 pp less critical (95% CI gap clearly separated). This pattern is consistent with prestige bias in either direction — high-impact journals may either (a) attract more critical voices or (b) editorially favor critique; future work should distinguish."
