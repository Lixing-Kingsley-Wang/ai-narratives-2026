# S4-4 — Q3 prefilter funnel audit

**Question (Dan):** the analyzed Q3 set is only ~1,000 papers — is Q3 being
excluded at an anomalous rate by the prefilter?

**Verdict: LEGITIMATE — proceed.** Q3's prefilter KEEP rate (19.4%) is
2.2 pp higher than Q1/Q2's
(17.2%). Q3 yields ~1,055 papers simply because the
eligible Q3 journal pool (5,433) is ~18x
smaller than Q1/Q2 (97,492) — not because the prefilter drops Q3
harder.

## Funnel

| Stage | Q1/Q2 | Q3 |
|---|---:|---:|
| raw_medical_all (shared fetch) | 116,117 | 116,117 |
| SJR filter | 97,492 | 5,433 |
| prefilter KEEP (discourse+evaluative) | 16,759 | 1,055 |
| classified | 16,759 | 1,055 |
| **prefilter KEEP rate** | **17.19%** | **19.42%** |

KEEP + DROP reconciles exactly in both arms; prefilter -> classified is 1:1.

## Why this is not a bug

- **Identical criteria.** `prefilter.py` uses a byte-for-byte identical
  `SYSTEM_PROMPT`, KEEP rule (`paper_type in {discourse, evaluative}`), 300-char
  abstract truncation, and model (`claude-haiku-4-5`) for both arms; only the I/O
  filenames differ. No Q1/Q2-specific assumption can misfire on Q3.
- **No fetch truncation.** `fetch_pubmed_medical.py` uses per-month
  `retmax=9,999` with month-splitting and an explicit overflow warning; the raw
  fetch is shared across all quartiles (quartile is assigned later), so it cannot
  truncate Q3 specifically.
- **SJR logic sound.** Per-record journal-title -> publication-year SJR best
  quartile; Q3 -> comparison arm. The duplicate `sjr_quartile.1` column is
  harmless (both values `Q3`, 0 mismatches).

## Caveats

- The four SJR buckets sum to 114,953, 1,164 short of
  the current raw (116,117); the shortfall is entirely partial-year 2026
  records (0 orphans, 0 bucket overlap) — the SJR filter was last run on a
  slightly earlier raw snapshot. Affects both arms proportionally; re-running
  `sjr_filter.py all` would fold them in.
- A false-exclude sample was NOT taken: it is triggered only if Q3's KEEP rate is
  materially lower, which it is not. Any baseline false-exclude rate applies
  equally to the primary Q1/Q2 corpus.
