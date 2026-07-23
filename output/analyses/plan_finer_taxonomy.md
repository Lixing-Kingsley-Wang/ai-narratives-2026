# Finer-grained specialty taxonomy — decision brief for Dan

**Prepared:** 2026-05-26 (Session 2 fixup + Session 3 close-out).
**Audience:** Dan Poenaru. **Status:** awaiting decision.
**Decision needed:** run now / run post-Commentary / skip entirely.

---

## The problem

The Session 2 specialty classifier (Haiku 4.5 on 16,759 records, single-best-fit, 18 categories) is the right level of granularity for the Lancet Digital Health Commentary. But it has one structural weakness:

- **25.9% of the corpus** (4,343 records) lands in **`Medical Informatics / Digital Health`** — the bucket reserved for papers *about* AI itself (frameworks, ethics, benchmarks, "AI in medicine" overviews). This bucket has the **2nd-highest critical rate** (44.9%, after Mental Health at 51.3%), but it's internally heterogeneous:
  - Some records are pure-methodology (transformer architectures, dataset construction, benchmark papers).
  - Some are ethics / regulation / governance.
  - Some are cross-cutting clinical-AI overviews that arguably belong in a specific clinical bucket.
- Conversely, every "clinical specialty" record we have (Cardiology, Surgery, Radiology, etc.) is currently *forced* to drop any methodology signal — we can't ask "what % of Cardiology papers are methodology-focused vs. clinical-application?" because we forced single-best-fit.

This is fine for a 1,200-word Commentary. It's a limitation for any longer follow-up paper that wants to:

