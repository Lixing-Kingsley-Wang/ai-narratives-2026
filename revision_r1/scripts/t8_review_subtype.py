"""T8 · Review-subtype provenance (X5).

Quotes the rule that assigns 'Systematic Review' vs 'Review (narrative)',
tabulates which PubMed Publication Type tags land in each subtype (and how
Meta-Analysis is treated), and reproduces the Table S11 counts.
Output: revision_r1/outputs/T8_review_subtype.md (+ csv)
"""

from __future__ import annotations

import sys
from collections import Counter

import pandas as pd

from r1_common import OUT, REPO, STANCES, load_v1, md_table

sys.path.insert(0, str(REPO))
from analysis.robustness import simplify_pubtype_5, simplify_pubtype_7  # noqa: E402


def quote(path, start, end):
    lines = (REPO / path).read_text().split("\n")
    return "\n".join(f"{i:>4}  {lines[i-1]}" for i in range(start, end + 1))


def main():
    root_same = (REPO / "robustness.py").read_text() == (REPO / "analysis/robustness.py").read_text()
    df = load_v1(year_range=(2021, 2026))
    df["pt_raw"] = df["pub_type"].fillna("")
    df["pt7"] = df["pt_raw"].map(simplify_pubtype_7)
    df["pt5"] = df["pt_raw"].map(simplify_pubtype_5)
    df["subtype"] = df["pt7"].map({"Systematic Review": "Systematic Review", "Review": "Review (narrative)"})
    tags = df["pt_raw"].str.split(";").apply(lambda l: [t.strip() for t in l if t.strip()])

    # tags per subtype
    rows = []
    for st in ["Systematic Review", "Review (narrative)"]:
        c = Counter(t for l in tags[df.subtype == st] for t in l)
        n = int((df.subtype == st).sum())
        for t, k in c.most_common():
            rows.append({"subtype": st, "PubMed tag": t, "records carrying tag": k, "of subtype N": n})
    tagtab = pd.DataFrame(rows)
    tagtab.to_csv(OUT / "T8_tags_by_subtype.csv", index=False)

    has = lambda t: tags.apply(lambda l: t in l)
    ma = has("Meta-Analysis"); sr = has("Systematic Review"); rv = has("Review")
    ma_tab = pd.crosstab(df.loc[ma, "pt7"], [sr[ma].map({True: "SR tag", False: "no SR tag"})], margins=True)
    rev_lost = df[(sr | rv) & ~df["pt7"].isin(["Systematic Review", "Review"])]
    sr_lost = df[sr & (df["pt7"] != "Systematic Review")]
    narr = df[df.subtype == "Review (narrative)"]
    narr_noexact = narr[~rv[narr.index]]
    noexact_tags = Counter(t for l in tags[narr_noexact.index] for t in l if "Review" in t)

    # Table S11 reproduction
    s11 = []
    for st in ["Systematic Review", "Review (narrative)"]:
        sub = df[df.subtype == st]
        r = {"Subtype": st, "n": len(sub), "Critical %": sub["critical"].mean() * 100}
        for s in ["Alarm", "Caution", "Cautious Optimism", "Advocacy", "Neutral"]:
            r[f"{s} %"] = (sub["stance"] == s).mean() * 100
        s11.append(r)
    s11 = pd.DataFrame(s11)
    target = {"Systematic Review": (980, 29.3, 3.0, 26.3, 68.2, 0.3), "Review (narrative)": (4464, 23.9, 0.7, 23.2, 72.0, 2.1)}
    ok = all(int(r["n"]) == target[r["Subtype"]][0] and
             round(r["Critical %"], 1) == target[r["Subtype"]][1] and
             round(r["Alarm %"], 1) == target[r["Subtype"]][2] and round(r["Caution %"], 1) == target[r["Subtype"]][3] and
             round(r["Cautious Optimism %"], 1) == target[r["Subtype"]][4] and round(r["Advocacy %"], 1) == target[r["Subtype"]][5]
             for _, r in s11.iterrows())

    L = ["# T8 · Review-subtype provenance (X5)\n",
         "Script: `revision_r1/scripts/t8_review_subtype.py`.\n",
         "## 1. The rule (verbatim)\n",
         "File `analysis/robustness.py` (imported by the publication-type analyses, e.g. `analysis/run_pubtype_stance.py`, "
         "`analysis/run_reviews_positivity_why.py`); functions `simplify_pubtype_7` (lines 49–68) and `simplify_pubtype_5` "
         f"(lines 71–85). The repo-root copy `robustness.py` cited in Supplementary Note 1 is {'byte-identical' if root_same else 'NOT identical'}.\n",
         "```python", quote("analysis/robustness.py", 49, 85), "```\n",
         "So the subtype is decided **only by PubMed Publication Type strings** (case-sensitive substring test on the "
         "semicolon-joined `pub_type` field from `PublicationType` in the PubMed XML). No title/abstract text, no LLM, and no "
         "MeSH heading is used. 'Systematic Review' = the record carries the PubMed type `Systematic Review` (and no Editorial "
         "or Letter type, which take precedence). 'Review (narrative)' = carries `Review` but not `Systematic Review` (and no "
         "Editorial/Letter). The label 'narrative' is therefore a residual category: any PubMed `Review` that is not tagged "
         "`Systematic Review` (including every record tagged `Scoping Review` without `Systematic Review`; see sections 2–3). "
         "\n",
         "## 2. PubMed tags in each subtype\n",
         md_table(tagtab.groupby("subtype").head(12), "{:.0f}"),
         "\nFull list: [T8_tags_by_subtype.csv](T8_tags_by_subtype.csv).\n",
         "## 3. Meta-Analysis\n",
         "There is no Meta-Analysis rule. A record tagged `Meta-Analysis` goes wherever its other tags send it: to Systematic "
         "Review if it also carries `Systematic Review`, to Review (narrative) if it carries `Review` only, and to Research "
         "Article if it carries neither (the substring 'Review' does not occur in 'Meta-Analysis').\n",
         f"Records tagged Meta-Analysis in the analytic set: {int(ma.sum())}. Assigned bucket (rows) × presence of the "
         "Systematic Review tag:\n",
         md_table(ma_tab.reset_index(), "{:.0f}"), "",
         f"- Records carrying a `Review` or `Systematic Review` tag but assigned to Editorial or Letter by precedence: "
         f"{len(rev_lost)} ({', '.join(f'{k}: {v}' for k, v in rev_lost['pt7'].value_counts().items())}).",
         f"- Records carrying `Systematic Review` but not assigned to Systematic Review: {len(sr_lost)}.",
         f"- Because the test is a substring test, {len(narr_noexact)} of the {len(narr):,} 'Review (narrative)' records carry no "
         f"exact `Review` tag and were captured through another tag containing 'Review' "
         f"({', '.join(f'{k}: {v}' for k, v in noexact_tags.most_common())}).\n",
         "## 4. Reproduction of Table S11\n",
         f"**{'Reproduced exactly' if ok else 'MISMATCH'}** (n, critical, Alarm, Caution, Cautious Optimism, Advocacy to one decimal).\n",
         md_table(s11, "{:.1f}"), "",
         f"Both subtypes fold into the five-category 'Review' (n = {int((df.pt5 == 'Review').sum()):,} = 980 + 4,464).\n"]
    (OUT / "T8_review_subtype.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
