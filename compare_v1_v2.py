"""
Descriptive comparison of v1 (original prompt) vs v2 (revised prompt) stance
classifications. Joins on pmid, produces output/comparison_v1_v2.md.

Sections:
  1. Stance distribution comparison
  2. Migration matrix (v1 stance -> v2 stance)
  3. Largest migration flows (top 5, off-diagonal)
  4. predictive_claim flip counts
  5. v2 stance distribution by year

No kappa here. Step 6 is the kappa pass.
"""
import pandas as pd

V1_PATH = "output/classified_medical_Q1Q2.csv"
V2_PATH = "output/classified_medical_Q1Q2_v2.csv"
OUT_PATH = "output/comparison_v1_v2.md"

STANCE_ORDER = ["Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy", "FAILED"]


def fmt_pct(n, total):
    return f"{n / total * 100:.1f}%" if total else "—"


def main():
    print("Loading v1...")
    v1 = pd.read_csv(V1_PATH, dtype=str, low_memory=False)
    print(f"  v1 rows: {len(v1):,}")
    print("Loading v2...")
    v2 = pd.read_csv(V2_PATH, dtype=str, low_memory=False)
    print(f"  v2 rows: {len(v2):,}")

    # Verify pmid overlap
    v1_pmids = set(v1["pmid"])
    v2_pmids = set(v2["pmid"])
    only_v1 = v1_pmids - v2_pmids
    only_v2 = v2_pmids - v1_pmids
    common = v1_pmids & v2_pmids
    print(f"  common pmids: {len(common):,}  only_v1: {len(only_v1)}  only_v2: {len(only_v2)}")

    # Join on pmid
    keep_v1 = ["pmid", "title", "pub_year", "stance", "predictive_claim"]
    keep_v2 = ["pmid", "stance", "predictive_claim", "meta_discourse", "confidence"]
    j = v1[keep_v1].merge(
        v2[keep_v2], on="pmid", how="inner", suffixes=("_v1", "_v2")
    )
    print(f"  joined rows: {len(j):,}")

    lines = []
    lines.append("# v1 vs v2 stance classification — descriptive comparison\n")
    lines.append(f"- v1 file: `{V1_PATH}`")
    lines.append(f"- v2 file: `{V2_PATH}`")
    lines.append(f"- v1 rows: {len(v1):,}")
    lines.append(f"- v2 rows: {len(v2):,}")
    lines.append(f"- joined on pmid: {len(j):,}")
    if only_v1 or only_v2:
        lines.append(f"- only_v1: {len(only_v1)}   only_v2: {len(only_v2)}")
    lines.append("")

    # ===== Section 1: Stance distribution =====
    lines.append("## 1. Stance distribution\n")
    c1 = j["stance_v1"].value_counts()
    c2 = j["stance_v2"].value_counts()
    total = len(j)
    lines.append("| Stance | v1 n | v1 % | v2 n | v2 % | Δ n | Δ % |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    stances_seen = [s for s in STANCE_ORDER if s in c1.index or s in c2.index]
    for s in stances_seen:
        n1 = int(c1.get(s, 0))
        n2 = int(c2.get(s, 0))
        lines.append(
            f"| {s} | {n1:,} | {fmt_pct(n1, total)} | {n2:,} | {fmt_pct(n2, total)} | "
            f"{n2 - n1:+,} | {(n2 - n1) / total * 100:+.1f}pp |"
        )
    lines.append(f"| **Total** | **{total:,}** | 100.0% | **{total:,}** | 100.0% | | |")
    lines.append("")

    # ===== Section 2: Migration matrix =====
    lines.append("## 2. Migration matrix (v1 → v2)\n")
    mig = pd.crosstab(j["stance_v1"], j["stance_v2"])
    # Order rows/cols by STANCE_ORDER (only those present)
    row_order = [s for s in STANCE_ORDER if s in mig.index]
    col_order = [s for s in STANCE_ORDER if s in mig.columns]
    mig = mig.loc[row_order, col_order]
    lines.append("Rows = v1 stance, columns = v2 stance. Diagonal = unchanged.\n")
    header = "| v1 ↓ \\ v2 → | " + " | ".join(col_order) + " | row total |"
    lines.append(header)
    lines.append("|" + "---|" * (len(col_order) + 2))
    for r in row_order:
        cells = [f"{int(mig.loc[r, c]):,}" if c in mig.columns else "0" for c in col_order]
        lines.append(f"| **{r}** | " + " | ".join(cells) + f" | {int(mig.loc[r].sum()):,} |")
    col_totals = [f"{int(mig[c].sum()):,}" for c in col_order]
    lines.append("| **col total** | " + " | ".join(col_totals) + f" | {int(mig.values.sum()):,} |")
    lines.append("")

    n_unchanged = int(sum(mig.loc[s, s] for s in row_order if s in col_order))
    n_changed = total - n_unchanged
    lines.append(f"- Unchanged (diagonal): **{n_unchanged:,}** ({fmt_pct(n_unchanged, total)})")
    lines.append(f"- Changed: **{n_changed:,}** ({fmt_pct(n_changed, total)})")
    lines.append("")

    # ===== Section 3: Largest migration flows =====
    lines.append("## 3. Largest migration flows (top 5, off-diagonal)\n")
    flows = []
    for r in row_order:
        for c in col_order:
            if r == c:
                continue
            n = int(mig.loc[r, c]) if c in mig.columns else 0
            if n > 0:
                flows.append((n, r, c))
    flows.sort(reverse=True)
    top = flows[:5]
    for rank, (n, src, dst) in enumerate(top, 1):
        lines.append(f"### {rank}. {src} → {dst}  (n = {n:,})\n")
        examples = j[(j["stance_v1"] == src) & (j["stance_v2"] == dst)].head(5)
        lines.append("| pmid | pub_year | title (first 100 chars) |")
        lines.append("|---|---|---|")
        for _, row in examples.iterrows():
            title = (row["title"] or "")[:100].replace("|", "\\|")
            lines.append(f"| {row['pmid']} | {row['pub_year']} | {title} |")
        lines.append("")

    # ===== Section 4: predictive_claim flips =====
    lines.append("## 4. predictive_claim flag flips\n")
    # Normalize values (v1 used "yes"/"no", v2 same)
    p1 = j["predictive_claim_v1"].fillna("no").str.strip().str.lower()
    p2 = j["predictive_claim_v2"].fillna("no").str.strip().str.lower()
    flip_y2n = int(((p1 == "yes") & (p2 == "no")).sum())
    flip_n2y = int(((p1 == "no") & (p2 == "yes")).sum())
    same     = int((p1 == p2).sum())
    n_yes_v1 = int((p1 == "yes").sum())
    n_yes_v2 = int((p2 == "yes").sum())
    lines.append(f"- predictive_claim=yes in v1: **{n_yes_v1:,}** ({fmt_pct(n_yes_v1, total)})")
    lines.append(f"- predictive_claim=yes in v2: **{n_yes_v2:,}** ({fmt_pct(n_yes_v2, total)})")
    lines.append(f"- Unchanged: {same:,}")
    lines.append(f"- Flipped yes → no: {flip_y2n:,}")
    lines.append(f"- Flipped no → yes: {flip_n2y:,}")
    lines.append("")

    # ===== Section 5: v2 stance distribution by year =====
    lines.append("## 5. v2 stance distribution by year\n")
    by_year = pd.crosstab(j["pub_year"], j["stance_v2"])
    by_year = by_year[[c for c in STANCE_ORDER if c in by_year.columns]]
    by_year["total"] = by_year.sum(axis=1)
    # Sort by year ascending
    by_year = by_year.sort_index()
    cols = list(by_year.columns)
    lines.append("| year | " + " | ".join(cols) + " |")
    lines.append("|" + "---|" * (len(cols) + 1))
    for year, row in by_year.iterrows():
        lines.append(f"| {year} | " + " | ".join(f"{int(v):,}" for v in row) + " |")
    lines.append("")

    # ===== meta_discourse summary (bonus, since v2 has the new flag) =====
    lines.append("## 6. meta_discourse (v2 only, new field)\n")
    md = j["meta_discourse"].fillna("no").str.strip().str.lower()
    n_md = int((md == "yes").sum())
    lines.append(f"- meta_discourse=yes: **{n_md:,}** ({fmt_pct(n_md, total)})")
    lines.append("")
    if n_md > 0:
        md_by_stance = j[md == "yes"]["stance_v2"].value_counts()
        lines.append("Stance of meta-discourse papers (per v2 rubric: default Neutral unless authors editorialize):\n")
        lines.append("| stance_v2 | n |")
        lines.append("|---|---:|")
        for s in STANCE_ORDER:
            if s in md_by_stance.index:
                lines.append(f"| {s} | {int(md_by_stance[s]):,} |")
        lines.append("")

    out = "\n".join(lines) + "\n"
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"\nWrote {OUT_PATH}")

    # ===== Console summary =====
    print("\n=== SUMMARY ===")
    print(f"Total records compared: {total:,}")
    print(f"Unchanged: {n_unchanged:,} ({fmt_pct(n_unchanged, total)})")
    print(f"Changed:   {n_changed:,} ({fmt_pct(n_changed, total)})")
    print(f"Top 3 flows:")
    for n, src, dst in flows[:3]:
        print(f"  {src} → {dst}: {n:,}")
    print(f"predictive_claim flips: {flip_y2n + flip_n2y:,} (y→n {flip_y2n:,}; n→y {flip_n2y:,})")
    print(f"meta_discourse=yes (v2): {n_md:,} ({fmt_pct(n_md, total)})")


if __name__ == "__main__":
    main()
