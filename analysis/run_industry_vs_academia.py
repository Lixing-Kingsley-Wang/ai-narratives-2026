"""
S4-6 — First-author industry vs academic/clinical critical stance.

Only first-author affiliation exists in the corpus, so this is a
FIRST-AUTHOR-based split, not any-author. Classify first_affiliation into
{industry, academic_clinical, mixed, other/unclear} by keyword/regex heuristic,
then compare critical (Alarm+Caution) rate industry vs academic_clinical with
bootstrap 95% CIs — overall, by pub_year, and pub-type-controlled (industry
skews toward certain pub-types).

Conventions: v1 canonical (classified_medical_Q1Q2.csv), drop FAILED,
pub_year 2021-2026, bootstrap n=1000 seed=42 percentile 95% CI.

Produces:
  output/analyses/industry_vs_academia.csv
  output/figures/industry_vs_academia.png  (300 dpi)
"""

from __future__ import annotations

import re
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
V1_PATH = DATA_DIR / "classified_medical_Q1Q2.csv"
RAW_PATH = DATA_DIR / "raw_medical_all.csv"

CRITICAL = ["Alarm", "Caution"]
YEARS = list(range(2021, 2027))

# ── industry heuristic ─────────────────────────────────────────────────────────
# Legal-form / corporate suffixes (word-boundary regex per brief).
INDUSTRY_SUFFIX_RE = re.compile(
    r"\b(Inc|Ltd|LLC|GmbH|Corp|Corporation|Co\.|Company|Pharmaceuticals?|"
    r"Biosciences?|Biotech\w*|Technologies|Therapeutics|Labs?)\b",
    re.IGNORECASE,
)
# Named big-tech / big-pharma / health-AI firms.
INDUSTRY_NAMES = [
    "google", "deepmind", "microsoft", "openai", "meta ", "facebook", "amazon",
    "apple ", "nvidia", "ibm", "intel ", "tencent", "alibaba", "baidu", "huawei",
    "samsung", "babylon health", "tempus", "flatiron", "nuance", "viz.ai", "aidoc",
    "philips", "siemens", "ge healthcare", "ge medical", "general electric",
    "medtronic", "stryker", "johnson & johnson", "abbott", "boston scientific",
    "roche", "genentech", "novartis", "pfizer", "astrazeneca", "merck", "bayer",
    "sanofi", "gsk", "glaxosmithkline", "bristol myers", "eli lilly", "amgen",
    "moderna", "biontech", "takeda", "novo nordisk", "boehringer",
    "mckinsey", "deloitte", "accenture", "iqvia", "covance",
]
INDUSTRY_NAME_RE = re.compile(
    "|".join(re.escape(n.strip()) for n in INDUSTRY_NAMES), re.IGNORECASE)

# ── academic / clinical heuristic ──────────────────────────────────────────────
ACADEMIC_RE = re.compile(
    r"\b(Universit\w+|College|Institut\w*|Hospital|School of Medicine|"
    r"Faculty|Clinic|Medical Cent(?:er|re)|Department of|"
    r"National Institutes|NIH|Polyclinic|Universidad|Universit[aä]t|Université)\b",
    re.IGNORECASE,
)


def classify_affiliation(aff: str) -> str:
    if not aff or not aff.strip():
        return "other/unclear"
    has_ind = bool(INDUSTRY_SUFFIX_RE.search(aff) or INDUSTRY_NAME_RE.search(aff))
    has_acad = bool(ACADEMIC_RE.search(aff))
    if has_ind and has_acad:
        return "mixed"
    if has_ind:
        return "industry"
    if has_acad:
        return "academic_clinical"
    return "other/unclear"


# ── load ────────────────────────────────────────────────────────────────────────
def load_frame() -> pd.DataFrame:
    df = pd.read_csv(V1_PATH, low_memory=False)
    df = df[df["stance"] != "FAILED"].copy()
    df["pub_year"] = pd.to_numeric(df["pub_year"], errors="coerce").astype("Int64")
    df = df[(df["pub_year"] >= 2021) & (df["pub_year"] <= 2026)].copy()

    # Recover first_affiliation from raw if it was dropped.
    if "first_affiliation" not in df.columns or df["first_affiliation"].notna().mean() < 0.5:
        raw = pd.read_csv(RAW_PATH, usecols=["pmid", "first_affiliation"], low_memory=False)
        df["pmid"] = df["pmid"].astype(str)
        raw["pmid"] = raw["pmid"].astype(str)
        df = df.drop(columns=[c for c in ["first_affiliation"] if c in df.columns])
        df = df.merge(raw, on="pmid", how="left")

    df["first_affiliation"] = df["first_affiliation"].fillna("")
    df["sector"] = df["first_affiliation"].map(classify_affiliation)
    df["pub_type_simple_5"] = df["pub_type"].fillna("").map(simplify_pubtype_5)
    return df


