# Prophecy Panel — Pre-Registration Protocol

**Analysis:** Forward-validation of 2021–2023 predictive claims against the 2024–2026 published record
**Status:** Frozen before adjudication. Any deviation after this point is logged as a protocol amendment with date and rationale.
**Prepared by:** Kingsley (Lixing) Wang · **Sign-off:** D. Poenaru
**Frozen on:** [FILL DATE] · **Evidence cutoff:** [FILL — v1 retrieval date]

---

## Part A — Protocol (detailed; for sign-off, freeze before any adjudication)

### A1. Objective and framing

This panel is an **exploratory forward-validation**: a structured reconciliation of the discourse's earlier predictions against the subsequent published record. It is the closing analysis of the Results and operationalizes, at the level of individual claims, the corpus-level findings that Advocacy collapsed (Spearman ρ = −1.0) and that critical stance rose monotonically.

Organizing axis is **falsifiability**, not optimism: we ask not "were optimists right?" but "of the predictions specific enough to be tested, which were borne out?" This reframes the Advocacy-only scope (see A2) as the natural product of a falsifiability filter rather than a convenience.

Section-appropriate protective framing (to appear in the panel's opening and limitations): *we adjudicate whether the discourse's predictions were borne out in the subsequent published record — not whether the underlying AI "works." Verdicts describe the state of the literature at the evidence cutoff, not ground-truth capability.*

### A2. Candidate pool and inclusion

- **Source:** `prophecy_panel_candidates_2021_2023.csv`, n = 92 = (stance = Advocacy) ∧ (pub_year ∈ 2021–2023) ∧ (predictive_claim = yes), as labelled by the v1 Sonnet classifier.
- **Advocacy-only justification (pre-committed):** falsifiable predictions — specific, mechanistic, time-bound — concentrate in the Advocacy tier. Pessimistic claims are disproportionately existence claims ("patient harm will occur") or unfalsifiable conditionals ("without regulation, unsafe"), which a single instance confirms or which no counterfactual can adjudicate. The Advocacy concentration of falsifiable claims is itself reported as a finding.
- **Flag validation (the key integrity step):** the `predictive_claim` flag was produced by the v1 classifier and never validated. Every one of the 92 records is manually inspected to confirm it contains a *specific forward-looking claim*. We report flag precision = (confirmed) / 92. False positives are excluded with a one-line reason logged. Expected attrition concentrates in the 27 title-only records; anticipated confirmed N ≈ 88–90.
- **Unit of analysis:** **per-claim, one signature prediction per paper** — the single most specific and falsifiable bet the paper makes. This keeps n_claims = n_papers (honest Sankey, no話痨-paper visual dominance, no pseudo-replication from non-independent same-author claims). Papers carrying ≥ 2 genuinely independent major bets are flagged and the secondary claim handled as a separate, explicitly noted entry.
- **Title-only records (n = 27):** signature claim extracted from the title; records whose title yields no specific testable claim are excluded as flag false positives.

### A3. Tier taxonomy (frozen, assigned blind to reality)

Left axis of the Sankey. Assignment is by **claim structure, not topic.** Topic (specialty/theme) is recorded as a secondary attribute for the appendix. A provisional card-sort was performed at title level; final per-claim assignment occurs during signature-claim extraction and must be completed **before** any 2024–2026 evidence is consulted.

- **Tier 1 — Specific superiority / replacement.** Testable head-to-head or displacement claims: AI will outperform / replace clinicians, or has done so in a way predicted to generalize. *Examples: "AI outperformed every dermatologist"; "chatbot surpasses trained radiologists"; "cancer care by committee to be superseded by AI."* Highest falsifiability.
- **Tier 2 — Capability deployment.** AI will enter routine clinical use, accelerate drug development, or become embedded in workflow — a concrete mechanism, testable against the later record. *Examples: "lung cancer screening: the future is now"; "from concept to clinic"; pharma pipeline acceleration.* Medium falsifiability.
- **Tier 3 — Diffuse transformation.** "Revolutionize / paradigm shift / next frontier" with no mechanism and no horizon. *Examples: "revolutionizing infectious disease control"; "catalyzing a sustainable global healthcare paradigm."* Lowest falsifiability; largely escapes adjudication by construction.

### A4. Verdict rubric (4 levels, objective definitions)

- **Borne out** — positive evidence in the record that the predicted outcome materialized substantially as claimed.
- **Partially borne out** — the predicted direction is realized but narrower, weaker, or slower than claimed (e.g. piloted but not in routine use).
- **Not borne out** — **positive contrary evidence** that the predicted outcome did not materialize.
- **Too early / unfalsifiable** — horizon not yet reached; OR claim too vague/mechanism-free to test; OR the corpus is silent (no evidence either way).

**Iron rule (single biggest validity safeguard):** corpus silence maps to *too-early / insufficient*, **never** to *not borne out*. Only positive contrary evidence yields *not borne out*. This prevents retrieval misses from manufacturing false failures.

**Default for open-ended, no-deadline claims:** *too-early / unfalsifiable* unless positive evidence of movement or reversal exists.

### A5. Evidence regime

- **Primary evidence: the internal corpus.** Adjudication uses the 2024–2026 evaluative/discourse subset (~[FILL] records) of the same corpus. This yields a **closed-loop, fully reproducible** design — the later record adjudicates the earlier predictions — and is reported as a methodological strength.
- **Structural boundary (pre-committed):** the corpus records *what was published*, not *what happened*. It adjudicates capability-materialization claims well, but cannot supply hard market/regulatory/labor facts. The ~10–15 "hard-fact" claims (replacement, headcount, regulatory clearance) are tagged. For these, either (a) the verdict is restricted to "the literature does not report the predicted outcome" (weaker, still closed-loop), or (b) one clearly-cited external datum (e.g. FDA clearances, workforce data) is permitted. We report the count of externally-adjudicated verdicts. **Internal-only is run first and in full; external supplementation is decided afterward.**
- **Evidence cutoff:** [FILL — v1 retrieval date]. Frozen; adjudication consults nothing dated after it.
- **Transparency:** every verdict carries ≥ 1 cited evidence item. This is the primary reliability mechanism (see A7).

### A6. Retrieval procedure (RAG-assisted, human-verified)

1. Restrict corpus to 2024–2026 (predictions are 2021–2023; evidence is the later record).
2. Embed the subset; for each signature claim, retrieve top-k most-similar abstracts. *(The full 35 MB corpus cannot be placed in a single context window (~8–9 M tokens); genuine retrieval is required, not in-context stuffing.)*
3. Prompt the model **neutrally** — "summarize the 2024–2026 status of [claim]" — never "find evidence this failed."
4. **The model never assigns a verdict.** It surfaces candidate evidence; the human verifies every item and assigns the verdict.
5. A retrieval miss is *too-early / insufficient*, not a failure (per A4 iron rule).

### A7. Reliability

- **Primary mechanism — evidence transparency.** Each verdict cites checkable evidence; the reader serves as second rater. For clean fact-checkable cases this is stronger than inter-rater agreement, as each verdict is independently verifiable without trusting two coders.
- **Targeted adjudication.** The second rater (D.P.) independently codes only the **ambiguous subset** — the *partial* and *too-early* calls — blind to the primary verdict. Raw agreement on that subset is reported in one sentence.
- **No formal κ:** with n this small and verdicts ordinal over 4 levels, κ is uninformative and unstable; it is not reported.
- **Stance-blind coding** where feasible: verdicts assigned without reference to the original stance label, to avoid "it's Advocacy, so it probably failed" bias.

### A8. Visualization specification

- **Sankey.** Left = 3 tiers (node height ∝ n); right = 4 verdicts (node height ∝ n); ribbon width ∝ count, **every ribbon labelled with its count**.
- Categories frozen before adjudication (A3, A4). No ribbon shown without its count; small n is not masked by wide ribbons.
- Publication-grade, exported as **SVG for downstream Illustrator editing**.
- Optional: tier nodes coloured along a falsifiability gradient (Tier 1 darkest → Tier 3 lightest) so the figure reads as both flow and gradient. No second quantitative axis is introduced.

### A9. Analysis and reporting structure

- **Census Sankey over the full confirmed N = primary exhibit.** Because every confirmed claim is adjudicated, there is no sampling and therefore no sampling bias; the ribbons are the population, not a sample.
- **10–15 deep case studies in prose.** Selected for specificity, falsifiability, and visibility — explicitly *illustrative, not a sample for generalization*; the census carries the distribution, so case selection cannot be cherry-picking.
- **Appendix:** full candidate table — signature claim, tier, topic, verdict, cited evidence, evidence source (internal/external) — for every confirmed record.

### A10. Pre-committed limitations

- Exploratory; small N; verdicts involve subjective judgment.
- The `predictive_claim` flag was unvalidated at classification time and validated only post-hoc (precision reported in A2).
- Advocacy-only scope supports the claim that optimists over-promised; it does **not** support a symmetric claim that critics were vindicated.
- Internal-corpus evidence reflects *what was published*, not ground-truth capability.
- A single primary rater; mitigated by per-claim cited evidence and targeted second-rater adjudication of ambiguous cases.

---

## Part B — Methods paragraphs (manuscript-ready; tighten tense after running)

**Candidate identification and flag validation.** From the classified corpus we drew all records labelled Advocacy with a positive predictive-claim flag and published 2021–2023 (n = 92). Because the predictive-claim flag was produced by the stance classifier and not separately validated, two reviewers manually confirmed that each record contained a specific forward-looking claim; flag precision was [FILL]/92, and [FILL] records were excluded as false positives, yielding N = [FILL]. The unit of analysis was the single most specific, falsifiable prediction per paper (its "signature claim"); the rare papers advancing two independent major predictions were entered as separate, annotated claims.

**Claim taxonomy.** Signature claims were sorted, blind to subsequent evidence, into three tiers by claim structure rather than topic: specific superiority/replacement (testable head-to-head or displacement claims), capability deployment (concrete mechanism entering clinical use, drug development, or workflow), and diffuse transformation (mechanism-free, horizon-free "revolution" claims). Topic was retained as a secondary attribute.

**Verdict rubric.** Each claim was adjudicated against the 2024–2026 published record as borne out, partially borne out, not borne out, or too early/unfalsifiable. Not-borne-out required positive contrary evidence; absence of evidence was coded too early/unfalsifiable, never as failure. Open-ended claims without a horizon defaulted to too early/unfalsifiable unless positive evidence of movement or reversal was identified.

**Evidence and adjudication.** Primary evidence was the 2024–2026 evaluative subset of the same corpus, giving a closed-loop, reproducible design in which the later record adjudicates the earlier predictions. Evidence was identified by retrieval over the later-year subset, with neutral prompting; the model surfaced candidate evidence and a reviewer verified every item and assigned the verdict. A small number of claims turning on market or regulatory facts the literature cannot supply were supplemented with a single cited external source; the count of externally-adjudicated verdicts is reported. Evidence consulted was frozen at the retrieval cutoff ([FILL]).

**Reliability.** Each verdict carries cited evidence, allowing independent reader verification. A second rater independently coded the ambiguous (partial and too-early) subset blind to the primary verdict; raw agreement was [FILL]. Given the small, ordinal verdict set, formal agreement coefficients were not computed.

**Visualization.** Flows from claim tier to verdict are shown as a Sankey diagram with every ribbon labelled by count and node height proportional to claim number; categories were fixed before adjudication and sample sizes are shown rather than masked.