- Distinguish methodology-driven vs. clinical-application papers within each specialty.
- Sub-split the Medical Informatics bucket into its real internal flavors.
- Re-route mis-classified records (e.g., a paper indexed as "Cardiology" that's really an AI methodology paper using ECG data).

---

## The proposed solution (Option A + Option C, combined)

**Re-classify the same 16,759 records with TWO labels per record instead of one:**

- **Axis 1 — Clinical specialty.** The existing 18 categories from Session 2, *unchanged*. Every analysis we've done remains valid against this axis.
- **Axis 2 — Methodology-focus tag.** A new 4-bucket label applied to *every* record:
  - `methodology` — pure framework / benchmark / dataset / model-architecture paper.
  - `ethics-governance` — regulation, policy, deployment-ethics, deployment-framework paper.
  - `overview` — general "AI in medicine" cross-cutting review / scoping review / bibliometric.
  - `not-applicable` — paper is a clinical-application paper with no methodology / ethics / overview focus (i.e., the standard case for a Cardiology paper *using* AI for a clinical question).

The combination lets us answer the questions a single-axis taxonomy can't:

| Question | Single-axis can answer? | Dual-axis can answer? |
|---|---|---|
| What % of papers are about Cardiology? | ✓ | ✓ |
| What's the critical rate in Cardiology? | ✓ | ✓ |
| What % of Cardiology papers are methodology-focused vs. clinical-application? | ✗ | ✓ |
| Does the critical-stance gap between specialties shrink when we control for methodology focus? | ✗ | ✓ |
| What does the Medical Informatics bucket actually contain? | ✗ | ✓ |
| Are some "Cardiology" papers mis-routed AI-methodology papers? | ✗ | ✓ |

**Option C layer:** use the methodology_tag specifically to sub-split the 4,343 Medical Informatics records into their three real flavors (methodology / ethics-governance / overview), and re-route any Medical Informatics records flagged `not-applicable` into the specialty their content actually targets. (The classifier will still assign a specialty label in axis 1 — we just need to validate it for the Med Info subset.)

---

## What we'd get out of it

1. **A cleaner critical-rate ranking by specialty.** Without methodology-paper contamination, clinical-application critical rates would be more directly comparable across specialties.
2. **A new headline: methodology-focused papers are more critical.** Quantifies how much of every specialty's critical-rate score is driven by methodology-paper subset.
3. **A defensible Medical Informatics breakdown.** Instead of one 25.9% lump, three sub-buckets each with its own critical-rate, temporal trend, and theme profile.
4. **A re-routing pass for mis-classified records.** Small expected effect (probably <5% of the corpus), but methodologically cleaner.
5. **All Session 2 specialty findings remain valid.** Axis 1 is unchanged. Dual-axis is purely additive.

---

## Cost and timeline

| Item | Estimate |
|---|---|
| Haiku 4.5 batch on 16,759 records (50% off list) | **~$11** |
| Batch wall time (Anthropic SLA) | **30–60 min** |
| Code work: extend `SPECIALTY_PROMPT`, parser, output schema | ~30 min |
| Re-run the 6 specialty analyses (A.2, A.3, A.4, A.5, A.6, C.3) with methodology axis as control | ~30 min |
| Write up Medical Informatics sub-split analysis | ~30 min |
| **Total wall time** | **~2.5–3 hours** |
| **Total compute cost** | **~$11** |

---

## Risks

- **Low.** Same classifier framework as the existing Session 2 specialty run (which had 13/16,759 = 0.08% FAILED). Haiku 4.5 has proven reliable on this corpus.
- **No risk to v1 stance classification** (the κ-validated anchor). Dual-axis taxonomy is a *parallel* dataset, not a replacement.
- **No risk to Session 1–3 deliverables.** All current findings remain canonical; this is additive.
- **Only "risk" is opportunity cost** — 2.5–3 hours of session time that could go elsewhere.

---

## Three paths forward

### Path 1 — Run NOW (before Lancet submission)

**Pros:** new findings could strengthen the Commentary, especially around the Medical Informatics bucket and the "methodology papers are more critical" angle.

**Cons:** Commentary is already a tight 1,200 words. Adding new findings forces cuts elsewhere. Risk of bloating the methods section.

**Recommended if:** the Commentary's word budget can absorb a 1–2 sentence finding *and* you specifically want a methodology-vs-clinical-application angle in the manuscript.

### Path 2 — Run POST-Commentary, for the follow-up longer paper (Claude's recommendation)

**Pros:** keeps the Commentary tight on the strongest existing findings. Gives the longer follow-up paper a distinctive analytical angle. Defers spend until we know whether the Commentary lands.

**Cons:** delays the analysis ~2–4 months.

**Recommended if:** the Commentary is targeting the existing Session 1–3 headline findings and you want the follow-up paper to be substantively differentiated, not just longer.

### Path 3 — Skip entirely

**Pros:** zero spend. No additional cognitive load.

**Cons:** the Medical Informatics 25.9% lump remains opaque in any future analysis. Reviewers of the Commentary may ask "what's actually in that bucket?" and we won't have a clean answer.

**Recommended if:** the follow-up paper is unlikely to materialize.

---

## Claude's recommendation

**Path 2 — run post-Commentary.** The Commentary's existing findings (theme inversion, opinion-pieces-more-critical, advocacy collapse, hallucination↑/regulation↓ being universal, East Asia low-critical-rate, reviews look-up vs research look-down) are strong enough to stand without it. The dual-axis taxonomy will give the follow-up paper a structural advantage that's hard to retrofit later.

If Dan prefers Path 1, the ~3-hour cost is manageable; just need to confirm the Commentary word budget can absorb one additional finding.

If Dan prefers Path 3, document the limitation in the Commentary's Methods section as a future-work item.

---

## Reference

Original decision note (Kingsley, 2026-05-26): in `output/analyses/session2_summary.md`, section "Future work — decisions noted → Finer-grained specialty taxonomy (post-Lancet-Commentary)".

Session 2 specialty classifier source: `analysis/classify_specialty.py`.
Session 2 specialty output: `output/specialty_classifications.csv`.
Session 2 specialty analyses: `output/analyses/specialty_critical_*`, `temporal_stance_by_specialty.*`, `themes_by_specialty.*`.
