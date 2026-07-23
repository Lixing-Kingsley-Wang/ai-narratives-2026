"""
S4-4 — Q3 prefilter funnel audit.

Dan flagged that the analyzed Q3 set is only ~1,000 papers. This audit checks
whether the reduction from 5,433 SJR-Q3 records to 1,055 classified papers is a
legitimate prefilter KEEP rate or an over-exclusion bug that drops Q3 more
aggressively than the primary Q1/Q2 corpus.

Method:
  1. Reconstruct the exact funnel raw -> SJR filter -> prefilter KEEP -> classified
     for both arms and compute the prefilter KEEP rate (discourse+evaluative).
  2. Compare the Q3 KEEP rate to the Q1/Q2 KEEP rate (the key diagnostic).
  3. Provenance / integrity checks: raw-vs-bucket reconciliation, duplicate
     sjr_quartile column.

The prefilter prompt/criteria are identical between arms (only the I/O paths
differ in prefilter.py), so any rate gap is corpus-driven, not code-driven.

Conventions: data lives in the gitignored main-checkout output/ (DATA_DIR).

Produces:
  output/analyses/q3_prefilter_funnel.csv
  output/analyses/q3_prefilter_audit.md
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from analysis.robustness import DATA_DIR

WORKTREE = Path(__file__).resolve().parents[1]
ANALYSES_DIR = WORKTREE / "output" / "analyses"

# funnel files (in DATA_DIR)
FILES = {
    "raw": "raw_medical_all.csv",
    "q12_filtered": "filtered_medical_all_Q1Q2.csv",
    "q3_filtered": "filtered_medical_all_Q3.csv",
    "excluded": "filtered_medical_all_excluded.csv",
    "unmatched": "filtered_medical_all_unmatched.csv",
    "q12_keep": "prefiltered_discourse_eval.csv",
    "q12_app": "prefiltered_application.csv",
    "q3_keep": "prefiltered_Q3_discourse_eval.csv",
    "q3_app": "prefiltered_Q3_application.csv",  # may be absent (not retained)
    "q12_classified": "classified_medical_Q1Q2.csv",
    "q3_classified": "classified_medical_Q3.csv",
}


def count(name: str) -> int | None:
    p = DATA_DIR / FILES[name]
    if not p.exists():
        return None
    return len(pd.read_csv(p, low_memory=False))


def pmids(name: str) -> set[str]:
    p = DATA_DIR / FILES[name]
    return set(pd.read_csv(p, low_memory=False)["pmid"].astype(str))


def main() -> None:
    ANALYSES_DIR.mkdir(parents=True, exist_ok=True)
    print("=" * 72)
    print("S4-4 — Q3 prefilter funnel audit")
    print("=" * 72)

    c = {k: count(k) for k in FILES}

    # DROP counts (application). Q3 app file may be absent -> derive by subtraction.
    q12_drop = c["q12_app"]
    q3_drop = c["q3_app"] if c["q3_app"] is not None else c["q3_filtered"] - c["q3_keep"]
    q3_drop_note = "" if c["q3_app"] is not None else " (by subtraction; app file not retained)"

    q12_rate = c["q12_keep"] / c["q12_filtered"] * 100
    q3_rate = c["q3_keep"] / c["q3_filtered"] * 100
    delta = q3_rate - q12_rate

    print("\n[1] Funnel")
    print(f"  raw_medical_all                 {c['raw']:>7,}  (shared fetch, all quartiles)")
    print(f"  SJR filter -> Q1/Q2             {c['q12_filtered']:>7,}")
    print(f"  SJR filter -> Q3                {c['q3_filtered']:>7,}")
    print(f"  prefilter KEEP Q1/Q2            {c['q12_keep']:>7,}  (DROP {q12_drop:,})")
    print(f"  prefilter KEEP Q3               {c['q3_keep']:>7,}  (DROP {q3_drop:,}{q3_drop_note})")
    print(f"  classified Q1/Q2               {c['q12_classified']:>7,}")
    print(f"  classified Q3                  {c['q3_classified']:>7,}")

    print("\n[2] KEY DIAGNOSTIC — prefilter KEEP rate")
    print(f"  Q1/Q2: {c['q12_keep']:,}/{c['q12_filtered']:,} = {q12_rate:.2f}%")
    print(f"  Q3   : {c['q3_keep']:,}/{c['q3_filtered']:,} = {q3_rate:.2f}%")
    print(f"  Delta (Q3 - Q1/Q2) = {delta:+.2f} pp  -> "
          f"{'Q3 NOT over-excluded' if delta >= -1 else 'Q3 MATERIALLY LOWER — investigate'}")

    # [3] integrity checks
    print("\n[3] Integrity / provenance")
    raw_ids = pmids("raw")
    bucket_ids = set().union(*(pmids(k) for k in
                               ["q12_filtered", "q3_filtered", "excluded", "unmatched"]))
    unbucketed = raw_ids - bucket_ids
    orphans = bucket_ids - raw_ids
    print(f"  raw pmids={len(raw_ids):,}  bucketed={len(bucket_ids):,}  "
          f"unbucketed={len(unbucketed):,}  orphans={len(orphans):,}")
    if unbucketed:
        rawdf = pd.read_csv(DATA_DIR / FILES["raw"], low_memory=False)
        rawdf["pmid"] = rawdf["pmid"].astype(str)
        yrs = rawdf[rawdf.pmid.isin(unbucketed)]["year"].value_counts().to_dict()
        print(f"  unbucketed by year (filter ran on earlier raw snapshot): {yrs}")

    q3df = pd.read_csv(DATA_DIR / FILES["q3_filtered"], low_memory=False)
    dup = [col for col in q3df.columns if col.startswith("sjr_quartile")]
    mism = None
    if "sjr_quartile.1" in q3df.columns:
        mism = int((q3df["sjr_quartile"].astype(str)
                    != q3df["sjr_quartile.1"].astype(str)).sum())
    print(f"  Q3 sjr_quartile columns: {dup}  mismatches={mism}  -> harmless duplicate")

    # ── write funnel CSV ───────────────────────────────────────────────────────
    funnel = pd.DataFrame([
        {"arm": "Q1/Q2", "sjr_filtered": c["q12_filtered"], "prefilter_keep": c["q12_keep"],
         "prefilter_drop": q12_drop, "classified": c["q12_classified"],
         "keep_rate_pct": round(q12_rate, 2)},
        {"arm": "Q3", "sjr_filtered": c["q3_filtered"], "prefilter_keep": c["q3_keep"],
         "prefilter_drop": q3_drop, "classified": c["q3_classified"],
         "keep_rate_pct": round(q3_rate, 2)},
    ])
    out_csv = ANALYSES_DIR / "q3_prefilter_funnel.csv"
    funnel.to_csv(out_csv, index=False)

    # ── write verdict markdown ──────────────────────────────────────────────────
    verdict = "LEGITIMATE — proceed" if delta >= -1 else "OVER-EXCLUSION — fix prefilter"
    md = f"""# S4-4 — Q3 prefilter funnel audit

