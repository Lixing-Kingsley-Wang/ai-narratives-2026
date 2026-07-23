# Discussion brief — East Asia low critical rate (for upstream Opus chat)

## Headline finding from Session 2

East Asia: 18.5% critical (n=3,260, 95% CI 17.2–19.9). About **half the NA+WEU rate** (both ~35%). Strong robust signal; n is large.

## Three candidate explanations

- **(a) Genuine voice divergence** — East Asian institutions publish more positive AI-medicine discourse on the same clinical problems.
- **(b) Conclusion-style norms** — institutional / linguistic conventions favor less critical conclusions in published abstracts (e.g., publication culture rewards constructive framing).
- **(c) Corpus composition** — East Asia publishes more methodology / less clinical-application papers, and clinical-application papers attract more criticism.

## Diagnostic 1 — Critical rate WITHIN specialty (East Asia vs NA+WEU)

If the EA-vs-(NA+WEU) gap holds *within* the same specialty (e.g., Radiology EA vs Radiology NA+WEU), composition (c) is **not** the full story.

| Specialty | n_EA | n_NA+WEU | EA % crit | NA+WEU % crit | Δ pp |
|---|---:|---:|---:|---:|---:|
| Medical Education | 188 | 507 | 18.1 (12.8–23.9) | 41.0 (36.5–45.6) | -22.9 |
| Medical Informatics / Digital Health | 746 | 2,561 | 31.4 (28.1–35.0) | 50.2 (48.4–52.2) | -18.8 |
| Surgery | 173 | 918 | 17.9 (12.1–23.7) | 31.7 (28.6–34.9) | -13.8 |
| Radiology / Diagnostic Imaging | 568 | 1,188 | 12.2 (9.7–15.0) | 24.7 (22.2–27.4) | -12.5 |
| Ophthalmology | 200 | 353 | 11.0 (7.0–15.5) | 22.9 (18.7–27.8) | -11.9 |
| Oncology | 368 | 743 | 11.7 (8.4–15.2) | 23.1 (20.2–26.4) | -11.5 |
| Dentistry | 131 | 209 | 16.0 (9.9–22.1) | 27.3 (21.5–33.5) | -11.2 |
| Internal Medicine / Primary Care | 264 | 579 | 14.0 (9.8–18.6) | 25.0 (21.8–28.7) | -11.0 |
| Pathology / Laboratory Medicine | 91 | 299 | 13.2 (6.6–20.9) | 23.4 (18.7–28.1) | -10.2 |
| Cardiology | 112 | 397 | 15.2 (8.9–22.3) | 18.1 (14.4–22.2) | -3.0 |

**Within-specialty Δ pattern:** Gap **persists** within every major specialty — points away from (c) and toward (a)/(b).

## Diagnostic 2 — Per-country critical rate within East Asia

If China, Japan, S. Korea, etc. differ substantially, the regional bucket is not a uniform voice; the explanation must accommodate country-level heterogeneity.

| Country | n | Critical % (95% CI) |
|---|---:|---|
| Hong Kong | 95 | 31.6 (21.1–41.0) |
| Singapore | 179 | 26.8 (20.7–33.5) |
| Taiwan | 169 | 21.3 (15.4–27.2) |
| South Korea | 487 | 20.3 (16.6–24.2) |
| Japan | 424 | 19.6 (15.8–23.6) |
| China | 1,903 | 16.1 (14.5–17.8) |

## Diagnostic 3 — Mix-adjusted East Asia critical rate

Reweighting East Asia's per-specialty critical rates by the NA+WEU specialty mix gives **19.89%** (vs raw EA 18.53% and raw NA+WEU 35.10%).

- **Composition explains 8%** of the EA-vs-(NA+WEU) gap (1.36 pp of 16.57 pp total).
- **Residual 92%** is not explained by composition — that's the part requiring explanation (a) or (b).

## Open question for upstream Opus chat

Given the mix-adjustment leaves ~92% of the gap unexplained, and given the within-specialty gap is consistent across every major specialty, how should the Commentary discuss this?

**Three drafting options:**

1. **Lead with the limitation.** "East Asia's lower critical rate may reflect publication norms in abstracts; we cannot distinguish from data alone." Hedges, but honest.
2. **Lead with the empirical observation, defer interpretation.** "East Asian publications show a markedly lower critical-stance rate (18.5% vs ~35% in NA/WEU), which persists after adjusting for specialty mix. Future qualitative work is needed to distinguish institutional voice from conclusion-style norms."
3. **Take a position.** Argue that the within-specialty consistency (every specialty shows the same EA-vs-NA+WEU gap, not just methodology-heavy ones) suggests (b) conclusion-style norms are at least partly responsible. Risky without outside-data anchor.

Claude's read: **Option 2** is the right register for a Lancet Digital Health Commentary — empirically anchored, methodologically honest, opens a research direction.
