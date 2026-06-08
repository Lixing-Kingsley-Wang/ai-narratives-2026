# Session 4 — Analysis Summary (ai-narratives-2026)

**Study:** Bibliometric analysis of AI/LLM *stance* in Q1/Q2 medical journals (with a
Q3 comparison arm), Jan 2021–Apr 2026. Stance = 5-point scale {Alarm, Caution,
Neutral, Cautious Optimism, Advocacy}; "critical" = Alarm + Caution. Corpus: 16,747
classified Q1/Q2 papers (v1 canonical), 1,055 Q3. Target: *Lancet Digital Health*
Commentary (~mid-Aug 2026). Senior author: Dan Poenaru.

**Global conventions used throughout:** v1 canonical, drop FAILED, pub_year
2021–2026, bootstrap n=1000 / seed=42 / percentile 95% CI. 2026 is a partial year
(data through April). All six analyses committed + pushed to branch
`analysis-session-4`.

---

## S4-1 — Does clinical AI adoption predict *less* critical stance? (Dan's "unfamiliarity" hypothesis)
- **Method:** Per-specialty critical rate (18 specialties, n≥30). External adoption
  index = FDA AI/ML-enabled device counts per specialty (1,430 devices mapped).
  In-corpus proxy = share of empirical-evaluation vs discourse papers. One-sided
  Spearman (Dan predicted negative) + permutation test.
- **Result:** **FDA adoption ρ = −0.65** (1-sided p = 0.002, perm 0.002); **in-corpus
  proxy ρ = −0.47** (p = 0.026, perm 0.028). Both significant and negative.
- **Verdict:** Supports Dan — specialties with *more* AI adoption (Radiology,
  Cardiology, Pathology) are *less* critical; low-adoption specialties more critical.
  Dermatology is a mild outlier (high critical despite imaging-adjacent).
- **Caveats:** FDA panels → specialty mapping is approximate and US-centric; in-corpus
  proxy is endogenous (same corpus that defines the outcome); n=18 is small (hence
  permutation test).
- **Files:** `analysis/run_specialty_aiadoption.py`,
  `output/analyses/specialty_aiadoption.csv`,
  `output/figures/specialty_aiadoption_vs_critical.png`.

## S4-2 — Is the "regulation" theme really declining, or just diluted?
- **Method:** Theme counts vs rates by year over the 5,161 A+C papers. Spearman on
  absolute **counts** (not rates), with 2021–2025 full-year sensitivity (2026 partial).
- **Result:** Regulation and ethics_bias **decline in rate but are flat/rising in
  absolute count.** The denominator (A+C papers) exploded — driven by
  hallucination/safety papers — so the *rate* drop is **dilution, not real decline.**
- **Verdict:** "Regulation discourse isn't shrinking; it's being crowded out of the
  conversation share by the safety/hallucination surge."
- **Files:** `analysis/run_theme_count_vs_rate.py`,
  `output/analyses/theme_count_vs_rate.csv`,
  `output/figures/theme_count_vs_rate.png`,
  `output/figures/theme_regulation_ethics_dual.png`.

## S4-3 — World map of critical stance by first-author country
- **Method:** geopandas + Natural Earth 110m, Robinson projection; bubble area ∝ n,
  fill = critical rate (RdYlBu_r diverging, centered on corpus mean 30.5%). Country =
  first author (90.3% resolved). Cutoff **n≥20** (lowered from 30), 45 countries;
  20≤n<50 flagged low-confidence (dashed, wide CIs ~30 pp). n≥50 comparison map = 36.
- **Result:** **US 34.5% (n=4,222) vs China 16.2% (n=1,904)** — the two research giants
  at opposite poles. High-critical cluster: Netherlands 44%, Denmark 43%, Australia
  42%, Ireland 41%, UK 41%. Low: Japan 18%, Iran 18%, S. Korea/India ~20%. New low-n
  additions (S. Africa, New Zealand, Latin America) are noisy.
- **Caveats:** First-author only; centroid bubbles; small-n countries unstable.
- **Files:** `analysis/run_country_critical_map.py`,
  `output/analyses/country_critical.csv`,
  `output/figures/world_critical_map.png/.pdf`,
  `output/figures/world_critical_map_n50.png/.pdf`.

