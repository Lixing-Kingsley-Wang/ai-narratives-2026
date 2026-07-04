# phase2_prophecy_verdicts_worksheet.csv — column guide

Unit of analysis = **one claim per row** (a few papers contribute 2 claims; see `claim_role`).
The model assigns **NO verdict**. Machine columns surface candidate evidence; the human adjudicates.

## Machine-filled (do not edit — provenance)
| column | meaning |
|---|---|
| `claim_id` | `PMID` (primary) or `PMID-2` (secondary claim of a 2-claim paper) |
| `pmid` | source paper PMID (2021–2023 prediction) |
| `claim_role` | `primary` / `secondary` |
| `pub_year` | prediction paper year |
| `tier` | 1 = superiority/replacement · 2 = capability deployment · 3 = diffuse transformation (frozen, blind) |
| `topic`, `horizon` | theme tag; explicit timeframe or `open-ended` |
| `signature_claim` | the frozen prediction being adjudicated |
| `retrieved_pmids_top20` | top-20 evidence PMIDs (2024–2026), `\|`-separated, by MedCPT similarity |
| `top_score` | MedCPT dot-product similarity of the best-matching evidence abstract |
| `corpus_silent` | TRUE if model judged the corpus doesn't address the claim, OR `low_similarity`=TRUE. **TRUE ⇒ defaults to too_early/unfalsifiable, NEVER to not_borne_out.** |
| `low_similarity` | TRUE if `top_score` below the logged p10 threshold (weak best match) |
| `evidence_status_summary` | neutral 2–4 sentence summary grounded ONLY in retrieved abstracts; no verdict |
| `key_evidence` | up to 5 `PMID - finding [outcome\|restatement]` items. Continued advocacy = `[restatement]`, not outcome |

## Human-filled (leave blank for the model; you complete)
| column | how to fill |
|---|---|
| `verdict` | one of `borne_out` · `partially` · `not_borne_out` · `too_early_unfalsifiable`. **`not_borne_out` REQUIRES positive contrary evidence** (a study showing the predicted outcome did not materialize). Corpus silence ⇒ `too_early_unfalsifiable`. |
| `verdict_evidence_pmid` | the specific cited evidence PMID backing your verdict (≥1 per A7) |
| `external_evidence_used` | `none`, or the external source if you used one cited external datum (A5 hard-fact claims) |
| `ambiguous_flag` | `Y`/`N` — mark `partially` and `too_early` calls for Dan's blind spot-check (A7) |
| `adjudicator_note` | free text rationale |

**Iron rule (A4):** absence of evidence is never failure. Only positive contrary evidence yields `not_borne_out`.
