# Prophecy Panel — notes to fold into the manuscript

Running list of points worth surfacing when writing the panel (Results / Methods / Limitations).

## 1. Tier-1 definition phrasing (Methods)
Use this wording for the Tier-1 (superiority/replacement) definition — it cleanly handles the
"result vs. prophecy" subtlety:

> **Tier 1 — specific superiority / replacement:** "AI will outperform / replace clinicians,
> **or has done so in a way predicted to generalize**."

Source of record: pre-registration **A3** (`~/Downloads/prophecy_panel_preregistration.md:32`).
Why it matters: several Tier-1 papers report an *in-sample* head-to-head result (e.g. "our model
outperformed all 157 dermatologists", PMID 34471174) rather than a future-tense forecast. The
"…or has done so in a way predicted to generalize" clause is what makes a demonstrated superiority
count as a falsifiable *prediction* (the bet is that the result generalizes to practice) — which is
exactly what Phase 2 adjudicates. NB: the Phase-1 system prompt was aligned to this exact wording
(amendment logged in run_manifest.txt).

## 2. Corpus-scope boundary, illustrated (Limitations / Discussion)
PMID 36143468 ("Artificial Intelligence in Biological Sciences") carries an independent **claim 2**:
*"AI… can modify the metabolic pathways of living systems to maximize yield in bio-based industrial
setups."* This is a concrete (Tier-2) mechanism, and it is **non-clinical** (industrial bioprocessing /
metabolic engineering). I initially expected it to fall outside the corpus and return `corpus_silent`
— but **it did not**: the broad medical-AI corpus actually contains adjacent bioprocess/biotech-AI
papers, and Phase 2 retrieved real `[outcome]` evidence (ANN-GA giving a 2.38-fold bacteriocin yield
increase with bioreactor scale-up; ML optimization of biogas/methane yields; 3.76-fold squalene yield
in plant cell cultures). So the claim turned out to be *adjudicable* after all.

The manuscript point is therefore the reverse of what I first assumed, and more interesting: the
corpus is **broader than strictly clinical medicine** (the fetch was the broad medical-AI corpus, not
the discourse-evaluative subset — see the brief), so some ostensibly out-of-scope predictions are in
fact reachable. The A5 structural boundary is real but *softer* than a clean clinical cut-off — worth
stating precisely rather than overclaiming that non-clinical predictions are unadjudicable. (Contrast:
truly niche claims like the 33937332 nanogenomics lab-instrument DID come back `corpus_silent`.)
