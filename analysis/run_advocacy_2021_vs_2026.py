"""
Session 3 — Advocacy 2026 vs 2021: list both years and characterize the
collapse anatomy at observation level (general, no detailed prophecy).

Produces:
  output/analyses/advocacy_2021_vs_2026.md
  output/analyses/advocacy_2021_records.csv
  output/analyses/advocacy_2026_records.csv
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from analysis.robustness import load_classifications

WORKTREE = Path(__file__).resolve().parents[1]
ANALYSES_DIR = WORKTREE / "output" / "analyses"
SPEC_PATH = WORKTREE / "output" / "specialty_classifications.csv"
GEO_PATH = WORKTREE / "output" / "geography_classifications.csv"
V1_FULL = Path("/Users/kingslywang/repos/ai-narratives-2026/output/classified_medical_Q1Q2.csv")


def main() -> None:
    v1 = load_classifications("v1")
    v1["pmid"] = v1["pmid"].astype(str)

    spec = pd.read_csv(SPEC_PATH, usecols=["pmid", "specialty"])
    geo = pd.read_csv(GEO_PATH, usecols=["pmid", "country", "region"])
    full = pd.read_csv(V1_FULL, usecols=["pmid", "title", "abstract"], low_memory=False)
    for f in [spec, geo, full]:
        f["pmid"] = f["pmid"].astype(str)

    v1 = v1.merge(spec, on="pmid", how="left").merge(geo, on="pmid", how="left").merge(full, on="pmid", how="left")

    adv_2021 = v1[(v1["pub_year"] == 2021) & (v1["stance"] == "Advocacy")].copy()
    adv_2026 = v1[(v1["pub_year"] == 2026) & (v1["stance"] == "Advocacy")].copy()

    cols = ["pmid", "journal", "pub_type_simple_5", "specialty", "country", "region",
            "predictive_claim", "title"]
    adv_2021[cols].to_csv(ANALYSES_DIR / "advocacy_2021_records.csv", index=False)
    adv_2026[cols].to_csv(ANALYSES_DIR / "advocacy_2026_records.csv", index=False)

    md = [
        "# Advocacy 2021 vs 2026 — collapse anatomy at observation level",
        "",
        f"**2021 Advocacy: n={len(adv_2021)}.** **2026 Advocacy: n={len(adv_2026)}** "
        f"(partial year, Jan–Apr 2026).",
        "",
        f"As Advocacy rate fell 2.91% → 0.63% (ρ=-1.0 monotonic), what survived in 2026? "
        f"This brief lists every 2026 Advocacy record and a comparable cut of 2021 "
        f"Advocacy, with structural columns. Detailed prophecy-panel triage is a "
        f"separate manual task (see `prophecy_panel_candidates_2021_2023.csv` for 2021–2023).",
        "",
        "## 2026 Advocacy — all 17 records",
        "",
    ]
    for _, r in adv_2026.iterrows():
        line = (f"- **{r['journal']}** | {r['pub_type_simple_5']} | "
                f"{r['specialty']} | {r['country']} ({r['region']}) | "
                f"pred_claim={r['predictive_claim']}")
        md.append(line)
        md.append(f"  > _{r['title']}_")
    md.append("")
    md.append("## 2021 Advocacy — all 31 records")
    md.append("")
    for _, r in adv_2021.iterrows():
        line = (f"- **{r['journal']}** | {r['pub_type_simple_5']} | "
                f"{r['specialty']} | {r['country']} ({r['region']}) | "
                f"pred_claim={r['predictive_claim']}")
        md.append(line)
        md.append(f"  > _{r['title']}_")

    md.append("")
    md.append("## Comparison tables")
    md.append("")
    for col, label in [("specialty", "Specialty"), ("pub_type_simple_5", "Pub type"),
                        ("region", "Region"), ("predictive_claim", "Predictive claim"),
                        ("journal", "Journal (top 10)")]:
        md.append(f"### {label}")
        md.append("")
        c21 = adv_2021[col].value_counts().head(10) if col == "journal" else adv_2021[col].value_counts()
        c26 = adv_2026[col].value_counts().head(10) if col == "journal" else adv_2026[col].value_counts()
        all_keys = sorted(set(c21.index) | set(c26.index),
                           key=lambda k: -(int(c21.get(k, 0)) + int(c26.get(k, 0))))
        md.append(f"| {label} | 2021 (n={len(adv_2021)}) | 2026 (n={len(adv_2026)}) |")
        md.append("|---|---:|---:|")
        for k in all_keys:
            v21 = int(c21.get(k, 0))
            v26 = int(c26.get(k, 0))
            p21 = v21 / len(adv_2021) * 100 if len(adv_2021) else 0
            p26 = v26 / len(adv_2026) * 100 if len(adv_2026) else 0
            md.append(f"| {k} | {v21} ({p21:.1f}%) | {v26} ({p26:.1f}%) |")
        md.append("")

    md.append("## General observations (Claude's read; Kingsley to refine)")
    md.append("")

    # Auto-generate some sketchy observations from the data
    spec_2021_top = adv_2021["specialty"].value_counts().head(3).index.tolist()
    spec_2026_top = adv_2026["specialty"].value_counts().head(3).index.tolist()
    region_2021 = adv_2021["region"].value_counts().to_dict()
    region_2026 = adv_2026["region"].value_counts().to_dict()
    pred_2021 = (adv_2021["predictive_claim"] == "yes").sum()
    pred_2026 = (adv_2026["predictive_claim"] == "yes").sum()

    md.append(f"- **Specialty shift:** 2021 Advocacy concentrated in "
              f"{', '.join(spec_2021_top)}; 2026 survivors concentrated in "
              f"{', '.join(spec_2026_top)}.")
    md.append(f"- **Geographic shift:** 2021 spread across "
              f"{len(region_2021)} regions; 2026 across {len(region_2026)} regions.")
    md.append(f"- **Predictive-claim fraction:** "
              f"2021 {pred_2021}/{len(adv_2021)} = {pred_2021/len(adv_2021)*100:.0f}% "
              f"forward-looking predictions; "
              f"2026 {pred_2026}/{len(adv_2026)} = {pred_2026/len(adv_2026)*100:.0f}%.")
    md.append("")
    md.append("**Interpretation seed for the Commentary** (Kingsley to refine):")
    md.append("")
    md.append(
        "The Advocacy stance has not disappeared but has narrowed substantially. "
        "Where 2021 saw broad-strokes forward-looking claims (\"AI will revolutionize X\") "
        "across multiple specialties, 2026 Advocacy survives mainly as field-specific "
        "endorsements with concrete clinical anchors. This convergence with Cautious "
        "Optimism — rather than disappearance — is consistent with the broader narrative "
        "of medicine absorbing AI into its existing measured-language conventions, rather "
        "than rejecting AI outright."
    )

    out = ANALYSES_DIR / "advocacy_2021_vs_2026.md"
    out.write_text("\n".join(md) + "\n")
    print(f"2021 Advocacy: n={len(adv_2021)}")
    print(f"2026 Advocacy: n={len(adv_2026)}")
    print(f"Wrote: {out}")
    print(f"Wrote: {ANALYSES_DIR / 'advocacy_2021_records.csv'}")
    print(f"Wrote: {ANALYSES_DIR / 'advocacy_2026_records.csv'}")


if __name__ == "__main__":
    main()
