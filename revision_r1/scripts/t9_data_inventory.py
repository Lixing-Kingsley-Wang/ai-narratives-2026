"""T9 · Data inventory for Batch 2 (read-only; no API calls). D3, D4a, D5, D1/X2.

Outputs: revision_r1/outputs/T9_data_inventory.md (+ csv)
"""

from __future__ import annotations

import re

import numpy as np
import pandas as pd

from r1_common import DATA_ROOT, OUT, REPO, REPO_OUT, load_v1, md_table, read_str

MON = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}
# Pricing: claude-haiku-4-5, $1.00 input / $5.00 output per MTok (Anthropic first-party list price,
# claude-api skill table cached 2026-10-06); Message Batches API = 50% of standard.
PRICE_IN, PRICE_OUT, BATCH = 1.00, 5.00, 0.5
CHARS_PER_TOKEN = 4.0  # heuristic for English text; exact counts need messages.count_tokens (not called)


def month_kind(pd_str):
    s = (pd_str or "").strip()
    m = re.match(r"^(\d{4}) ([A-Z][a-z]{2})$", s)
    if m:
        return "PubDate Year+Month (Jan may be the parser default)", MON.get(m.group(2))
    if re.match(r"^\d{4} [A-Z][a-z]{2}-[A-Z][a-z]{2}", s) or re.match(r"^\d{4} [A-Z][a-z]{2} \d", s):
        return "MedlineDate range", MON.get(s[5:8])
    if re.match(r"^\d{4}-\d{4}", s) or re.match(r"^\d{4} (Spring|Summer|Fall|Autumn|Winter)", s):
        return "MedlineDate season/year range", None
    if re.match(r"^\d{4}$", s):
        return "year only", None
    return "other", None


