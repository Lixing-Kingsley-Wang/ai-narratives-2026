# C.2 — Q1/Q2 vs Q3 comparison

## Status: DEFERRED — Q3 corpus not yet classified with v1/v2 prompts

### What's on disk

- `output/filtered_medical_all_Q3.csv` — 5,433 records, filtered but not classified
- `output/prefiltered_Q3_discourse_eval.csv` — 1,055 records, discourse+evaluative subset (~20% of Q3, mirroring the same prefilter step that produced the 16,759-record Q1/Q2 working set)
- `output/analysis/05_q1q2_vs_q3_stance.csv` — Dan's prior analysis, **superseded** because it was produced from his truncated-abstract pre-v1 classifier ([[project-dans-analyses]])

### Why deferred

The Q3 discourse+evaluative corpus has not been run through `classify_stance_batch.py` with the locked v1 prompt or the v2 robustness prompt. Without those classifications, any Q3-vs-Q1/Q2 comparison would either:

1. **Rely on Dan's superseded numbers** — undermines methodological consistency since v1 is the canonical anchor for every other Session 1 / Session 2 result.
2. **Skip the comparison** — leaves a known limitation in the manuscript.

### Decision needed from Kingsley

Three options for handling this before Lancet Digital Health submission (target mid-Aug 2026):

| Option | Effort | Trade-off |
|---|---|---|
| **A.** Run Sonnet stance classification on the 1,055 Q3 discourse+evaluative records using the v1 prompt | ~30 min compute + ~30 min code reuse | Methodologically clean. Could be done in a Session 3 task. Cost ≈ $10–15. |
| **B.** Report Q1/Q2 results only; cite Dan's prior Q3 comparison as a directional sanity check with caveat | Zero | Honest but invites reviewer question. |
| **C.** Drop Q3 comparison entirely from the manuscript | Zero | Leaves out a useful generalizability check. |

The script `compare_q3.py` (parent checkout) already implements the structural comparison logic; it just needs a v1-classified Q3 file to read from. The cleanest path is Option A.

### Files generated this session

None — this is a status note only.
