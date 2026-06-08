"""
S4-5 — Is Q3's lower critical rate composition (more reviews) or within-type?

Q3 medical journals are less critical (Alarm+Caution) than Q1/Q2. This script
decomposes the gap into (a) publication-type composition (Q3 may carry more
Reviews / fewer Editorials) vs (b) a genuine within-type difference (Q3 less
critical inside each pub-type).

Method (mirrors the East Asia composition diagnostic, run_east_asia_diagnose):
  - Bucket raw multi-label pub_type into the session-1 5-bucket scheme via the
    shared analysis.robustness.simplify_pubtype_5 (identical map for both arms).
  - Direct standardization: reweight Q3's per-pub-type critical rates by Q1/Q2's
    pub-type mix -> mix-adjusted Q3 rate.
  - % of the Q3-(Q1/Q2) gap explained by composition =
        (adjusted_Q3 - raw_Q3) / (raw_Q1Q2 - raw_Q3) * 100

Conventions: drop FAILED, pub_year 2021-2026, bootstrap n=1000 seed=42 95% CI.

Produces:
  output/analyses/q3_pubtype_mix.csv
  output/figures/q3_pubtype_mix.png  (300 dpi)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analysis.robustness import (
    DATA_DIR,
    PUBTYPE_BUCKETS_5,
    SEED,
    bootstrap_ci,
    simplify_pubtype_5,
)

WORKTREE = Path(__file__).resolve().parents[1]
ANALYSES_DIR = WORKTREE / "output" / "analyses"
FIGURES_DIR = WORKTREE / "output" / "figures"

Q3_PATH = DATA_DIR / "classified_medical_Q3.csv"
Q12_PATH = DATA_DIR / "classified_medical_Q1Q2.csv"

CRITICAL = ["Alarm", "Caution"]


def load_arm(path: Path) -> pd.DataFrame:
    """Load a classified corpus; drop FAILED, restrict to 2021-2026, bucket pub_type."""
    df = pd.read_csv(path, low_memory=False)
    # Q3 file carries a duplicate pub_year.1; use the canonical pub_year.
    df = df[df["stance"] != "FAILED"].copy()
    df["pub_year"] = pd.to_numeric(df["pub_year"], errors="coerce").astype("Int64")
    df = df[(df["pub_year"] >= 2021) & (df["pub_year"] <= 2026)].copy()
    df["pub_type_simple_5"] = df["pub_type"].fillna("").map(simplify_pubtype_5)
    return df


def critical_rate(df: pd.DataFrame) -> float:
    return df["stance"].isin(CRITICAL).mean() * 100


def pubtype_mix(df: pd.DataFrame) -> pd.Series:
    """Proportion of records in each pub-type bucket."""
    return (df["pub_type_simple_5"].value_counts(normalize=True)
            .reindex(PUBTYPE_BUCKETS_5).fillna(0.0))


def critical_by_pubtype(df: pd.DataFrame) -> pd.Series:
    g = df.groupby("pub_type_simple_5")["stance"].apply(
        lambda s: s.isin(CRITICAL).mean() * 100)
    return g.reindex(PUBTYPE_BUCKETS_5)


def main() -> None:
    ANALYSES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 72)
    print("S4-5 — Q3 vs Q1/Q2 critical rate: composition or within-type?")
    print("=" * 72)

    q3 = load_arm(Q3_PATH)
    q12 = load_arm(Q12_PATH)
    print(f"Q3   records (2021-2026, FAILED dropped): {len(q3):,}")
    print(f"Q1/Q2 records (2021-2026, FAILED dropped): {len(q12):,}")

    # ── [2] distribution + within-type critical rate ──────────────────────────
    mix_q3 = pubtype_mix(q3)
    mix_q12 = pubtype_mix(q12)
    n_q3 = q3["pub_type_simple_5"].value_counts().reindex(PUBTYPE_BUCKETS_5).fillna(0).astype(int)
    n_q12 = q12["pub_type_simple_5"].value_counts().reindex(PUBTYPE_BUCKETS_5).fillna(0).astype(int)
    crit_q3 = critical_by_pubtype(q3)
    crit_q12 = critical_by_pubtype(q12)

    print("\n[2] Pub-type distribution & within-type critical (A+C) rate")
    print(f"  {'pub_type':<17}{'Q3 share':>9}{'Q1/Q2 share':>13}"
          f"{'Q3 crit%':>10}{'Q1/Q2 crit%':>13}{'within Δ':>10}")
    for pt in PUBTYPE_BUCKETS_5:
        wdelta = crit_q3[pt] - crit_q12[pt]
        c3 = f"{crit_q3[pt]:.1f}" if pd.notna(crit_q3[pt]) else "  n/a"
        c12 = f"{crit_q12[pt]:.1f}" if pd.notna(crit_q12[pt]) else "  n/a"
        wd = f"{wdelta:+.1f}" if pd.notna(wdelta) else "  n/a"
        print(f"  {pt:<17}{mix_q3[pt]*100:>8.1f}%{mix_q12[pt]*100:>12.1f}%"
              f"{c3:>10}{c12:>13}{wd:>10}  (n_Q3={n_q3[pt]:,})")

    # ── [3] mix-adjustment (direct standardization to Q1/Q2 pub-type mix) ──────
    raw_q3 = critical_rate(q3)
    raw_q12 = critical_rate(q12)
    # reweight Q3's within-type rates by Q1/Q2's mix; fill empty Q3 cells with
    # Q3's overall rate (no information to do otherwise).
    aligned = crit_q3.reindex(PUBTYPE_BUCKETS_5).fillna(raw_q3)
    adjusted_q3 = float((aligned / 100 * mix_q12).sum() * 100)

    gap = raw_q12 - raw_q3
    explained_pp = adjusted_q3 - raw_q3
    composition_pct = explained_pp / gap * 100 if gap else float("nan")
    within_pct = 100 - composition_pct

    print("\n[3] Mix-adjustment (Q3 within-type rates @ Q1/Q2 pub-type mix)")
    print(f"  raw Q3            : {raw_q3:.2f}%")
    print(f"  raw Q1/Q2         : {raw_q12:.2f}%")
    print(f"  mix-adjusted Q3   : {adjusted_q3:.2f}%")
    print(f"  total gap (Q1/Q2 - Q3) : {gap:.2f} pp")
    print(f"  explained by composition: {explained_pp:.2f} pp  = {composition_pct:.0f}%")
    print(f"  residual within-type    : {gap - explained_pp:.2f} pp  = {within_pct:.0f}%")

    # bootstrap CI on the three headline rates
    ci_raw_q3 = bootstrap_ci(q3, critical_rate)
    ci_raw_q12 = bootstrap_ci(q12, critical_rate)

    def adj_fn(d: pd.DataFrame) -> float:
        cr = critical_by_pubtype(d).reindex(PUBTYPE_BUCKETS_5).fillna(critical_rate(d))
        return float((cr / 100 * mix_q12).sum() * 100)  # fixed Q1/Q2 standard mix

    ci_adj = bootstrap_ci(q3, adj_fn, seed=SEED)
    print(f"\n  95% CIs: raw Q3 [{ci_raw_q3['lower']:.1f}, {ci_raw_q3['upper']:.1f}]  "
          f"raw Q1/Q2 [{ci_raw_q12['lower']:.1f}, {ci_raw_q12['upper']:.1f}]  "
          f"adj Q3 [{ci_adj['lower']:.1f}, {ci_adj['upper']:.1f}]")

    verdict = ("COMPOSITION-DOMINATED" if composition_pct >= 60 else
               "WITHIN-TYPE-DOMINATED" if composition_pct <= 40 else
               "MIXED")
    print(f"\n  VERDICT: {verdict} "
          f"(composition {composition_pct:.0f}% / within-type {within_pct:.0f}%)")

    # ── [4] table out ─────────────────────────────────────────────────────────
    rows = []
    for pt in PUBTYPE_BUCKETS_5:
        rows.append({
            "pub_type": pt,
            "q3_n": int(n_q3[pt]), "q12_n": int(n_q12[pt]),
            "q3_share_pct": round(mix_q3[pt] * 100, 2),
            "q12_share_pct": round(mix_q12[pt] * 100, 2),
            "q3_critical_pct": round(crit_q3[pt], 2) if pd.notna(crit_q3[pt]) else None,
            "q12_critical_pct": round(crit_q12[pt], 2) if pd.notna(crit_q12[pt]) else None,
        })
    rows.append({
        "pub_type": "ALL", "q3_n": len(q3), "q12_n": len(q12),
        "q3_share_pct": 100.0, "q12_share_pct": 100.0,
        "q3_critical_pct": round(raw_q3, 2), "q12_critical_pct": round(raw_q12, 2),
    })
    out_csv = ANALYSES_DIR / "q3_pubtype_mix.csv"
    pd.DataFrame(rows).to_csv(out_csv, index=False)

    # summary row appended as a second small file is overkill; keep headline in print.

    # ── [4] figure ────────────────────────────────────────────────────────────
    fig, (axL, axR) = plt.subplots(
        1, 2, figsize=(13, 5.5), gridspec_kw={"width_ratios": [2.3, 1]})

    # left: grouped bars of pub-type distribution
    x = np.arange(len(PUBTYPE_BUCKETS_5))
    w = 0.38
    axL.bar(x - w / 2, mix_q12.values * 100, w, label="Q1/Q2", color="#2980B9", alpha=0.9)
    axL.bar(x + w / 2, mix_q3.values * 100, w, label="Q3", color="#C0392B", alpha=0.9)
    for j, pt in enumerate(PUBTYPE_BUCKETS_5):
        axL.text(x[j] - w / 2, mix_q12[pt] * 100 + 0.8, f"{mix_q12[pt]*100:.0f}%",
                 ha="center", fontsize=8, color="#1c5a86")
        axL.text(x[j] + w / 2, mix_q3[pt] * 100 + 0.8, f"{mix_q3[pt]*100:.0f}%",
                 ha="center", fontsize=8, color="#7d2519")
    axL.set_xticks(x)
    axL.set_xticklabels(PUBTYPE_BUCKETS_5, fontsize=9)
    axL.set_ylabel("% of corpus", fontsize=10)
    axL.set_title("Publication-type mix: Q3 vs Q1/Q2", fontsize=11, fontweight="bold")
    axL.legend(fontsize=9, framealpha=0.9)
    axL.set_ylim(0, max(mix_q12.max(), mix_q3.max()) * 100 + 8)

    # right: raw vs mix-adjusted gap waterfall-ish
    labels = ["raw\nQ3", "mix-adj\nQ3", "raw\nQ1/Q2"]
    vals = [raw_q3, adjusted_q3, raw_q12]
    colors = ["#C0392B", "#E67E22", "#2980B9"]
    bars = axR.bar(labels, vals, color=colors, alpha=0.9,
                   yerr=[[raw_q3 - ci_raw_q3["lower"], adjusted_q3 - ci_adj["lower"],
                          raw_q12 - ci_raw_q12["lower"]],
                         [ci_raw_q3["upper"] - raw_q3, ci_adj["upper"] - adjusted_q3,
                          ci_raw_q12["upper"] - raw_q12]],
                   error_kw={"lw": 1, "capsize": 4, "ecolor": "#333"})
    for b, v in zip(bars, vals):
        axR.text(b.get_x() + b.get_width() / 2, v + 0.5, f"{v:.1f}%",
                 ha="center", fontsize=9, fontweight="bold")
    axR.set_ylabel("% critical (Alarm+Caution)", fontsize=10)
    axR.set_title(f"Composition explains {composition_pct:.0f}% of gap",
                  fontsize=11, fontweight="bold")
    axR.set_ylim(0, raw_q12 + 8)
    # annotate the composition vs within split
    axR.annotate("", xy=(1, adjusted_q3), xytext=(0, raw_q3),
                 arrowprops=dict(arrowstyle="->", color="#555", lw=1.2))
    axR.text(0.5, max(raw_q3, adjusted_q3) + 2.2,
             f"composition\n+{explained_pp:.1f}pp", ha="center", fontsize=8, color="#555")

    fig.suptitle(
        "Q3's lower critical stance — composition (more reviews) vs within-type effect\n"
        f"Q1/Q2 medical (n={len(q12):,}) vs Q3 (n={len(q3):,}), 2021–2026; "
        f"gap {gap:.1f}pp = {composition_pct:.0f}% composition / {within_pct:.0f}% within-type.",
        fontsize=11, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    out_fig = FIGURES_DIR / "q3_pubtype_mix.png"
    fig.savefig(out_fig, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"\nFiles:")
    print(f"  {out_csv.relative_to(WORKTREE)}")
    print(f"  {out_fig.relative_to(WORKTREE)}")


if __name__ == "__main__":
    main()