def main():
    raw = read_str(DATA_ROOT / "raw_medical_all.csv")
    ana = load_v1(year_range=(2021, 2026))
    L = ["# T9 · Data inventory for Batch 2 (read-only)\n",
         "Script: `revision_r1/scripts/t9_data_inventory.py`. No API calls.\n"]

    # ---- 1. dates -----------------------------------------------------------
    L.append("## 1. Publication dates (D3)\n")
    L.append("Field used: `fetch_pubmed_medical.py::parse_pubmed_xml` (lines 179–187) reads `PubDate/Year` and "
             "`PubDate/Month` **with default `\"Jan\"` when Month is absent**, falling back to `PubDate/MedlineDate` "
             "(year = first 4 characters). `ArticleDate` (electronic publication date) and `PubDate/Day` are not read. "
             "Retrieval windows used `[PDAT]` month by month; `pub_year` (analysis) is from PubDate. Stored as the string "
             "`pub_date` (e.g. `2023 Mar`).\n")
    ana["kind"], ana["month"] = zip(*ana["pub_date"].map(month_kind))
    kt = pd.crosstab(ana["pub_year"], ana["kind"], margins=True, margins_name="All")
    L.append("Format of `pub_date` in the 16,747 analytic records, by year:\n")
    L.append(md_table(kt.reset_index(), "{:.0f}"))
    mm = ana[ana["month"].notna()]
    mt = pd.crosstab(mm["pub_year"], mm["month"].astype(int))
    jan_share = (mt[1] / mt.sum(axis=1) * 100).round(1)
    L.append("\nMonth distribution (records with a month), by year; January share is the check for the parser "
             "default (expected ≈ 8.3% if months were uniform; for 2026 the window is Jan–Apr):\n")
    mt2 = mt.copy(); mt2["Jan share %"] = jan_share
    L.append(md_table(mt2.reset_index(), "{:.1f}"))
    mt.to_csv(OUT / "T9_month_by_year.csv")
    q = mm[mm["pub_year"] <= 2025].copy()
    q["quarter"] = ((q["month"].astype(int) - 1) // 3 + 1)
    qt = pd.crosstab(q["pub_year"], q["quarter"], margins=True)
    qt_crit = q.groupby(["pub_year", "quarter"])["critical"].agg(["sum", "size"])
    L.append("\nRecords per quarter, 2021–2025 (analytic set; month as stored, so Q1 includes any Jan defaults):\n")
    L.append(md_table(qt.reset_index(), "{:.0f}"))
    L.append(f"\nSmallest quarter: {int(qt_crit['size'].min())} records; critical records per quarter range "
             f"{int(qt_crit['sum'].min())}–{int(qt_crit['sum'].max())}. Records without a month: "
             f"{int(ana[(ana.pub_year <= 2025) & ana.month.isna()].shape[0])} (2021–2025).\n")
    qt_crit.to_csv(OUT / "T9_quarter_counts_2021_2025.csv")

    # ---- 2. journals --------------------------------------------------------
    L.append("## 2. Journal identifiers (D4a)\n")
    L.append(f"Stored columns: {list(raw.columns)}. **No NLM Unique ID and no ISSN** are stored (the parser reads "
             "`Journal/Title` and `Journal/ISOAbbreviation` only). ISSN is available indirectly from the SJR files (`Issn` "
             "column) through the same title match used for quartiles.\n")
    jt = ana["journal"].str.strip().str.lower()
    per = jt.value_counts()
    d = per.describe(percentiles=[.25, .5, .75, .9, .99])
    L.append(f"Unique journals in the analytic set (exact `journal` string, case-folded): **{per.size:,}**; by ISO "
             f"abbreviation: {ana['journal_abbr'].str.strip().str.lower().nunique():,}.\n")
    dist = pd.DataFrame({"statistic": ["journals", "records", "mean", "min", "25%", "median", "75%", "90%", "99%", "max",
                                       "journals with 1 record", "journals with ≥10", "journals with ≥50",
                                       "records in top 20 journals"],
                         "value": [per.size, int(per.sum()), round(d["mean"], 2), d["min"], d["25%"], d["50%"], d["75%"],
                                   d["90%"], d["99%"], d["max"], int((per == 1).sum()), int((per >= 10).sum()),
                                   int((per >= 50).sum()), int(per.head(20).sum())]})
    L.append(md_table(dist, "{:.0f}"))
    top = per.head(15).reset_index(); top.columns = ["journal", "records"]
    L.append("\nTop 15 journals by records:\n"); L.append(md_table(top, "{:.0f}"))
    per.rename("records").to_csv(OUT / "T9_records_per_journal.csv")

    # ---- 3. MeSH / keywords -----------------------------------------------
    L.append("\n## 3. MeSH headings and author keywords (D5)\n")
    has_mesh = any("mesh" in c.lower() or "keyword" in c.lower() for c in raw.columns)
    xml_files = list(REPO.glob("**/*.xml"))
    L.append(f"**Not stored.** No MeSH or keyword column in any corpus CSV (has_mesh_column = {has_mesh}); the parser "
             "does not read `MeshHeadingList` or `KeywordList`, and the raw PubMed XML was not saved "
             f"({len(xml_files)} .xml files in the repository). Completeness by year therefore cannot be measured "
             "locally; it requires an E-utilities `efetch` of the 16,759 retained PMIDs (not done).\n")

    # ---- 4. affiliations ----------------------------------------------------
    L.append("## 4. Affiliations (D5)\n")
    L.append("Only the **first author's first affiliation** is stored (`first_affiliation`: `authors[0]` → first "
             "`AffiliationInfo/Affiliation`, `fetch_pubmed_medical.py` lines 193–201). Other authors' affiliations, "
             "secondary affiliations of the first author, and the author count are not stored, and no raw XML is "
             f"available locally. Empty `first_affiliation` in the analytic set: "
             f"{int(ana['first_affiliation'].fillna('').str.strip().eq('').sum())}.\n")

    # ---- 5. excluded records ------------------------------------------------
    L.append("## 5. Excluded `application` records (D1, X2)\n")
    ap = read_str(DATA_ROOT / "prefiltered_application.csv")
    q12 = read_str(DATA_ROOT / "filtered_medical_all_Q1Q2.csv").set_index("pmid")
    has_abs = ap["abstract"].str.strip().str.len() > 0
    alen = ap["abstract"].str.len()
    # truncation check vs the pre-prefilter corpus
    same = (q12.loc[ap["pmid"], "abstract"].values == ap["abstract"].values).mean() * 100
    # read SYSTEM_PROMPT from source text (importing prefilter_batch would load .env)
    src = (REPO / "prefilter_batch.py").read_text()
    sys_chars = len(re.search(r'SYSTEM_PROMPT = """(.*?)"""', src, re.S).group(1))
    user_chars = ("Classify this paper:\n\nTitle: " + ap["title"] + np.where(has_abs, "\nAbstract: " + ap["abstract"], "")).str.len()
    in_tok = (sys_chars + user_chars) / CHARS_PER_TOKEN + 10  # +10 message framing
    in_tok_300 = (sys_chars + ("Classify this paper:\n\nTitle: " + ap["title"] +
                               np.where(has_abs, "\nAbstract: " + ap["abstract"].str.slice(0, 300), "")).str.len()) / CHARS_PER_TOKEN + 10
    out_tok_per = 25
    tot_in, tot_out = float(in_tok.sum()), out_tok_per * len(ap)
    cost_std = tot_in / 1e6 * PRICE_IN + tot_out / 1e6 * PRICE_OUT
    cost_batch = cost_std * BATCH
    by_y = ap.assign(y=ap["pub_year"], has=has_abs).groupby("y").agg(records=("pmid", "size"), with_abstract=("has", "sum"))
    L.append(f"- Q1/Q2 records labelled `application`: **{len(ap):,}** (of which 96 are failure-branch defaults, T1).")
    L.append(f"- Full abstracts stored locally: {int(has_abs.sum()):,} ({has_abs.mean()*100:.1f}%) have a non-empty abstract; "
             f"{int((~has_abs).sum())} are title-only. Abstracts are stored untruncated (identical to the pre-prefilter corpus "
             f"for {same:.1f}% of records; truncation to 300 characters happened only in the prompt). Abstract length: "
             f"median {int(alen[has_abs].median()):,} characters, 95th percentile {int(alen[has_abs].quantile(.95)):,}.")
    L.append("\nBy year:\n"); L.append(md_table(by_y.reset_index().rename(columns={"y": "pub_year"}), "{:.0f}"))
    L.append(f"\n**Cost estimate for re-running the prefilter on title + full abstract** (model `claude-haiku-4-5-20251001`, "
             f"Batch API, same system prompt, max_tokens 120):\n")
    est = pd.DataFrame({"item": ["requests", "input tokens (est.)", "  per request, median", "output tokens (est., 25/request)",
                                 "price (Haiku 4.5, per MTok)", "standard cost", "Batch API cost (50%)",
                                 "for comparison: input tokens with 300-char truncation"],
                        "value": [f"{len(ap):,}", f"{tot_in/1e6:.1f} M", f"{int(np.median(in_tok)):,}", f"{tot_out/1e6:.2f} M",
                                  f"${PRICE_IN:.2f} in / ${PRICE_OUT:.2f} out", f"${cost_std:,.0f}", f"**${cost_batch:,.0f}**",
                                  f"{in_tok_300.sum()/1e6:.1f} M"]})
    L.append(md_table(est))
    L.append(f"\nAssumptions: tokens ≈ characters / {CHARS_PER_TOKEN:.0f} (heuristic; `messages.count_tokens` would give exact "
             "counts but was not called); 25 output tokens per JSON reply; no prompt caching (the system prompt, "
             f"{sys_chars:,} characters, is below the minimum cacheable prefix). Prices are Anthropic first-party list "
             "prices for Claude Haiku 4.5 ($1/$5 per MTok) with the 50% Batch discount; confirm before running. A run "
             "on all 97,492 eligible records would cost roughly "
             f"${cost_batch * 97492 / len(ap):,.0f} (Batch).\n")

    # ---- 6. specialty -----------------------------------------------------
    spec = pd.read_csv(REPO_OUT / "specialty_classifications.csv", dtype={"pmid": str})
    de = read_str(DATA_ROOT / "prefiltered_discourse_eval.csv")
    L.append("## 6. Specialty labels\n")
    L.append(f"`output/specialty_classifications.csv` has {len(spec):,} rows; PMID set equals the 16,759 retained "
             f"(discourse + evaluative) records: **{set(spec.pmid) == set(de.pmid)}**. Overlap with the 80,733 "
             f"application records: {len(set(spec.pmid) & set(ap.pmid))}. So specialty labels exist only for retained "
             "records (confirmed).\n")
    (OUT / "T9_data_inventory.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
