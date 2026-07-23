"""
Step 4.1 (C.1) — Hallucination x patient_safety co-occurrence.

Within the A+C subset (5,161 records in output/analysis/thematic_alarm.csv):
  - Pearson r between hallucination + safety_clinical binary flags
  - P(safety_clinical=1 | hallucination=1)
  - P(hallucination=1 | safety_clinical=1)
  - Year-by-year prevalence of records flagged BOTH

Produces:
  output/analyses/hallucination_patient_safety_cooccurrence.md
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import pearsonr

WORKTREE = Path(__file__).resolve().parents[1]
ANALYSES_DIR = WORKTREE / "output" / "analyses"
ANALYSES_DIR.mkdir(parents=True, exist_ok=True)

THEMES_PATH = Path("/Users/kingslywang/repos/ai-narratives-2026/output/analysis/thematic_alarm.csv")


def has_theme(themes_str: str, theme: str) -> int:
    if not isinstance(themes_str, str):
        return 0
    parts = {t.strip() for t in themes_str.split("|")}
    return int(theme in parts)


def main() -> None:
    df = pd.read_csv(THEMES_PATH, low_memory=False)
    df["pub_year"] = pd.to_numeric(df["pub_year"], errors="coerce").astype("Int64")
    df = df[(df["pub_year"] >= 2021) & (df["pub_year"] <= 2026)].copy()

    df["hallu"] = df["themes"].apply(lambda s: has_theme(s, "hallucination"))
    df["safety"] = df["themes"].apply(lambda s: has_theme(s, "safety_clinical"))
    df["both"] = ((df["hallu"] == 1) & (df["safety"] == 1)).astype(int)

    n = len(df)
    n_hallu = int(df["hallu"].sum())
    n_safety = int(df["safety"].sum())
    n_both = int(df["both"].sum())

    print(f"A+C subset (2021–2026): n={n:,}")
    print(f"  hallucination flagged: {n_hallu:,} ({n_hallu/n*100:.1f}%)")
    print(f"  safety_clinical flagged: {n_safety:,} ({n_safety/n*100:.1f}%)")
    print(f"  BOTH: {n_both:,} ({n_both/n*100:.1f}%)")

    r, p = pearsonr(df["hallu"], df["safety"])
    p_safety_given_hallu = n_both / n_hallu if n_hallu else float("nan")
    p_hallu_given_safety = n_both / n_safety if n_safety else float("nan")

    # Independence baseline: if independent, P(both) = P(hallu) * P(safety)
    expected_independent = (n_hallu / n) * (n_safety / n) * n
    lift = n_both / expected_independent if expected_independent else float("nan")

    print(f"\nPearson r(hallucination, safety_clinical) = {r:+.3f}  (p = {p:.2e})")
    print(f"P(safety_clinical=1 | hallucination=1) = {p_safety_given_hallu:.3f}")
    print(f"P(hallucination=1 | safety_clinical=1) = {p_hallu_given_safety:.3f}")
    print(f"Co-occurrence lift over independence: {lift:.2f}x  "
          f"(observed {n_both}, expected {expected_independent:.0f} under independence)")

    # Year-by-year
    yearly = df.groupby("pub_year").agg(
        n=("pmid", "count"),
        hallu_n=("hallu", "sum"),
        safety_n=("safety", "sum"),
        both_n=("both", "sum"),
    ).reset_index()
    yearly["hallu_pct"] = yearly["hallu_n"] / yearly["n"] * 100
    yearly["safety_pct"] = yearly["safety_n"] / yearly["n"] * 100
    yearly["both_pct"] = yearly["both_n"] / yearly["n"] * 100

    print(f"\nYear-by-year (within A+C):")
    print(f"  {'year':>6} {'n':>6} {'hallu%':>8} {'safety%':>9} {'both%':>8}")
    for _, row in yearly.iterrows():
        print(f"  {int(row['pub_year']):>6} {int(row['n']):>6,} "
              f"{row['hallu_pct']:>7.1f}% {row['safety_pct']:>8.1f}% {row['both_pct']:>7.1f}%")

    # Write report
    md = [
        "# C.1 — Hallucination × patient_safety co-occurrence",
        "",
        "Subset: A+C (Alarm + Caution) records from v1, 2021–2026, n=" + f"{n:,}.",
        "Themes from `output/analysis/thematic_alarm.csv` (v1-only theme classification).",
        "Mapping: plan's `patient_safety` = `safety_clinical` flag in the themes column.",
        "",
        "## Headline",
        "",
        f"- Records flagged **hallucination**: {n_hallu:,} ({n_hallu/n*100:.1f}%)",
        f"- Records flagged **safety_clinical**: {n_safety:,} ({n_safety/n*100:.1f}%)",
        f"- Records flagged **BOTH**: {n_both:,} ({n_both/n*100:.1f}%)",
        f"- **Pearson r = {r:+.3f}** (p = {p:.2e})",
        f"- P(safety_clinical | hallucination) = **{p_safety_given_hallu:.3f}**",
        f"- P(hallucination | safety_clinical) = **{p_hallu_given_safety:.3f}**",
        f"- Co-occurrence lift over independence: **{lift:.2f}×** (observed {n_both} vs expected {expected_independent:.0f})",
        "",
        "## Interpretation",
        "",
    ]
    if r > 0.15 and lift > 1.3:
        verdict = (
            f"Strong positive coupling. r={r:+.3f} with lift {lift:.2f}× over "
            f"independence indicates hallucination and patient-safety concerns "
            "are mentioned together more often than chance — they function as "
            "one tightly-linked discourse cluster rather than two parallel "
            "themes."
        )
    elif r > 0.05:
        verdict = (
            f"Moderate positive coupling. r={r:+.3f}, lift {lift:.2f}×. "
            "Some co-occurrence above independence baseline, but the asymmetric "
            f"conditional probabilities (P(safety|hallu)={p_safety_given_hallu:.2f} "
            f"vs P(hallu|safety)={p_hallu_given_safety:.2f}) suggest "
            "hallucination papers often raise safety concerns, but safety "
            "papers don't always invoke hallucination — two overlapping rather "
            "than identical clusters."
        )
    else:
        verdict = (
            f"Weak coupling. r={r:+.3f}, lift {lift:.2f}×. The two themes appear "
            "to operate as largely parallel discourses with limited overlap."
        )
    md.append(verdict)
    md.append("")
    md.append("## Year-by-year prevalence within A+C")
    md.append("")
    md.append("| year | n | hallucination % | safety_clinical % | both % |")
    md.append("|---:|---:|---:|---:|---:|")
    for _, row in yearly.iterrows():
        md.append(f"| {int(row['pub_year'])} | {int(row['n']):,} | "
                  f"{row['hallu_pct']:.1f}% | {row['safety_pct']:.1f}% | {row['both_pct']:.1f}% |")
    md.append("")
    md.append("Note: percentages are within the A+C subset, not the full corpus. "
              "Both themes rise sharply post-ChatGPT (2022→2023); the BOTH-flag "
              "rate is the most discriminating signal — its slope indicates whether "
              "the two themes are fusing into one cluster over time.")

    out = ANALYSES_DIR / "hallucination_patient_safety_cooccurrence.md"
    out.write_text("\n".join(md) + "\n")
    print(f"\nWrote: {out}")

    yearly.to_csv(ANALYSES_DIR / "hallucination_patient_safety_yearly.csv", index=False)


if __name__ == "__main__":
    main()
