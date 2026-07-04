"""
TASK CV-1 — Within-genre critical-share trend.

v1 canonical labels; drop FAILED/unparseable; pub_year 2021-2026.
Split the stance-classified records by prefilter genre label
(paper_type: discourse vs evaluative). For each genre compute the yearly
critical share = (Alarm + Caution) / N_year, with percentile bootstrap
95% CIs (n_boot=1000, seed=42). Also compute a descriptive Spearman rho
of critical share vs year for each genre, and the discourse:evaluative
record ratio by year.

Outputs:
  output/revision_checks/cv1_within_genre_trends.csv
  output/revision_checks/cv1_genre_ratio_by_year.csv
  output/revision_checks/cv1_within_genre_trends.png
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

WT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WT))
from analysis.robustness import DATA_DIR, SEED  # noqa: E402

OUT = WT / "output" / "revision_checks"
OUT.mkdir(parents=True, exist_ok=True)

N_BOOT = 1000
YEARS = list(range(2021, 2027))
GENRES = ["discourse", "evaluative"]


def load_v1() -> pd.DataFrame:
    """v1 canonical: drop FAILED, keep parseable stance, pub_year 2021-2026."""
    df = pd.read_csv(DATA_DIR / "classified_medical_Q1Q2.csv", low_memory=False)
    n_total = len(df)
    df = df[df["stance"] != "FAILED"].copy()
    n_after_failed = len(df)
    df["pub_year"] = pd.to_numeric(df["pub_year"], errors="coerce")
    df = df[df["pub_year"].between(2021, 2026)].copy()
    df["pub_year"] = df["pub_year"].astype(int)
    print(f"v1 rows total={n_total}, after drop FAILED={n_after_failed}, "
          f"after 2021-2026 filter={len(df)}")
    # genre label = prefilter paper_type
    df = df[df["paper_type"].isin(GENRES)].copy()
    print(f"after restricting to discourse/evaluative genres={len(df)}")
    return df


def bootstrap_critical_share(vals: np.ndarray, n_boot: int, seed: int):
    """vals = 0/1 array (critical or not). Return (point%, lo%, hi%)."""
    rng = np.random.default_rng(seed)
    n = len(vals)
    point = vals.mean() * 100
    if n == 0:
        return np.nan, np.nan, np.nan
    boot = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, size=n)
        boot[i] = vals[idx].mean() * 100
    lo = np.percentile(boot, 2.5)
    hi = np.percentile(boot, 97.5)
    return point, lo, hi


def main() -> None:
    df = load_v1()
    df["critical"] = df["stance"].isin(["Alarm", "Caution"]).astype(int)

    rows = []
    for genre in GENRES:
        g = df[df["paper_type"] == genre]
        for yr in YEARS:
            gy = g[g["pub_year"] == yr]
            vals = gy["critical"].to_numpy()
            # deterministic per (genre, year) seed derived from SEED
            seed = SEED + hash((genre, yr)) % 10000
            point, lo, hi = bootstrap_critical_share(vals, N_BOOT, seed)
            rows.append({
                "genre": genre,
                "pub_year": yr,
                "n_records": len(gy),
                "n_critical": int(vals.sum()) if len(vals) else 0,
                "critical_share_pct": point,
                "ci_lo_pct": lo,
                "ci_hi_pct": hi,
            })
    trends = pd.DataFrame(rows)
    trends.to_csv(OUT / "cv1_within_genre_trends.csv", index=False)

    # Spearman rho of critical share vs year, per genre (descriptive, n=6 years)
    print("\n=== Spearman rho: yearly critical share vs year (per genre) ===")
    spearman_rows = []
    for genre in GENRES:
        sub = trends[trends["genre"] == genre].sort_values("pub_year")
        rho, p = spearmanr(sub["pub_year"], sub["critical_share_pct"])
        spearman_rows.append({"genre": genre, "spearman_rho": rho,
                              "p_two_sided": p, "n_years": len(sub)})
        print(f"  {genre:<11} rho={rho:+.3f}  p={p:.4f}  "
              f"(share {sub['critical_share_pct'].iloc[0]:.1f}% -> "
              f"{sub['critical_share_pct'].iloc[-1]:.1f}%)")
    pd.DataFrame(spearman_rows).to_csv(
        OUT / "cv1_within_genre_spearman.csv", index=False)

    # Genre ratio by year
    print("\n=== discourse:evaluative ratio by year ===")
    ratio_rows = []
    for yr in YEARS:
        nd = int((df[(df["pub_year"] == yr) & (df["paper_type"] == "discourse")]).shape[0])
        ne = int((df[(df["pub_year"] == yr) & (df["paper_type"] == "evaluative")]).shape[0])
        ratio = nd / ne if ne else np.nan
        ratio_rows.append({"pub_year": yr, "n_discourse": nd,
                           "n_evaluative": ne, "discourse_to_evaluative_ratio": ratio})
        print(f"  {yr}: discourse={nd:>5}  evaluative={ne:>5}  ratio={ratio:.3f}")
    pd.DataFrame(ratio_rows).to_csv(
        OUT / "cv1_genre_ratio_by_year.csv", index=False)

    # Figure
    fig, ax = plt.subplots(figsize=(9, 6))
    colours = {"discourse": "#8E44AD", "evaluative": "#16A085"}
    for genre in GENRES:
        sub = trends[trends["genre"] == genre].sort_values("pub_year")
        x = sub["pub_year"].to_numpy()
        y = sub["critical_share_pct"].to_numpy()
        lo = sub["ci_lo_pct"].to_numpy()
        hi = sub["ci_hi_pct"].to_numpy()
        ax.plot(x, y, "-o", color=colours[genre], label=genre, lw=2, zorder=3)
        ax.fill_between(x, lo, hi, color=colours[genre], alpha=0.18, zorder=1)
    ax.set_xlabel("Publication year", fontsize=11)
    ax.set_ylabel("Critical share (Alarm + Caution), %", fontsize=11)
    ax.set_title("CV-1 — Within-genre critical-share trend (v1, Q1/Q2 medical, 2021-2026)\n"
                 "Bands: percentile bootstrap 95% CI (n=1000, seed=42)",
                 fontsize=11, fontweight="bold")
    ax.set_xticks(YEARS)
    ax.grid(True, ls=":", alpha=0.4)
    ax.legend(title="Prefilter genre", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "cv1_within_genre_trends.png", dpi=300,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"\nSaved: {OUT / 'cv1_within_genre_trends.csv'}")
    print(f"Saved: {OUT / 'cv1_genre_ratio_by_year.csv'}")
    print(f"Saved: {OUT / 'cv1_within_genre_trends.png'}")


if __name__ == "__main__":
    main()
