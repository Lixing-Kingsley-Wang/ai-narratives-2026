"""
TASK CV-2 — Prefilter KEEP-rate audit.

Reconstruct the prefilter KEEP rate within Q1/Q2 over time.
  kept        = discourse + evaluative  (output/prefiltered_discourse_eval.csv)
  denominator = pre-prefilter eligible Q1/Q2 records with a parseable pub_year
                (output/filtered_medical_all_Q1Q2.csv, the prefilter input)
KEEP rate = kept / denominator, by year 2021-2026. Flag monotonic trend.

Specialty arm: specialty labels exist only for KEPT records
(specialty_classifications.csv is an LLM pass over the discourse/evaluative
subset). There is NO committed specialty label at the pre-prefilter denominator
level, so a KEEP rate by specialty is NOT recoverable — this is stated, not
estimated.

Outputs:
  output/revision_checks/cv2_keep_rate_by_year.csv
  (no cv2_keep_rate_by_specialty.csv — denominator not recoverable; see note)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd
from scipy.stats import spearmanr

WT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WT))
from analysis.robustness import DATA_DIR  # noqa: E402

OUT = WT / "output" / "revision_checks"
OUT.mkdir(parents=True, exist_ok=True)

YEARS = list(range(2021, 2027))
_YEAR_RE = re.compile(r"\b(20\d{2})\b")


def extract_year(s: str):
    m = _YEAR_RE.search(s or "")
    return int(m.group(1)) if m else None


def year_counts(csv_path: Path, year_source: str) -> pd.Series:
    """Return per-year record counts, extracting year like prefilter.py does."""
    # read only the column needed for year derivation
    df = pd.read_csv(csv_path, usecols=[year_source], low_memory=False,
                     dtype=str)
    yrs = df[year_source].map(extract_year)
    return yrs.value_counts()


def main() -> None:
    denom_path = DATA_DIR / "filtered_medical_all_Q1Q2.csv"
    kept_path = DATA_DIR / "prefiltered_discourse_eval.csv"

    print("Denominator (pre-prefilter eligible Q1/Q2):", denom_path.name)
    print("Kept (discourse + evaluative):", kept_path.name)

    # Denominator: filtered_medical_all_Q1Q2 has pub_date (no pub_year col).
    denom_by_year = year_counts(denom_path, "pub_date")
    denom_total_raw = int(pd.read_csv(denom_path, usecols=["pub_date"],
                                      dtype=str).shape[0])
    n_denom_noyear = denom_total_raw - int(denom_by_year.sum())

    # Kept: prefiltered_discourse_eval has an explicit pub_year column.
    kept_df = pd.read_csv(kept_path, usecols=["pub_year"], low_memory=False,
                          dtype=str)
    kept_df["yr"] = pd.to_numeric(kept_df["pub_year"], errors="coerce")
    kept_by_year = kept_df["yr"].dropna().astype(int).value_counts()
    kept_total_raw = int(kept_df.shape[0])
    n_kept_noyear = kept_total_raw - int(kept_by_year.sum())

    rows = []
    for yr in YEARS:
        kept = int(kept_by_year.get(yr, 0))
        denom = int(denom_by_year.get(yr, 0))
        rate = kept / denom * 100 if denom else float("nan")
        rows.append({"pub_year": yr, "n_kept": kept,
                     "n_eligible_denominator": denom,
                     "keep_rate_pct": rate})
    out = pd.DataFrame(rows)

    # overall + out-of-window diagnostics appended as summary rows
    overall_kept = int(kept_by_year.reindex(YEARS).fillna(0).sum())
    overall_denom = int(denom_by_year.reindex(YEARS).fillna(0).sum())
    print("\n=== KEEP rate by year (2021-2026) ===")
    for _, r in out.iterrows():
        print(f"  {int(r['pub_year'])}: kept={int(r['n_kept']):>6}  "
              f"eligible={int(r['n_eligible_denominator']):>6}  "
              f"keep_rate={r['keep_rate_pct']:.2f}%")
    print(f"  ALL 2021-2026: kept={overall_kept}  eligible={overall_denom}  "
          f"keep_rate={overall_kept/overall_denom*100:.2f}%")
    print(f"\n  (diagnostics) denominator rows w/o parseable year: {n_denom_noyear}"
          f"  | kept rows w/o parseable year: {n_kept_noyear}")
    print(f"  denominator total rows={denom_total_raw}  kept total rows={kept_total_raw}")

    # Monotonic-trend flag
    rate_series = out.set_index("pub_year")["keep_rate_pct"]
    diffs = rate_series.diff().dropna()
    mono_inc = bool((diffs > 0).all())
    mono_dec = bool((diffs < 0).all())
    rho, p = spearmanr(out["pub_year"], out["keep_rate_pct"])
    trend = ("strictly monotonic INCREASING" if mono_inc else
             "strictly monotonic DECREASING" if mono_dec else
             "non-monotonic")
    print(f"\n  Trend: {trend}; Spearman rho(year, keep_rate)={rho:+.3f}, p={p:.4f}")

    out.to_csv(OUT / "cv2_keep_rate_by_year.csv", index=False)
    print(f"\nSaved: {OUT / 'cv2_keep_rate_by_year.csv'}")

    # ---- Specialty recoverability check -----------------------------------
    spec_path = DATA_DIR / "specialty_classifications.csv"
    print("\n=== KEEP rate by specialty — recoverability ===")
    print(f"specialty_classifications.csv exists: {spec_path.exists()}")
    if spec_path.exists():
        sp = pd.read_csv(spec_path, usecols=lambda c: c in ("pmid", "specialty"),
                         low_memory=False)
        print(f"  rows in specialty file = {len(sp):,} "
              f"(covers KEPT discourse/evaluative records only)")
    print("  NOT RECOVERABLE: no committed specialty label exists at the "
          "pre-prefilter denominator level (the 80,751 dropped 'application' "
          "records + kept records = 97,510). Specialty was classified only on "
          "the 16,759 kept records, so a per-specialty denominator cannot be "
          "formed from committed artifacts. No specialty CSV written.")


if __name__ == "__main__":
    main()
