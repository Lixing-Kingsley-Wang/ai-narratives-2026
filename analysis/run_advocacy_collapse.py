"""
Step 2.9 (A.6) — Advocacy collapse anatomy.

Compare 2021 Advocacy vs 2026 Advocacy on specialty, journal, pub-type,
predictive_claim distribution. Plus emit a prophecy-panel candidates CSV
listing ALL 2021–2023 Advocacy records with predictive_claim=yes — these
become Session 3 candidates for Kingsley to triage.

Produces:
  output/analyses/advocacy_collapse_anatomy.md
  output/analyses/prophecy_panel_candidates_2021_2023.csv
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from analysis.robustness import load_classifications

WORKTREE = Path(__file__).resolve().parents[1]
ANALYSES_DIR = WORKTREE / "output" / "analyses"
SPEC_PATH = WORKTREE / "output" / "specialty_classifications.csv"
V1_FULL_PATH = Path("/Users/kingslywang/repos/ai-narratives-2026/output/classified_medical_Q1Q2.csv")


def mix_pct(records: pd.DataFrame, key: str, top_k: int = 10) -> pd.DataFrame:
    counts = records[key].value_counts().head(top_k)
    pcts = (counts / len(records) * 100).round(1)
    return pd.DataFrame({"count": counts.values, "pct": pcts.values}, index=counts.index)


def main() -> None:
    print("Step 2.9 (A.6) — Advocacy collapse anatomy")
    print("=" * 60)

    v1 = load_classifications("v1")
    v1["pmid"] = v1["pmid"].astype(str)

    spec = pd.read_csv(SPEC_PATH, usecols=["pmid", "specialty"])
    spec["pmid"] = spec["pmid"].astype(str)
    v1 = v1.merge(spec, on="pmid", how="left")

    # Pull title from the full v1 CSV (load_classifications doesn't keep it)
    full = pd.read_csv(V1_FULL_PATH, usecols=["pmid", "title", "abstract"], low_memory=False)
    full["pmid"] = full["pmid"].astype(str)
    v1 = v1.merge(full, on="pmid", how="left")

    adv_2021 = v1[(v1["pub_year"] == 2021) & (v1["stance"] == "Advocacy")].copy()
    adv_2026 = v1[(v1["pub_year"] == 2026) & (v1["stance"] == "Advocacy")].copy()
    print(f"2021 Advocacy: n={len(adv_2021):,}")
    print(f"2026 Advocacy: n={len(adv_2026):,}")

    def section(records: pd.DataFrame, label: str, target_md: list[str]) -> None:
        target_md.append(f"### {label} (n={len(records)})")
        target_md.append("")
        # Specialty
        target_md.append("**Specialty:**")
        for s, row in mix_pct(records, "specialty").iterrows():
            target_md.append(f"- {s}: {int(row['count'])} ({float(row['pct']):.1f}%)")
        target_md.append("")
        # Pub-type
        target_md.append("**Pub type:**")
        for pt, row in mix_pct(records, "pub_type_simple_5").iterrows():
            target_md.append(f"- {pt}: {int(row['count'])} ({float(row['pct']):.1f}%)")
        target_md.append("")
        # Top journals
        target_md.append("**Top journals:**")
        for j, row in mix_pct(records, "journal").iterrows():
            target_md.append(f"- {j}: {int(row['count'])} ({float(row['pct']):.1f}%)")
        target_md.append("")
        # Predictive claim
        pred_yes = (records["predictive_claim"] == "yes").sum()
        target_md.append(f"**predictive_claim=yes:** {pred_yes}/{len(records)} "
                         f"({pred_yes/len(records)*100:.1f}%)" if len(records) else "**predictive_claim=yes:** n/a")
        target_md.append("")

    md = [
        "# A.6 — Advocacy collapse anatomy",
        "",
        f"Advocacy stance collapsed monotonically from {len(adv_2021)} records in 2021 "
        f"to {len(adv_2026)} in 2026 (partial year). This drill-down compares the "
        "composition of Advocacy papers at the two endpoints.",
        "",
        "## Composition by year",
        "",
    ]
    section(adv_2021, "2021 Advocacy", md)
    section(adv_2026, "2026 Advocacy (Jan–Apr partial year)", md)

    # ── Prophecy panel candidates (2021–2023 Advocacy + predictive_claim) ─────
    cand = v1[
        (v1["pub_year"].isin([2021, 2022, 2023]))
        & (v1["stance"] == "Advocacy")
        & (v1["predictive_claim"] == "yes")
    ][["pmid", "pub_year", "journal", "pub_type_simple_5", "specialty",
        "title", "abstract"]].copy()
    cand = cand.sort_values(["pub_year", "journal"])
    out_csv = ANALYSES_DIR / "prophecy_panel_candidates_2021_2023.csv"
    cand.to_csv(out_csv, index=False)

    md.append("")
    md.append("## Prophecy panel candidates")
    md.append("")
    md.append(f"Wrote `{out_csv.name}` listing all **{len(cand)}** records that are: "
              "Advocacy stance + 2021–2023 + predictive_claim=yes. These are candidates "
              "for the Session 3 prophecy panel — quotable forward-looking claims to "
              "now-check against 2024–2026 reality.")
    md.append("")
    md.append("Breakdown by year:")
    for yr in [2021, 2022, 2023]:
        n = (cand["pub_year"] == yr).sum()
        md.append(f"- {yr}: {n} candidates")
    md.append("")
    md.append("Top journals among candidates:")
    for j, row in mix_pct(cand, "journal", top_k=10).iterrows():
        md.append(f"- {j}: {int(row['count'])}")

    out_md = ANALYSES_DIR / "advocacy_collapse_anatomy.md"
    out_md.write_text("\n".join(md) + "\n")
    print(f"\nWrote: {out_md}")
    print(f"Wrote: {out_csv} ({len(cand)} candidates)")


if __name__ == "__main__":
    main()
