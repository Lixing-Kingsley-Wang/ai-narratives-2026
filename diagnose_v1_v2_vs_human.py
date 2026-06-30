"""
Diagnose why v2 kappa is essentially identical to v1 kappa despite v2
relabelling 19.9% of the corpus.

Builds a record-level dataframe (n=300) of: human, v1, v2 stance, then
categorizes:
  - both_correct        : v1 == human AND v2 == human
  - v2_fixed_v1         : v1 != human AND v2 == human
  - v2_broke_v1         : v1 == human AND v2 != human
  - both_wrong_same     : v1 != human AND v2 != human AND v1 == v2
  - both_wrong_diff     : v1 != human AND v2 != human AND v1 != v2

If v2_fixed_v1 ≈ v2_broke_v1, that explains zero net κ change.

Outputs:
  output/validation/v1_v2_human_comparison.csv     (record-level detail)
  output/validation/v1_v2_diagnosis.md             (summary)
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parent
SHEET_PATH = REPO / "output/validation/kingsly_coding_sheet.xlsx"
FULL_PATH  = REPO / "output/validation/kingsly_validation_full.csv"
V2_PATH    = REPO / "output/classified_medical_Q1Q2_v2_pre_predclaim_fix.csv"
OUT_CSV    = REPO / "output/validation/v1_v2_human_comparison.csv"
OUT_MD     = REPO / "output/validation/v1_v2_diagnosis.md"

STANCE_ORDER = ["Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy"]


def main():
    sheet = pd.read_excel(SHEET_PATH)
    full = pd.read_csv(FULL_PATH)
    v2 = pd.read_csv(V2_PATH, dtype=str, low_memory=False)

    full["pmid"] = full["pmid"].astype(str)
    v2["pmid"] = v2["pmid"].astype(str)
    v2_lookup = dict(zip(v2["pmid"], v2["stance"]))
    v2_meta_lookup = dict(zip(v2["pmid"], v2.get("meta_discourse", pd.Series([""] * len(v2)))))

    # Merge: sheet has record_id, human_stance, human_notes. full has pmid, v1 stance.
    full_slim = full[["record_id", "pmid", "pub_year", "title", "stance"]].rename(
        columns={"stance": "v1_stance"}
    )
    df = sheet.merge(full_slim, on="record_id", how="inner", validate="one_to_one")
    df["v2_stance"] = df["pmid"].map(v2_lookup)
    df["v2_meta_discourse"] = df["pmid"].map(v2_meta_lookup).fillna("")

    df["human_stance"] = df["human_stance"].astype(str).str.strip()
    df["v1_stance"]    = df["v1_stance"].astype(str).str.strip()
    df["v2_stance"]    = df["v2_stance"].astype(str).str.strip()

    # Categorize
    def category(r):
        h, v1, v2 = r["human_stance"], r["v1_stance"], r["v2_stance"]
        if v2 == "FAILED":
            return "v2_failed"
        if v1 == h and v2 == h:
            return "both_correct"
        if v1 != h and v2 == h:
            return "v2_fixed_v1"
        if v1 == h and v2 != h:
            return "v2_broke_v1"
        if v1 != h and v2 != h:
            return "both_wrong_same" if v1 == v2 else "both_wrong_diff"
        return "?"

    df["category"] = df.apply(category, axis=1)
    df["v2_changed"] = (df["v1_stance"] != df["v2_stance"])

    # ===== Summary table =====
    cat_counts = df["category"].value_counts()
    n = len(df)
    print(f"\n=== Diagnostic (n={n}) ===\n")
    print(f"Records where v2 changed v1: {df['v2_changed'].sum()} ({df['v2_changed'].mean()*100:.1f}%)\n")

    order = ["both_correct", "v2_fixed_v1", "v2_broke_v1",
             "both_wrong_same", "both_wrong_diff", "v2_failed"]
    rows = []
    for cat in order:
        c = int(cat_counts.get(cat, 0))
        rows.append((cat, c, f"{c/n*100:.1f}%"))
        print(f"  {cat:<20} {c:>4}  ({c/n*100:.1f}%)")

    net_change = int(cat_counts.get("v2_fixed_v1", 0)) - int(cat_counts.get("v2_broke_v1", 0))
    print(f"\n  Net: v2_fixed - v2_broke = {net_change:+d}")
    print(f"  (positive = v2 better, negative = v2 worse, ~0 = wash)")

    # Drill into v2_broke_v1: what flow went wrong?
    broke = df[df["category"] == "v2_broke_v1"]
    print(f"\n=== v2_broke_v1 details (n={len(broke)}) ===")
    print("These are records where v1 matched human but v2 disagreed:\n")
    broke_flows = broke.groupby(["human_stance", "v2_stance"]).size().reset_index(name="n").sort_values("n", ascending=False)
    print(broke_flows.to_string(index=False))

    fixed = df[df["category"] == "v2_fixed_v1"]
    print(f"\n=== v2_fixed_v1 details (n={len(fixed)}) ===")
    print("These are records where v1 disagreed with human but v2 matched human:\n")
    fixed_flows = fixed.groupby(["v1_stance", "human_stance"]).size().reset_index(name="n").sort_values("n", ascending=False)
    print(fixed_flows.to_string(index=False))

    # Cross-tab of changes: what stance did v2 *prefer* on records it changed?
    changed = df[df["v2_changed"]]
    print(f"\n=== Among the {len(changed)} v2 changes (regardless of human): direction of flow ===")
    flow = changed.groupby(["v1_stance", "v2_stance"]).size().reset_index(name="n").sort_values("n", ascending=False)
    print(flow.to_string(index=False))

    # Save record-level CSV
    out_cols = ["record_id", "pmid", "pub_year", "title",
                "human_stance", "v1_stance", "v2_stance",
                "v2_meta_discourse", "category", "v2_changed",
                "human_notes"]
    out_cols = [c for c in out_cols if c in df.columns]
    df_out = df[out_cols].sort_values(["category", "record_id"])
    df_out.to_csv(OUT_CSV, index=False)
    print(f"\nWrote {OUT_CSV}")

    # Save markdown
    lines = []
    lines.append("# v1 vs v2 — diagnostic against human labels\n")
    lines.append(f"_n = {n} validation records_\n")
    lines.append("## Why is v2 κ ≈ v1 κ despite 19.9% of corpus relabelled?\n")
    lines.append("Categorization:\n")
    lines.append("| category | n | % |")
    lines.append("|---|---:|---:|")
    for cat, c, pct in rows:
        lines.append(f"| {cat} | {c} | {pct} |")
    lines.append("")
    lines.append(f"**Net v2_fixed − v2_broke = {net_change:+d}**\n")
    lines.append("Read:")
    lines.append(f"- v2_fixed_v1 = v2 corrected an error v1 made")
    lines.append(f"- v2_broke_v1 = v2 introduced an error on a record v1 had correct")
    lines.append(f"- A near-zero net difference means v2's gains and losses cancel out → κ unchanged.\n")

    lines.append("## v2_broke_v1 — records v1 had right, v2 got wrong\n")
    lines.append(f"n = {len(broke)}\n")
    lines.append("Flows (human stance → v2 stance):\n")
    lines.append("| human | v2 | n |")
    lines.append("|---|---|---:|")
    for _, r in broke_flows.iterrows():
        lines.append(f"| {r['human_stance']} | {r['v2_stance']} | {int(r['n'])} |")
    lines.append("")

    lines.append("## v2_fixed_v1 — records v1 got wrong, v2 corrected\n")
    lines.append(f"n = {len(fixed)}\n")
    lines.append("Flows (v1 stance → human stance):\n")
    lines.append("| v1 | human | n |")
    lines.append("|---|---|---:|")
    for _, r in fixed_flows.iterrows():
        lines.append(f"| {r['v1_stance']} | {r['human_stance']} | {int(r['n'])} |")
    lines.append("")

    lines.append("## Direction of v2's relabelling (independent of human)\n")
    lines.append(f"All v2 changes among the 300 validation records (n={len(changed)}):\n")
    lines.append("| v1 | v2 | n |")
    lines.append("|---|---|---:|")
    for _, r in flow.iterrows():
        lines.append(f"| {r['v1_stance']} | {r['v2_stance']} | {int(r['n'])} |")
    lines.append("")

    OUT_MD.write_text("\n".join(lines))
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