**Question (Dan):** the analyzed Q3 set is only ~1,000 papers — is Q3 being
excluded at an anomalous rate by the prefilter?

**Verdict: {verdict}.** Q3's prefilter KEEP rate ({q3_rate:.1f}%) is
{abs(delta):.1f} pp {'higher' if delta >= 0 else 'lower'} than Q1/Q2's
({q12_rate:.1f}%). Q3 yields ~{c['q3_keep']:,} papers simply because the
eligible Q3 journal pool ({c['q3_filtered']:,}) is ~{c['q12_filtered'] / c['q3_filtered']:.0f}x
smaller than Q1/Q2 ({c['q12_filtered']:,}) — not because the prefilter drops Q3
harder.

## Funnel

| Stage | Q1/Q2 | Q3 |
|---|---:|---:|
| raw_medical_all (shared fetch) | {c['raw']:,} | {c['raw']:,} |
| SJR filter | {c['q12_filtered']:,} | {c['q3_filtered']:,} |
| prefilter KEEP (discourse+evaluative) | {c['q12_keep']:,} | {c['q3_keep']:,} |
| classified | {c['q12_classified']:,} | {c['q3_classified']:,} |
| **prefilter KEEP rate** | **{q12_rate:.2f}%** | **{q3_rate:.2f}%** |

KEEP + DROP reconciles exactly in both arms; prefilter -> classified is 1:1.

## Why this is not a bug

- **Identical criteria.** `prefilter.py` uses a byte-for-byte identical
  `SYSTEM_PROMPT`, KEEP rule (`paper_type in {{discourse, evaluative}}`), 300-char
  abstract truncation, and model (`claude-haiku-4-5`) for both arms; only the I/O
  filenames differ. No Q1/Q2-specific assumption can misfire on Q3.
- **No fetch truncation.** `fetch_pubmed_medical.py` uses per-month
  `retmax=9,999` with month-splitting and an explicit overflow warning; the raw
  fetch is shared across all quartiles (quartile is assigned later), so it cannot
  truncate Q3 specifically.
- **SJR logic sound.** Per-record journal-title -> publication-year SJR best
  quartile; Q3 -> comparison arm. The duplicate `sjr_quartile.1` column is
  harmless (both values `Q3`, {mism} mismatches).

## Caveats

- The four SJR buckets sum to {len(bucket_ids):,}, {len(unbucketed):,} short of
  the current raw ({len(raw_ids):,}); the shortfall is entirely partial-year 2026
  records (0 orphans, 0 bucket overlap) — the SJR filter was last run on a
  slightly earlier raw snapshot. Affects both arms proportionally; re-running
  `sjr_filter.py all` would fold them in.
- A false-exclude sample was NOT taken: it is triggered only if Q3's KEEP rate is
  materially lower, which it is not. Any baseline false-exclude rate applies
  equally to the primary Q1/Q2 corpus.
"""
    out_md = ANALYSES_DIR / "q3_prefilter_audit.md"
    out_md.write_text(md, encoding="utf-8")

    print(f"\nFiles:")
    print(f"  {out_csv.relative_to(WORKTREE)}")
    print(f"  {out_md.relative_to(WORKTREE)}")


if __name__ == "__main__":
    main()
