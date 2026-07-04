# Prophecy Panel — session summary (for Methods & Results drafting)

Detailed record of what was built and found, 2026-06-30/07-01. Numbers are exact. Intended as raw
material for the Methods and Results sections; cherry-pick as needed. Pre-registration = Part A of
`prophecy_panel_preregistration.md` (frozen before adjudication).

---

## 1. Objective and framing
Exploratory **forward-validation** of the AI/LLM discourse's earlier predictions against the subsequent
published record. Organizing axis is **falsifiability**, not optimism: not "were optimists right?" but
"of the predictions specific enough to be tested, which were borne out?" Closing analysis operationalizing,
at the level of individual claims, the corpus-level finding that Advocacy collapsed. Protective framing:
we adjudicate whether the discourse's predictions were borne out **in the published record**, not whether
the underlying AI "works"; verdicts describe the state of the literature at the evidence cutoff.

## 2. Inputs
- **Candidate pool:** 92 records = (stance = Advocacy) ∧ (pub_year ∈ 2021–2023) ∧ (predictive_claim = yes),
  as labelled by the v1 Sonnet stance classifier. Columns: pmid, pub_year, journal, pub_type_simple_5,
  specialty, title, abstract. **27 of 92 are title-only** (empty abstract).
- **Evidence corpus:** `filtered_medical_all_Q1Q2.csv`, 97,492 records (2021–Apr 2026), the **broad**
  medical-AI corpus (deliberately not the discourse-evaluative subset, because deployment/validation
  evidence lives in application papers). Evidence cutoff **April 2026** (fetched 2026-05-09; PubMed
  `[PDAT] ≤ 2026-04` + post-fetch month filter). Year column is `year`. 2026 = Jan–Apr only, partially
  indexed (~10.8k records).
- **Design invariants:** (i) Phase 1 is **blind to reality** — tier/flag from the 2021–2023 paper's own
  text only; (ii) Phase 2 evidence comes **only** from the retrieved 2024–2026 corpus; (iii) the model
  **never assigns a verdict** — a human does; (iv) embeddings are **local** (no external embedding API).

---

## 3. PHASE 1 — claim extraction, flag validation, tiering (blind)

**Method.** For each of the 92 candidates, a frozen Sonnet classifier (`claude-sonnet-4-6`,
temperature = 0, max_tokens = 700, concurrency 5, seed 20260630; system-prompt SHA logged) was given
**only** the paper's own title + abstract (title-only records judged from title alone) and returned strict
JSON with: `flag_confirmed` {yes,no} + one-line reason; `signature_claim` (single most specific/falsifiable
prediction, verbatim-or-close) + optional `signature_claim_2` (only for a genuinely independent second
major bet); `tier`; `topic`; `horizon`. An explicit blindness instruction forbade use of any post-2023
knowledge; tier is a function of **claim structure**, never of known outcome.

**Frozen tier taxonomy (pre-registration A3):**
- **Tier 1 — specific superiority / replacement:** testable head-to-head or displacement — "AI will
  outperform/replace clinicians, **or has done so in a way predicted to generalize**." Highest falsifiability.
- **Tier 2 — capability deployment:** a concrete mechanism entering clinical use / drug development / workflow.
- **Tier 3 — diffuse transformation:** "revolutionize / paradigm shift / next frontier," no mechanism, no horizon.
- Tie-breakers: any concrete testable element ⇒ not Tier 3; a benchmark/comparison against humans ⇒ Tier 1.

**Machine pre-pass result (before human review):** 84/92 flag-confirmed (machine flag precision 0.913);
tiers T1 = 9, T2 = 33, T3 = 42; 27 title-only (24 confirmed, 3 rejected); 0 API failures.