def critical_rate(df: pd.DataFrame) -> float:
    return df["stance"].isin(CRITICAL).mean() * 100


def main() -> None:
    ANALYSES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 72)
    print("S4-6 — First-author industry vs academic/clinical critical stance")
    print("=" * 72)

    df = load_frame()
    cov = (df["first_affiliation"].str.strip() != "").mean() * 100
    print(f"[1] Records (2021-2026, FAILED dropped): {len(df):,}")
    print(f"    first_affiliation coverage: {cov:.1f}%")

    # ── [2] distribution ──────────────────────────────────────────────────────
    dist = df["sector"].value_counts().reindex(
        ["academic_clinical", "industry", "mixed", "other/unclear"]).fillna(0).astype(int)
    print("\n[2] Sector distribution")
    for s, n in dist.items():
        print(f"    {s:<18} {n:>6,}  ({n/len(df)*100:4.1f}%)")

    # eyeball ~30 borderline cases: all 'mixed' + sample of 'industry'
    print("\n    Borderline inspection (mixed cases — both industry & academic tokens):")
    mixed = df[df["sector"] == "mixed"]
    for aff in mixed["first_affiliation"].head(18):
        print(f"      [mixed] {aff[:110]}")
    print("\n    Industry-classified sample (eyeball false positives):")
    for aff in df[df["sector"] == "industry"]["first_affiliation"].head(15):
        print(f"      [ind]   {aff[:110]}")

    # ── [3] critical rate industry vs academic, overall + bootstrap CI ─────────
    ind = df[df["sector"] == "industry"]
    acad = df[df["sector"] == "academic_clinical"]
    ci_ind = bootstrap_ci(ind, critical_rate)
    ci_acad = bootstrap_ci(acad, critical_rate)
    print("\n[3] Critical (Alarm+Caution) rate — overall")
    print(f"    industry          n={len(ind):>5,}  {ci_ind['point']:5.1f}%  "
          f"CI[{ci_ind['lower']:.1f}, {ci_ind['upper']:.1f}]  "
          f"(width {ci_ind['upper']-ci_ind['lower']:.1f}pp)")
    print(f"    academic_clinical n={len(acad):>5,}  {ci_acad['point']:5.1f}%  "
          f"CI[{ci_acad['lower']:.1f}, {ci_acad['upper']:.1f}]  "
          f"(width {ci_acad['upper']-ci_acad['lower']:.1f}pp)")
    print(f"    delta (industry - academic): {ci_ind['point']-ci_acad['point']:+.1f} pp")

    # by pub_year
    print("\n    By pub_year (industry n | crit% | academic crit%):")
    year_rows = []
    for y in YEARS:
        iy = ind[ind["pub_year"] == y]
        ay = acad[acad["pub_year"] == y]
        ir = critical_rate(iy) if len(iy) else np.nan
        ar = critical_rate(ay) if len(ay) else np.nan
        year_rows.append({"pub_year": y, "industry_n": len(iy),
                          "industry_crit": ir, "academic_n": len(ay), "academic_crit": ar})
        print(f"      {y}: ind n={len(iy):>3} crit={ir:5.1f}%  | "
              f"acad n={len(ay):>5,} crit={ar:5.1f}%"
              if len(iy) else
              f"      {y}: ind n={len(iy):>3} crit=  n/a  | "
              f"acad n={len(ay):>5,} crit={ar:5.1f}%")

    # ── pub-type-controlled (direct standardization of industry to academic mix)
    acad_mix = (acad["pub_type_simple_5"].value_counts(normalize=True)
                .reindex(PUBTYPE_BUCKETS_5).fillna(0.0))
    ind_mix = (ind["pub_type_simple_5"].value_counts(normalize=True)
               .reindex(PUBTYPE_BUCKETS_5).fillna(0.0))
    ind_crit_by_pt = (ind.groupby("pub_type_simple_5")["stance"]
                      .apply(lambda s: s.isin(CRITICAL).mean() * 100)
                      .reindex(PUBTYPE_BUCKETS_5))
    adj_ind = float((ind_crit_by_pt.fillna(ci_ind["point"]) / 100 * acad_mix).sum() * 100)
    print("\n    Pub-type-controlled (industry reweighted to academic pub-type mix):")
    print(f"      industry pub-type mix : "
          + ", ".join(f"{pt.split()[0]} {ind_mix[pt]*100:.0f}%" for pt in PUBTYPE_BUCKETS_5))
    print(f"      academic pub-type mix : "
          + ", ".join(f"{pt.split()[0]} {acad_mix[pt]*100:.0f}%" for pt in PUBTYPE_BUCKETS_5))
    print(f"      raw industry {ci_ind['point']:.1f}% -> mix-adjusted {adj_ind:.1f}% "
          f"(academic {ci_acad['point']:.1f}%)")

    # ── table out ──────────────────────────────────────────────────────────────
    rows = [
        {"group": "industry_overall", "n": len(ind), "critical_pct": round(ci_ind["point"], 2),
         "ci_lo": round(ci_ind["lower"], 2), "ci_hi": round(ci_ind["upper"], 2)},
        {"group": "academic_overall", "n": len(acad), "critical_pct": round(ci_acad["point"], 2),
         "ci_lo": round(ci_acad["lower"], 2), "ci_hi": round(ci_acad["upper"], 2)},
        {"group": "industry_pubtype_adjusted", "n": len(ind), "critical_pct": round(adj_ind, 2),
         "ci_lo": None, "ci_hi": None},
    ]
    for yr in year_rows:
        rows.append({"group": f"industry_{yr['pub_year']}", "n": yr["industry_n"],
                     "critical_pct": round(yr["industry_crit"], 2) if pd.notna(yr["industry_crit"]) else None,
                     "ci_lo": None, "ci_hi": None})
        rows.append({"group": f"academic_{yr['pub_year']}", "n": yr["academic_n"],
                     "critical_pct": round(yr["academic_crit"], 2) if pd.notna(yr["academic_crit"]) else None,
                     "ci_lo": None, "ci_hi": None})
    out_csv = ANALYSES_DIR / "industry_vs_academia.csv"
    pd.DataFrame(rows).to_csv(out_csv, index=False)

    # ── [4] figure ─────────────────────────────────────────────────────────────
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 5.5),
                                   gridspec_kw={"width_ratios": [1, 1.4]})

    # left: bar + CI overall
    groups = ["industry", "academic_clinical"]
    pts = [ci_ind["point"], ci_acad["point"]]
    los = [ci_ind["lower"], ci_acad["lower"]]
    his = [ci_ind["upper"], ci_acad["upper"]]
    ns = [len(ind), len(acad)]
    colors = ["#8E44AD", "#16A085"]
    yerr = np.array([[p - l for p, l in zip(pts, los)], [h - p for p, h in zip(pts, his)]])
    bars = axL.bar(groups, pts, yerr=yerr, color=colors, alpha=0.9,
                   error_kw={"lw": 1.2, "capsize": 5, "ecolor": "#333"})
    for b, p, n in zip(bars, pts, ns):
        axL.text(b.get_x() + b.get_width() / 2, p + 1.2, f"{p:.1f}%\n(n={n:,})",
                 ha="center", fontsize=9, fontweight="bold")
    axL.axhline(adj_ind, ls="--", color="#8E44AD", lw=1.2, alpha=0.7)
    axL.text(0, adj_ind + 0.4, f"industry pub-type-adj {adj_ind:.1f}%",
             fontsize=7.5, color="#8E44AD")
    axL.set_ylabel("% critical (Alarm+Caution)", fontsize=10)
    axL.set_title("Overall critical rate (bootstrap 95% CI)", fontsize=11, fontweight="bold")
    axL.set_ylim(0, max(his) + 8)

    # right: by-year line
    yr_df = pd.DataFrame(year_rows)
    axR.plot(yr_df["pub_year"], yr_df["academic_crit"], "-o", color="#16A085",
             label="academic_clinical", lw=2)
    axR.plot(yr_df["pub_year"], yr_df["industry_crit"], "-s", color="#8E44AD",
             label="industry", lw=2)
    for _, r in yr_df.iterrows():
        if pd.notna(r["industry_crit"]):
            axR.annotate(f"n={int(r['industry_n'])}", (r["pub_year"], r["industry_crit"]),
                         textcoords="offset points", xytext=(0, 7), ha="center",
                         fontsize=7, color="#8E44AD")
    axR.set_xlabel("Publication year", fontsize=10)
    axR.set_ylabel("% critical (Alarm+Caution)", fontsize=10)
    axR.set_title("Critical rate by year (industry n small → noisy)",
                  fontsize=11, fontweight="bold")
    axR.set_xticks(YEARS)
    axR.legend(fontsize=9, framealpha=0.9)
    axR.grid(True, alpha=0.25)

    fig.suptitle(
        "First-author industry vs academic/clinical critical stance — Q1/Q2 medical, 2021–2026\n"
        f"industry n={len(ind):,} ({len(ind)/len(df)*100:.1f}%) — first-author only, heuristic split; "
        f"2026 partial year.",
        fontsize=11, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    out_fig = FIGURES_DIR / "industry_vs_academia.png"
    fig.savefig(out_fig, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"\nFiles:")
    print(f"  {out_csv.relative_to(WORKTREE)}")
    print(f"  {out_fig.relative_to(WORKTREE)}")


if __name__ == "__main__":
    main()
