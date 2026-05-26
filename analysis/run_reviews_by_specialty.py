"""
Step 4.3 (C.3) — Reviews-positive depth check by specialty.

Session 1 found that Editorial+Commentary+Letter (opinion pieces) skew more
critical than Research Articles. Reviews fall in between. Question: within
review papers specifically, does the critical rate by specialty match
research-article patterns, or do reviews show specialty-specific positivity?

Produces:
  output/analyses/reviews_by_specialty.md
  output/figures/reviews_vs_research_by_specialty.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analysis.robustness import load_classifications

WORKTREE = Path(__file__).resolve().parents[1]
ANALYSES_DIR = WORKTREE / "output" / "analyses"
FIGURES_DIR = WORKTREE / "output" / "figures"
SPEC_PATH = WORKTREE / "output" / "specialty_classifications.csv"


def main() -> None:
    print("Step 4.3 (C.3) — Reviews critical rate by specialty")
    print("=" * 60)

    v1 = load_classifications("v1")
    v1["pmid"] = v1["pmid"].astype(str)
    spec = pd.read_csv(SPEC_PATH, usecols=["pmid", "specialty"])
    spec["pmid"] = spec["pmid"].astype(str)
    v1 = v1.merge(spec, on="pmid", how="left")
    v1 = v1[v1["specialty"].notna() & (v1["specialty"] != "FAILED")].copy()

    # Reviews bucket = "Review" in simplified pub_type_simple_5
    v1["is_review"] = v1["pub_type_simple_5"] == "Review"
    v1["is_research"] = v1["pub_type_simple_5"] == "Research Article"
    v1["is_critical"] = v1["stance"].isin(["Alarm", "Caution"])

    # Per-specialty critical rate for reviews vs research articles
    spec_counts = v1["specialty"].value_counts()
    top_specs = spec_counts.head(10).index.tolist()

    rows = []
    for s in top_specs:
        rev = v1[(v1["specialty"] == s) & v1["is_review"]]
        res = v1[(v1["specialty"] == s) & v1["is_research"]]
        if len(rev) < 20 or len(res) < 20:
            continue
        rows.append({
            "specialty": s,
            "n_review": len(rev),
            "n_research": len(res),
            "review_critical_pct": round(rev["is_critical"].mean() * 100, 2),
            "research_critical_pct": round(res["is_critical"].mean() * 100, 2),
            "delta_review_minus_research": round(
                (rev["is_critical"].mean() - res["is_critical"].mean()) * 100, 2),
        })
    df = pd.DataFrame(rows).sort_values("delta_review_minus_research")
    df.to_csv(ANALYSES_DIR / "reviews_by_specialty.csv", index=False)

    print("\nReview critical rate vs Research-Article critical rate, per specialty:")
    print(f"  {'specialty':<40} {'n_rev':>6} {'n_res':>6} {'rev%':>7} {'res%':>7} {'Δ':>7}")
    for _, r in df.iterrows():
        print(f"  {r['specialty']:<40} {int(r['n_review']):>6,} {int(r['n_research']):>6,} "
              f"{r['review_critical_pct']:>6.1f}% {r['research_critical_pct']:>6.1f}% "
              f"{r['delta_review_minus_research']:>+6.1f}")

    # Overall control
    rev_all = v1[v1["is_review"]]
    res_all = v1[v1["is_research"]]
    print(f"\nOverall (all specialties pooled):")
    print(f"  Reviews:  n={len(rev_all):,} critical={rev_all['is_critical'].mean()*100:.1f}%")
    print(f"  Research: n={len(res_all):,} critical={res_all['is_critical'].mean()*100:.1f}%")

    n_review_more_critical = (df["delta_review_minus_research"] > 0).sum()
    n_review_less_critical = (df["delta_review_minus_research"] < 0).sum()
    print(f"\nReviews MORE critical than research in: {n_review_more_critical}/{len(df)} specialties")
    print(f"Reviews LESS critical than research in: {n_review_less_critical}/{len(df)} specialties")

    # ── Figure: paired horizontal bars (review vs research per specialty) ─────
    fig, ax = plt.subplots(figsize=(10, 6))
    y = np.arange(len(df))
    bar_h = 0.4
    ax.barh(y - bar_h/2, df["research_critical_pct"], bar_h,
            label="Research articles", color="#3498DB", alpha=0.85)
    ax.barh(y + bar_h/2, df["review_critical_pct"], bar_h,
            label="Reviews",            color="#C0392B", alpha=0.85)
    ax.set_yticks(y)
    ax.set_yticklabels(df["specialty"], fontsize=9)
    ax.set_xlabel("% Critical (Alarm + Caution)", fontsize=10)
    ax.legend(loc="lower right", fontsize=9, framealpha=0.9)
    ax.set_title(
        "Reviews vs Research Articles — % Critical by specialty\n"
        f"v1 stance, Q1/Q2 medical, 2021–2026; specialties shown have n≥20 in each bucket.",
        fontsize=10, fontweight="bold",
    )
    for i, row in enumerate(df.itertuples()):
        ax.text(row.research_critical_pct + 0.5, i - bar_h/2,
                f"{row.research_critical_pct:.1f}% (n={int(row.n_research):,})",
                va="center", fontsize=7.5, color="#1F618D")
        ax.text(row.review_critical_pct + 0.5, i + bar_h/2,
                f"{row.review_critical_pct:.1f}% (n={int(row.n_review):,})",
                va="center", fontsize=7.5, color="#922B21")
    fig.tight_layout()
    out_fig = FIGURES_DIR / "reviews_vs_research_by_specialty.png"
    fig.savefig(out_fig, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    # Markdown
    md = [
        "# C.3 — Reviews critical rate vs Research Articles, by specialty",
        "",
        f"Overall reviews: n={len(rev_all):,}, critical={rev_all['is_critical'].mean()*100:.1f}%.",
        f"Overall research: n={len(res_all):,}, critical={res_all['is_critical'].mean()*100:.1f}%.",
        "",
        f"Per-specialty breakdown (specialties with n≥20 in each bucket):",
        "",
        "| specialty | n_review | n_research | review % crit | research % crit | Δ (rev−res) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for _, r in df.iterrows():
        md.append(f"| {r['specialty']} | {int(r['n_review']):,} | {int(r['n_research']):,} | "
                  f"{r['review_critical_pct']:.1f}% | {r['research_critical_pct']:.1f}% | "
                  f"{r['delta_review_minus_research']:+.1f} pp |")

    md.extend(["", "## Verdict", ""])
    if n_review_more_critical > n_review_less_critical:
        verdict = ("Reviews are MORE critical than research articles in most specialties — "
                   "the Session 1 reviews-positivity finding does NOT replicate within specialties. "
                   "The earlier pooled result may reflect a specialty mix effect.")
    elif n_review_less_critical > n_review_more_critical:
        verdict = ("Reviews are consistently LESS critical than research articles across "
                   "most specialties — the Session 1 reviews-positivity finding holds within-specialty. "
                   "Reviews systematically dampen criticism, regardless of clinical field.")
    else:
        verdict = "Mixed pattern — no consistent direction across specialties."
    md.append(verdict)
    md.append("")
    md.append(f"![figure](../figures/reviews_vs_research_by_specialty.png)")

    (ANALYSES_DIR / "reviews_by_specialty.md").write_text("\n".join(md) + "\n")
    print(f"\nFigure: {out_fig}")
    print(f"MD: {ANALYSES_DIR / 'reviews_by_specialty.md'}")


if __name__ == "__main__":
    main()