### 3a. Human review gate (the key integrity step)
Every record was manually inspected in a dropdown workbook (machine values preserved read-only for audit;
**full source abstract shown** alongside the extracted claim). Reviewer confirmed/corrected each
`flag_confirmed`, `signature_claim`, `tier`, and deleted false positives.
- **Result: 74 kept / 18 deleted.** Post-review flag precision = **74/92 = 0.804.**
- **False-positive pattern:** a large share of deletions were records (concentrated in the title-only set,
  as pre-registered) where the classifier **hallucinated a forward-looking "will"** not present in the
  source — i.e. manufactured a prediction from a descriptive/retrospective title. This is the precise
  failure the blind human gate exists to catch, and is itself reportable (the unvalidated v1 flag
  over-generated predictions on thin text).
- **Data-integrity catch:** one signature-claim cell (PMID 33937332, a breast-cancer nanogenomics paper)
  had been accidentally contaminated with another record's text (PMID 33529363, an epilepsy paper); a
  full row-by-row diff confirmed it was an isolated single-cell error (no systematic misalignment), and
  the original on-topic claim was restored before freezing.

### 3b. Unit of analysis = claim (not paper)
Per pre-registration A2, the unit is the single signature prediction per paper, with genuinely independent
secondary claims entered as separate, explicitly-flagged rows. **4 papers** carried a genuinely independent
second bet and were split into two claims each (`claim_role` primary/secondary, `claim_id` = PMID / PMID-2);
the reviewer applied a "genuinely independent, not a restatement" test (several machine-proposed secondaries
were dropped as restatements). Two demonstrated-superiority papers (PMIDs 32767299, 37489981) whose forward
bet had been captured as an in-sample *result* were reworded to retain the human head-to-head, keeping the
Tier-1 label and the retrieval query coherent (per the A3 "…predicted to generalize" clause).

**Frozen output:** `phase1_signature_claims_FROZEN.csv`, claim-level. **74 papers → 78 claims.**
Frozen tier distribution: **T1 = 7, T2 = 36, T3 = 35.**

---

## 4. PHASE 2 — RAG evidence retrieval + neutral status summary

### 4a. Evidence corpus
From the broad corpus, kept records with `year ∈ {2024, 2025, 2026}` AND a non-empty abstract.
In-window rows = 59,002 (2024 = 19,372; 2025 = 28,873; 2026 = 10,757); after the abstract filter =
**58,203** evidence abstracts. The 2021–2023 prediction papers are excluded automatically by the year filter.

### 4b. Embedding (MedCPT, local)
Encoders and conventions were confirmed from the official NCBI model cards, not assumed:
- **Query-Encoder** (`ncbi/MedCPT-Query-Encoder`): each signature claim tokenized at `max_length = 64`,
  truncation+padding, embedding = CLS token (`last_hidden_state[:,0,:]`), 768-dim.
- **Article-Encoder** (`ncbi/MedCPT-Article-Encoder`): each abstract as a `[title, abstract]` pair,
  `max_length = 512`, truncation+padding, CLS pooling.
- **Similarity:** dot product of CLS embeddings. (The model card does not state a metric; dot product was
  chosen consistent with MedCPT's contrastive inner-product training and NCBI's own retrieval examples;
  raw embeddings are cached so cosine is recomputable.) Seeds (torch, numpy) = 20260630; device = Apple
  MPS. All 58,203 article embeddings computed once (~1h29m on an M2) and cached to `.npy` (58,203 × 768);
  re-runs are instant.

### 4c. Retrieval
For each of the 78 claims, top-**k = 20** evidence abstracts by dot-product similarity; pmids + scores
stored. (k = 20 favours recall because a human verifies downstream.)

### 4d. Neutral status summary (Sonnet)
Each claim + its 20 retrieved abstracts passed to `claude-sonnet-4-6` (temperature 0) under a **strictly
neutral** instruction (verbatim from the protocol): a 2–4 sentence summary of the prediction's real-world
status **using only the provided abstracts**; **no** statement of right/wrong and **no** verdict; explicit
separation of **[outcome]** evidence (a study reporting what actually happened — deployment, validation,
head-to-head result, workforce/market fact) from **[restatement]** (a later paper merely repeating the
prediction/advocacy — "continued advocacy is not evidence the prediction came true"); a statement that the
corpus is silent if the abstracts do not address the claim; and up to 5 cited `PMID — finding` items each
tagged. Output columns are machine-filled; the human verdict columns are left blank.

