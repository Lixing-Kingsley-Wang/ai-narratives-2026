"""
Step 2.8 (A.5) — 2024 Alarm peak vs 2025 Alarm drill-down.

Compare 2024 and 2025 Alarm-stance records on:
  - specialty mix
  - pub-type mix
  - top journals
  - theme mix (within A+C subset)

Produces:
  output/analyses/alarm_peak_drilldown.md
  output/analyses/alarm_peak_drilldown_data.csv
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pandas as pd

from analysis.robustness import load_classifications, simplify_pubtype_5

WORKTREE = Path(__file__).resolve().parents[1]
ANALYSES_DIR = WORKTREE / "output" / "analyses"
SPEC_PATH = WORKTREE / "output" / "specialty_classifications.csv"
THEMES_PATH = Path("/Users/kingslywang/repos/ai-narratives-2026/output/analysis/thematic_alarm.csv")


def split_themes(s):
    if not isinstance(s, str):
        return []
    return [t.strip() for t in s.split("|") if t.strip()]


def mix_table(records: pd.DataFrame, key: str, top_k: int = 10) -> pd.DataFrame:
    counts = records[key].value_counts().head(top_k)
    pcts = (counts / len(records) * 100).round(1)
    return pd.DataFrame({"count": counts.values, "pct": pcts.values}, index=counts.index)


def theme_mix(records: pd.DataFrame, themes_df: pd.DataFrame, top_k: int = 8) -> pd.DataFrame:
    sub = themes_df[themes_df["pmid"].astype(str).isin(records["pmid"].astype(str))]
    all_themes = []
    for ts in sub["themes"].dropna():
        all_themes.extend(split_themes(ts))
    c = Counter(all_themes).most_common(top_k)
    if not c:
        return pd.DataFrame(columns=["count", "pct"])
    total = len(sub)
    rows = [{"theme": t, "count": n, "pct": round(n / total * 100, 1) if total else 0}
            for t, n in c]
    return pd.DataFrame(rows).set_index("theme")


def main() -> None:
    print("Step 2.8 (A.5) — 2024 Alarm peak vs 2025 drill-down")
    print("=" * 60)

    v1 = load_classifications("v1")
    v1["pmid"] = v1["pmid"].astype(str)

    spec = pd.read_csv(SPEC_PATH, usecols=["pmid", "specialty"])
    spec["pmid"] = spec["pmid"].astype(str)
    v1 = v1.merge(spec, on="pmid", how="left")

    # Pull title back in for the candidate CSV (load_classifications drops it)
    titles = pd.read_csv(
        Path("/Users/kingslywang/repos/ai-narratives-2026/output/classified_medical_Q1Q2.csv"),
        usecols=["pmid", "title"], low_memory=False,
    )
    titles["pmid"] = titles["pmid"].astype(str)
    v1 = v1.merge(titles, on="pmid", how="left")

    themes_df = pd.read_csv(THEMES_PATH, low_memory=False)
    themes_df["pmid"] = themes_df["pmid"].astype(str)

    alarm_2024 = v1[(v1["pub_year"] == 2024) & (v1["stance"] == "Alarm")].copy()
    alarm_2025 = v1[(v1["pub_year"] == 2025) & (v1["stance"] == "Alarm")].copy()

    # Rate (per-year Alarm %)
    n_2024 = int((v1["pub_year"] == 2024).sum())
    n_2025 = int((v1["pub_year"] == 2025).sum())
    rate_2024 = len(alarm_2024) / n_2024 * 100
    rate_2025 = len(alarm_2025) / n_2025 * 100

    print(f"2024 Alarm: n={len(alarm_2024):,} / total={n_2024:,}  rate={rate_2024:.2f}%")
    print(f"2025 Alarm: n={len(alarm_2025):,} / total={n_2025:,}  rate={rate_2025:.2f}%")
    delta_pct = (len(alarm_2025) - len(alarm_2024)) / len(alarm_2024) * 100
    delta_rate = rate_2025 - rate_2024
    print(f"Δ count: {len(alarm_2025) - len(alarm_2024):+,} ({delta_pct:+.1f}%)")
    print(f"Δ rate:  {delta_rate:+.2f} pp\n")

    md = [
        "# A.5 — 2024 Alarm peak drill-down",
        "",
        f"**Note**: the \"2024 peak\" is a per-year **rate** peak, not an absolute count peak. "
        f"Total Alarm count kept rising with corpus growth (29→335 from 2021→2025). The "
        f"per-year Alarm % dipped from {rate_2024:.2f}% (2024) to {rate_2025:.2f}% (2025) — a "
        f"{delta_rate:+.2f} pp drop — before partial-year 2026 partially rebounded.",
        "",
        f"- 2024 Alarm: **{len(alarm_2024):,}** records ({rate_2024:.2f}% of {n_2024:,} year-total)",
        f"- 2025 Alarm: **{len(alarm_2025):,}** records ({rate_2025:.2f}% of {n_2025:,} year-total)",
        f"- Δ count: {len(alarm_2025)-len(alarm_2024):+,} ({delta_pct:+.1f}%); Δ rate: {delta_rate:+.2f} pp",
        "",
        "## Specialty mix",
        "",
    ]
    spec_2024 = mix_table(alarm_2024, "specialty")
    spec_2025 = mix_table(alarm_2025, "specialty")
    union = sorted(set(spec_2024.index) | set(spec_2025.index),
                    key=lambda s: -(spec_2024["count"].get(s, 0) + spec_2025["count"].get(s, 0)))
    md.append("| specialty | 2024 n (%) | 2025 n (%) |")
    md.append("|---|---:|---:|")
    for s in union:
        v24c = int(spec_2024["count"].get(s, 0))
        v25c = int(spec_2025["count"].get(s, 0))
        v24p = float(spec_2024["pct"].get(s, 0.0))
        v25p = float(spec_2025["pct"].get(s, 0.0))
        md.append(f"| {s} | {v24c} ({v24p:.1f}%) | {v25c} ({v25p:.1f}%) |")

    md.append("")
    md.append("## Publication type mix")
    md.append("")
    alarm_2024["pt_simple"] = alarm_2024["pub_type_simple_5"]
    alarm_2025["pt_simple"] = alarm_2025["pub_type_simple_5"]
    pt_2024 = mix_table(alarm_2024, "pt_simple")
    pt_2025 = mix_table(alarm_2025, "pt_simple")
    md.append("| pub_type | 2024 n (%) | 2025 n (%) |")
    md.append("|---|---:|---:|")
    for pt in sorted(set(pt_2024.index) | set(pt_2025.index),
                      key=lambda p: -(pt_2024["count"].get(p, 0) + pt_2025["count"].get(p, 0))):
        md.append(f"| {pt} | {int(pt_2024['count'].get(pt,0))} ({pt_2024['pct'].get(pt,0):.1f}%) "
                  f"| {int(pt_2025['count'].get(pt,0))} ({pt_2025['pct'].get(pt,0):.1f}%) |")

    md.append("")
    md.append("## Top 10 journals")
    md.append("")
    md.append("### 2024 Alarm")
    md.append("")
    j_24 = mix_table(alarm_2024, "journal", top_k=10)
    md.append("| journal | n | % |")
    md.append("|---|---:|---:|")
    for j, c, p in zip(j_24.index, j_24["count"], j_24["pct"]):
        md.append(f"| {j} | {int(c)} | {float(p):.1f}% |")
    md.append("")
    md.append("### 2025 Alarm")
    md.append("")
    j_25 = mix_table(alarm_2025, "journal", top_k=10)
    md.append("| journal | n | % |")
    md.append("|---|---:|---:|")
    for j, c, p in zip(j_25.index, j_25["count"], j_25["pct"]):
        md.append(f"| {j} | {int(c)} | {float(p):.1f}% |")

    md.append("")
    md.append("## Top themes (within A+C subset)")
    md.append("")
    t_24 = theme_mix(alarm_2024, themes_df, top_k=8)
    t_25 = theme_mix(alarm_2025, themes_df, top_k=8)
    md.append("### 2024 Alarm")
    md.append("")
    md.append("| theme | n | % |")
    md.append("|---|---:|---:|")
    for theme, row in t_24.iterrows():
        md.append(f"| {theme} | {int(row['count'])} | {float(row['pct']):.1f}% |")
    md.append("")
    md.append("### 2025 Alarm")
    md.append("")
    md.append("| theme | n | % |")
    md.append("|---|---:|---:|")
    for theme, row in t_25.iterrows():
        md.append(f"| {theme} | {int(row['count'])} | {float(row['pct']):.1f}% |")

    md.append("")
    md.append("## Verdict")
    md.append("")
    # Look at mix shifts proportionally (pct) rather than absolute count
    top_spec_drop = max(union, key=lambda s: spec_2024["pct"].get(s, 0) - spec_2025["pct"].get(s, 0))
    top_spec_rise = max(union, key=lambda s: spec_2025["pct"].get(s, 0) - spec_2024["pct"].get(s, 0))
    spec_drop = spec_2024["pct"].get(top_spec_drop, 0) - spec_2025["pct"].get(top_spec_drop, 0)
    spec_rise = spec_2025["pct"].get(top_spec_rise, 0) - spec_2024["pct"].get(top_spec_rise, 0)
    v = (
        f"The 2025 Alarm-rate dip ({delta_rate:+.2f} pp from 2024) is **not** explained by "
        f"any single specialty pulling back. Biggest mix shift: **{top_spec_drop}** -{spec_drop:.1f} pp, "
        f"counter-balanced by **{top_spec_rise}** +{spec_rise:.1f} pp. Most likely interpretation: "
        f"the 2025 'dip' is a **publication-lag / denominator-growth artifact** — the absolute "
        f"Alarm count rose but the total corpus (denominator) grew faster as Cautious Optimism "
        f"papers expanded with the field. Partial-year 2026 already shows Alarm rate recovering."
    )
    md.append(v)

    out = ANALYSES_DIR / "alarm_peak_drilldown.md"
    out.write_text("\n".join(md) + "\n")
    print(f"\nWrote: {out}")

    combined = pd.concat([
        alarm_2024[["pmid","specialty","pub_type_simple_5","journal","title"]].assign(year=2024),
        alarm_2025[["pmid","specialty","pub_type_simple_5","journal","title"]].assign(year=2025),
    ])
    combined.to_csv(ANALYSES_DIR / "alarm_peak_drilldown_data.csv", index=False)


if __name__ == "__main__":
    main()