## S4-4 — Audit: is the ~1,055 Q3 set anomalously over-excluded? (Dan flagged)
- **Method:** Reconstructed the full funnel and compared prefilter KEEP rates across arms.
- **Result:** **Q3 KEEP rate = 19.4% vs Q1/Q2 = 17.2%** — Q3 is *not* over-excluded
  (slightly *higher* retention). The small set just reflects an 18× smaller eligible
  journal pool (5,433 vs 97,492). Prefilter prompt is byte-identical across arms; no
  fetch truncation; duplicate `sjr_quartile` column harmless.
- **Verdict:** Legitimate — proceed. Minor caveat: 1,164 partial-2026 records lag an
  earlier filter snapshot (affects both arms equally).
- **Files:** `analysis/run_q3_prefilter_audit.py`,
  `output/analyses/q3_prefilter_funnel.csv`, `output/analyses/q3_prefilter_audit.md`.

## S4-5 — Is Q3's lower critical rate composition (more reviews) or within-type?
- **Method:** Direct standardization — reweight Q3's per-pub-type critical rates by
  Q1/Q2's pub-type mix.
- **Result:** Pub-type mixes are **near-identical** (Research 63 vs 62%, Review 33 vs
  33%). Mix-adjusted Q3 = 26.4% ≈ raw 26.5%. **Composition explains ~0% (−4%) of the
  4.3 pp gap.** Q3 is less critical *within every bucket* (Research −2.4, Editorial
  −9.3, Review −6.0, Letter −26.7 pp).
- **Verdict:** **Within-type** — a genuine quality-tier stance difference, not a
  documentary-mix artifact.
- **Files:** `analysis/run_q3_pubtype_mix.py`, `output/analyses/q3_pubtype_mix.csv`,
  `output/figures/q3_pubtype_mix.png`.

## S4-6 — Do first-author-industry papers differ in critical stance?
- **Method:** first_affiliation (98.4% coverage) → {industry, academic_clinical,
  mixed, other} by regex/keyword heuristic. Bootstrap CIs overall + by year +
  pub-type-controlled. Added "any-industry" sensitivity arm (industry + mixed
  collaborations).
- **Result:** Industry n=285 (1.7%): **27.7%** [22.8, 33.0] vs academic **30.8%**
  [30.0, 31.5], Δ −3.0 pp, **CIs overlap.** Any-industry n=1,209: **27.7%** [25.1,
  30.4] — *identical point estimate*, tighter CI, borderline. Pub-type-adjusted
  industry = 27.3% (not an artifact). Collaborations track industry, not academia.
- **Verdict:** Industry papers are directionally ~3 pp less critical, consistent across
  both definitions, but **not a clean statistical separation.** Caveats: first-author
  only; heuristic noise (~15–20% false positives on generic corporate suffixes); small
  industry n.
- **Files:** `analysis/run_industry_vs_academia.py`,
  `output/analyses/industry_vs_academia.csv`,
  `output/figures/industry_vs_academia.png`.

---

## Cross-cutting themes
1. **An "adoption → comfort" gradient** runs through several findings: specialties
   (S4-1), countries (US/China, S4-3), and arguably quality tier (S4-5) all show that
   *more engagement/exposure to AI correlates with less alarm.*
2. **Stance composition is shifting beneath stable totals** (S4-2): safety/hallucination
   is crowding the critical conversation, masking that regulation/ethics aren't actually
   fading.
3. **Most "subgroup is different" effects are within-type, not compositional** — Q3
   (S4-5) and Q3 prefilter (S4-4) both survived composition/process audits, which
   strengthens the substantive interpretation.

## Open questions for next discussion
- **Framing S4-1 without overclaiming causation** — the inverse adoption–criticality
  link is striking but the in-corpus proxy is endogenous and FDA mapping is rough. How
  hard can we push it in a Commentary?
- **The US/China divergence (S4-3)** — worth a formal test/standardization (e.g.
  adjusting for specialty/pub-type mix) before featuring it, or present descriptively?
- **Headline selection** — which 2–3 are Commentary-worthy vs supplementary? (Instinct:
  S4-1 adoption gradient + S4-2 dilution as the conceptual hooks; S4-3 map as the
  visual; S4-4/5/6 as robustness/supplementary.)
- **Industry signal (S4-6)** — keep as a reported null/weak effect, or cut for space?
- **Still outstanding:** the "prophecy panel" analysis (the one remaining project-plan
  item, not done this session).