**`corpus_silent`** = the model judged nothing relevant **OR** the claim's top retrieval score fell below a
data-driven threshold (10th percentile of top-scores = 63.7; top-score distribution min 60.7 / median 66.1
/ max 70.0). Per pre-registration A4 this maps downstream to **too-early/unfalsifiable, never to not-borne-out.**

**Phase 2 result:** 78 claims summarized, **9 `corpus_silent`** (T1 = 0, T2 = 8, T3 = 1), 0 API failures.
Retrieval quality spot-checks: melanoma-superiority claim → top hits all dermoscopic-melanoma DL papers;
context-aware-chatbot (accGPT) claim → top hit a context-aware-chatbot-vs-radiologist study; a highly
specific newborn-hip-ultrasound claim initially drifted toward generic "AI-vs-physician" papers but top-20
recall + the neutral summary correctly surfaced the one relevant hip-dysplasia study and flagged the rest as
non-responsive; a non-clinical industrial-bioprocess claim (metabolic-pathway yield) unexpectedly retrieved
genuine adjacent bioprocess-AI outcome evidence, showing the broad corpus reaches somewhat beyond strictly
clinical medicine.

---

## 5. Human adjudication + verdict results

Verdicts assigned by the primary rater in a dropdown workbook (rubric A4: `borne_out`, `partially`,
`not_borne_out`, `too_early_unfalsifiable`), each carrying ≥1 cited `verdict_evidence_pmid`.

**Iron rule (A4):** corpus silence ⇒ `too_early_unfalsifiable`; `not_borne_out` **requires positive
contrary evidence**; absence of evidence is never failure. **Automated integrity checks passed:** no
`corpus_silent` row marked `not_borne_out`; all 8 `not_borne_out` cite contrary-evidence pmids; all
`borne_out`/`partially` cite evidence; `external_evidence_used` = none for all 78 (fully closed-loop,
internal-corpus-only adjudication).

**Verdict totals (N = 78):** partially borne out **54**, too early/unfalsifiable **14**, not borne out **8**,
borne out **2**.

**Tier × verdict matrix:**

| Tier (n) | borne_out | partially | not_borne_out | too_early_unfalsifiable |
|---|---|---|---|---|
| Tier 1 — superiority/replacement (7) | 0 | 1 | **5** | 1 |
| Tier 2 — capability deployment (36) | 2 | 23 | 1 | 10 |
| Tier 3 — diffuse transformation (35) | 0 | 30 | 2 | 3 |
| **Total** | **2** | **54** | **8** | **14** |

**Headline findings:**
1. **The most falsifiable claims failed most.** 5 of 7 Tier-1 specific-superiority/replacement predictions
   were `not_borne_out` — the single thickest flow in the figure — while decisive `borne_out` is vanishingly
   rare (2/78, both Tier 2). This is the claim-level operationalization of the corpus-level "Advocacy collapsed."
2. **Most predictions were partially borne out (54/78 ≈ 69%)** — the direction realized but narrower, weaker,
   or slower than claimed. Over-promising on magnitude/timeline, not wholesale wrongness, is the dominant pattern.
3. **Diffuse Tier-3 claims largely escape adjudication as "borne out"** — 30/35 land `partially` (the neutral
   summaries flag much of their supporting literature as `[restatement]` rather than `[outcome]`), consistent
   with low falsifiability by construction.
4. Illustrative Tier-1 case: a 2021 "our deep-CNN outperforms all 157 dermatologists" claim was adjudicated
   `partially` — 2024–2026 meta-analyses confirm DL is comparable-to-slightly-better than dermatologists
   (direction realized), but no study validated that specific model or the "beats every dermatologist"
   magnitude.

**Second-rater plan (A7):** the ambiguous subset for D.P.'s blind spot-check = `partially` + `too_early`
= **68 claims**; raw agreement to be reported in one sentence. No formal κ (small, ordinal, uninformative).

---

## 6. Visualization (A8)
`prophecy_sankey.svg` — tier → verdict Sankey: 3 tier nodes (left) → 4 verdict nodes (right), node height ∝ n,
**every ribbon width ∝ its count and labelled**, tier nodes on a falsifiability gradient (Tier 1 darkest →
Tier 3 lightest), ribbons coloured by destination verdict with the three dominant flows emphasized
(Tier 1→Not borne out, Tier 2→Too early, Tier 3→Partially) and secondary flows muted. Vector, Illustrator-editable.

## 7. Reproducibility
`run_manifest.txt` logs, per stage: model + exact settings, MedCPT model revisions, pooling/max-length/
similarity convention and rationale, torch/numpy seeds, system-prompt SHA, evidence-corpus row count,
evidence cutoff, all counts, and a dated protocol amendment (Tier-1 wording aligned to prereg: "claimed"→
"predicted to generalize"). Embeddings cached to `.npy`; full `pip freeze` recorded.

## 8. Pre-committed + observed limitations
- Exploratory; small N; verdicts involve subjective judgment; single primary rater (mitigated by per-claim
  cited evidence + blind second-rater coding of the ambiguous subset).
- **Advocacy-only scope** supports "optimists over-promised"; it does **not** support a symmetric "critics
  were vindicated."
- The `predictive_claim` flag was **unvalidated at classification time**, validated only post-hoc
  (precision 0.804); false positives concentrated in title-only records and in hallucinated forward framing.
- Internal-corpus evidence reflects **what was published**, not ground-truth capability.
- **Evidence truncation:** 2026 covers only Jan–Apr and is partially indexed (~10.8k); late-horizon
  predictions are adjudicated against an incomplete record and lean `too_early` (stated limitation, not a bug).
- **Result-vs-prophecy nuance:** several Tier-1 claims are in-sample results reframed as generalizing bets
  under the A3 "…predicted to generalize" clause; this reframing is documented, not silent.
- **Corpus-scope boundary is softer than assumed:** the broad medical-AI corpus reaches some adjacent
  non-clinical domains (e.g. an industrial-bioprocess claim still retrieved genuine outcome evidence).

## 9. Deliverables / file inventory (`output/analyses/prophecy/`)
- `prophecy_panel_candidates_2021_2023.csv` — 92-candidate input (provenance copy)
- `phase1_signature_claims_for_review.csv` / `.xlsx` — machine pre-pass + human review workbook
- `phase1_signature_claims_FROZEN.csv` — 78 frozen claims (claim-level)
- `embeddings/*.npy` (+ `evidence_meta.json`) — cached MedCPT vectors (58,203 articles) + 78 claim vectors
- `phase2_retrieval.csv` — top-20 pmids + scores per claim
- `phase2_prophecy_verdicts_worksheet.csv` / `.xlsx` — adjudication worksheet (verdicts filled) + column guide
- `phase2_raw_summaries.jsonl` — raw model JSON (audit trail)
- `prophecy_sankey.svg` — primary exhibit
- `run_manifest.txt` — full reproducibility manifest
- `WRITING_NOTES.md` — running manuscript notes
- Pipeline code (repo root, branch `prophecy-panel`): `prophecy_phase1_extract_claims.py`,
  `prophecy_phase1_build_review_xlsx.py`, `prophecy_phase1_freeze_from_xlsx.py`,
  `prophecy_phase2_embed_retrieve.py`, `prophecy_phase2_summarize.py`,
  `prophecy_phase2_build_verdict_xlsx.py`, `prophecy_sankey.py`
