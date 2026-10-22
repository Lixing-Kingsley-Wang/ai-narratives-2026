"""T6 · Missing-data accounting (E14; feeds the JARS flowchart, E10).

Counts records in/out at every pipeline stage, with the reason for each loss,
by publication year where relevant. Read-only. Log-derived counts are parsed
from the committed/local run logs in DATA_ROOT.
Outputs: revision_r1/outputs/T6_*.csv, T6_missing_data.md
"""

from __future__ import annotations

import re
import sys

import numpy as np
import pandas as pd

from r1_common import DATA_ROOT, OUT, REPO, REPO_OUT, load_v1, md_table, read_str

sys.path.insert(0, str(REPO))
from analysis.robustness import simplify_pubtype_7  # noqa: E402
from analysis.run_country_critical_map import resolve_country  # noqa: E402

YEARS = ["2018", "2020", "2021", "2022", "2023", "2024", "2025", "2026"]


def yr(df, col="year"):
    return df[col].astype(str).str.extract(r"(20\d{2}|19\d{2})")[0].fillna("missing")


def empty_abs(df):
    return df["abstract"].fillna("").astype(str).str.strip().str.len() == 0


def main():
    stages = []   # stage table
    byyear = {}   # stage -> Series by year

    fetch = (DATA_ROOT / "fetch.log").read_text(errors="ignore")
    m = re.search(r"Merged: (\d+) total → (\d+) deduplicated", fetch)
    n_monthly, n_dedup = int(m.group(1)), int(m.group(2))

    raw = read_str(DATA_ROOT / "raw_medical_all.csv")
    exc = read_str(DATA_ROOT / "filtered_medical_all_excluded.csv")
    unm = read_str(DATA_ROOT / "filtered_medical_all_unmatched.csv")
    q3 = read_str(DATA_ROOT / "filtered_medical_all_Q3.csv")
    q12 = read_str(DATA_ROOT / "filtered_medical_all_Q1Q2.csv")
    de = read_str(DATA_ROOT / "prefiltered_discourse_eval.csv")
    ap = read_str(DATA_ROOT / "prefiltered_application.csv")
    sjr_log = (DATA_ROOT / "sjr.log").read_text(errors="ignore")
    n_q12_pre = int(re.search(r"Q1\+Q2 \(primary corpus\):\s+(\d+)", sjr_log).group(1))
    n_q3_pre = int(re.search(r"Q3 \(comparison arm\):\s+(\d+)", sjr_log).group(1))
    # pre-cutoff Q1/Q2 per year from the sjr.log year breakdown
    pre = {}
    for y, q1, q2 in re.findall(r"(\d{4}):\s+\d+ total \| Q1=\s*(\d+) Q2=\s*(\d+)", sjr_log):
        pre[y] = int(q1) + int(q2)
    q12_y = yr(q12).value_counts()
    cutoff = pd.Series({y: pre.get(y, 0) - int(q12_y.get(y, 0)) for y in sorted(pre)})

    v1 = load_v1(year_range=None, drop_failed=False)
    failed = v1[v1["stance"] == "FAILED"]
    valid = v1[v1["stance"] != "FAILED"]
    analytic = valid[valid["pub_year"].between(2021, 2026)]
    crit = analytic[analytic["critical"]]

    th = pd.read_csv(REPO_OUT / "analysis/thematic_alarm.csv", dtype={"pmid": str}, low_memory=False)
    theme_log = (DATA_ROOT / "themes_batch_poll.log").read_text(errors="ignore")
    m_th = re.search(r"ended\s+succ=([\d,]+)\s+proc=\s*\d+\s+err=(\d+)", theme_log)
    th_err = int(m_th.group(2))
    only_other = th["themes"].fillna("").str.strip().eq("other")
    ac = pd.read_csv(REPO_OUT / "analyses/q7_classified_ac.csv", dtype={"pmid": str})
    spec = pd.read_csv(REPO_OUT / "specialty_classifications.csv", dtype={"pmid": str})
    geo = pd.read_csv(REPO_OUT / "geography_classifications.csv", dtype={"pmid": str})

    def add(stage, n_in, n_out, lost, reason, source, years=None):
        stages.append({"stage": stage, "records in": n_in, "records out": n_out, "excluded/missing": lost,
                       "reason": reason, "source": source})
        if years is not None:
            byyear[stage] = years

    add("1. PubMed retrieval (monthly windows, Jan 2021–Apr 2026)", "", n_monthly, "", "", "output/fetch.log")
    add("2. PMID de-duplication", n_monthly, n_dedup, n_monthly - n_dedup,
        "same PMID retrieved in more than one monthly window", "fetch.log; raw_medical_all.csv")
    add("3. Conference proceedings / preprints", len(raw), len(raw) - len(exc), len(exc),
        "journal on EXCLUDE_JOURNALS / EXCLUDE_KEYWORDS (sjr_filter.py)", "filtered_medical_all_excluded.csv", yr(exc).value_counts())
    add("4. SJR title matching", len(raw) - len(exc), n_q12_pre + n_q3_pre, len(unm),
        "normalised journal title not found in SCImago file for that year (unmatched)", "filtered_medical_all_unmatched.csv",
        yr(unm).value_counts())
    add("4b. SJR quartile Q3 (comparison arm, not primary)", "", n_q3_pre, n_q3_pre,
        "best quartile Q3; analysed separately (pre-cutoff count)", "sjr.log; filtered_medical_all_Q3.csv")
    add("5. April 2026 cover-date cutoff (Q1/Q2)", n_q12_pre, len(q12), n_q12_pre - len(q12),
        "PubDate May 2026 or later (records not retained on disk; per-year counts = sjr.log Q1+Q2 minus post-cutoff file)",
        "sjr.log; filtered_medical_all_Q1Q2.csv", cutoff)
    add("5b. Q3 cutoff", n_q3_pre, len(q3), n_q3_pre - len(q3), "same cutoff applied to Q3", "filtered_medical_all_Q3.csv")
    low_app = ap[ap["type_confidence"] == "Low"]
    add("6. AI-engagement prefilter", len(q12), len(de), len(ap),
        "classified application (AI as method), incl. failure-branch defaults", "prefiltered_application.csv", yr(ap, "pub_year").value_counts())
    add("6a. of which: prefilter failures defaulted to application (T1)", "", "", len(low_app),
        "non-succeeded batch result (9) or synchronous-path failure after 3 retries (87); see T1",
        "prefiltered_application.csv (type_confidence=Low)", yr(low_app, "pub_year").value_counts())
    add("7. Stance classification", len(de), len(valid), len(failed), "unparseable / empty response → FAILED",
        "classified_medical_Q1Q2.csv", failed["pub_year"].astype("string").fillna("missing").value_counts())
    out_win = valid[~valid["pub_year"].between(2021, 2026)]
    add("8. Year window 2021–2026", len(valid), len(analytic), len(out_win), "pub_year 2020 (PubDate earlier than retrieval PDAT)",
        "classified_medical_Q1Q2.csv", out_win["pub_year"].astype("string").value_counts())
    add("8b. Primary temporal window 2021–2025 (R1)", len(analytic), int(analytic["pub_year"].le(2025).sum()),
        int(analytic["pub_year"].eq(2026).sum()), "Jan–Apr 2026 partial year: descriptive only", "")
    add("9. Critical subset (Alarm or Caution)", len(analytic), len(crit), "", "theme and mechanism analyses run on critical records",
        "thematic_alarm.csv")
    add("10. Theme classification", len(th), len(th), 0,
        f"no record dropped; {th_err} non-succeeded batch result defaulted to ['other'] (log). "
        f"Records whose only theme is 'other': {int(only_other.sum())} (upper bound for fallbacks)",
        "themes_batch_poll.log; thematic_alarm.csv")
    n_fm_failed = int((ac["failure_mode"] == "FAILED").sum())
    add("11. Mechanism classification", len(ac), len(ac) - n_fm_failed, n_fm_failed, "FAILED after 3 retries",
        "q7_classified_ac.csv", ac.loc[ac["failure_mode"] == "FAILED", "pub_year"].astype(str).value_counts())
    acp = ac[ac["failure_mode"] != "FAILED"].merge(v1[["pmid", "has_abstract"]], on="pmid", how="left")
    to = acp[~acp["has_abstract"]]
    add("12. Title-only records within the parsed critical set", len(acp), len(acp) - len(to), len(to),
        "empty abstract (mechanism analyses restricted to abstract-present records)", "q7_classified_ac.csv + abstract",
        to["pub_year"].astype(str).value_counts())
    sp = analytic.merge(spec[["pmid", "specialty"]], on="pmid", how="left")
    sp_f = sp[sp["specialty"].isna() | (sp["specialty"] == "FAILED")]
    add("13. Specialty classification (analytic set)", len(sp), len(sp) - len(sp_f), len(sp_f),
        "specialty = FAILED (no JSON / outside vocabulary)", "specialty_classifications.csv", sp_f["pub_year"].astype(str).value_counts())
    n_spec_failed_all = int((spec["specialty"] == "FAILED").sum())
    g = analytic.merge(geo[["pmid", "country", "region"]], on="pmid", how="left")
    g["country_map"] = g["first_affiliation"].map(resolve_country)
    no_aff = g["first_affiliation"].fillna("").str.strip().eq("")
    unres_map = g["country_map"].isna()
    unres_geo = g["country"].isna() | g["country"].astype(str).str.strip().eq("")
    unk_region = g["region"].fillna("Unknown").isin(["Unknown", "Unresolved / unknown", ""])
    add("14a. First-author country (Figure 4 / Table S7 resolver)", len(g), int((~unres_map).sum()), int(unres_map.sum()),
        f"affiliation empty ({int(no_aff.sum())}) or no country string matched ({int((unres_map & ~no_aff).sum())})",
        "analysis/run_country_critical_map.py::resolve_country", g.loc[unres_map, "pub_year"].astype(str).value_counts())
    add("14b. First-author region (Table S9; geography_classifications.csv)", len(g), int((~unk_region).sum()), int(unk_region.sum()),
        "region 'Unknown' in geography_classifications.csv", "geography_classifications.csv",
        g.loc[unk_region, "pub_year"].astype(str).value_counts())
    pt = analytic["pub_type"].fillna("")
    seven = pt.map(simplify_pubtype_7)
    default_ra = seven.eq("Research Article")
    news = seven.eq("News")
    empty_pt = pt.str.strip().eq("")
    add("15. Publication type mapping", len(analytic), len(analytic), 0,
        f"no record unmapped: every record falls to a bucket. Default bucket 'Research Article' (no Editorial/Letter/Review/"
        f"Comment/News tag) = {int(default_ra.sum()):,}; News folded into Research Article = {int(news.sum())}; empty pub_type = {int(empty_pt.sum())}",
        "analysis/robustness.py::simplify_pubtype_7/5")

    st = pd.DataFrame(stages)
    st.to_csv(OUT / "T6_stage_table.csv", index=False)
    by = pd.DataFrame(byyear).fillna(0).astype(int)
    by = by.reindex([y for y in YEARS + ["missing"] if y in by.index] + [i for i in by.index if i not in YEARS + ["missing"]])
    by.index.name = "pub_year"
    by.loc["Total"] = by.sum()
    by.to_csv(OUT / "T6_losses_by_year.csv")

    # title-only / empty abstracts at each stage, by year
    sets = {"raw (116,117)": (raw, "year"), "excluded conf/preprint": (exc, "year"), "SJR unmatched": (unm, "year"),
            "Q1/Q2 eligible (97,492)": (q12, "year"), "prefilter: application": (ap, "pub_year"),
            "prefilter: retained (16,759)": (de, "pub_year"), "stance valid, 2021–2026 (16,747)": (analytic, "pub_year"),
            "critical (5,161)": (crit, "pub_year")}
    ta = []
    for name, (df, col) in sets.items():
        e = empty_abs(df)
        yy = df[col].astype(str).str.extract(r"(20\d{2}|19\d{2})")[0].fillna("missing")
        row = {"stage": name, "N": len(df), "empty abstract": int(e.sum()), "%": e.mean() * 100}
        for y in ["2021", "2022", "2023", "2024", "2025", "2026"]:
            mm = yy == y
            row[y] = f"{int((e & mm).sum())}/{int(mm.sum())}"
        ta.append(row)
    ta = pd.DataFrame(ta)
    ta.to_csv(OUT / "T6_title_only_by_stage.csv", index=False)

    # nested flow list
    F = []
    F.append(f"- Records identified in PubMed (monthly windows): {n_monthly:,}")
    F.append(f"  - Excluded: duplicate PMIDs across windows: {n_monthly - n_dedup:,}")
    F.append(f"- Unique records: {n_dedup:,}")
    F.append(f"  - Excluded: conference proceedings / preprints: {len(exc):,}")
    F.append(f"- Records eligible for SJR matching: {len(raw) - len(exc):,}")
    F.append(f"  - Excluded: journal not matched in SCImago: {len(unm):,}")
    F.append(f"  - Set aside: Q3 journals (comparison arm): {n_q3_pre:,} (after cutoff {len(q3):,})")
    F.append(f"- Q1/Q2 records: {n_q12_pre:,}")
    F.append(f"  - Excluded: cover date after April 2026: {n_q12_pre - len(q12):,}")
    F.append(f"- Q1/Q2 records screened by the AI-engagement prefilter: {len(q12):,}")
    F.append(f"  - Excluded: application (AI as method): {len(ap):,} (of which {len(low_app)} failure-branch defaults)")
    F.append(f"- Discourse or evaluative records: {len(de):,} (discourse {int((de.paper_type=='discourse').sum()):,}; evaluative {int((de.paper_type=='evaluative').sum()):,})")
    F.append(f"  - Excluded: stance unparseable: {len(failed)}")
    F.append(f"- Valid stance labels: {len(valid):,}")
    F.append(f"  - Excluded: dated 2020: {len(out_win)}")
    F.append(f"- Analytic set, 2021–April 2026: {len(analytic):,}")
    F.append(f"  - Reported separately (descriptive): January–April 2026: {int(analytic.pub_year.eq(2026).sum()):,}")
    F.append(f"  - Primary temporal set, 2021–2025: {int(analytic.pub_year.le(2025).sum()):,}")
    F.append(f"  - Specialty analyses: {len(sp) - len(sp_f):,} (excluded: specialty FAILED {len(sp_f)})")
    F.append(f"  - Country analyses: {int((~unres_map).sum()):,} resolved (unresolved {int(unres_map.sum()):,}; "
             f"{unres_map.mean()*100:.1f}%)")
    F.append(f"  - Critical (Alarm or Caution): {len(crit):,} → theme analysis {len(th):,} (fallback to ['other'] in {th_err} per batch log)")
    F.append(f"    - Mechanism classification: parsed {len(acp):,} (excluded: unparseable {n_fm_failed})")
    F.append(f"      - Excluded: title-only: {len(to)}")
    F.append(f"      - Abstract-present critical records: {len(acp) - len(to):,}")
    F.append(f"        - Hallucination-gated subset: {int(acp[acp.has_abstract].merge(th[['pmid','themes']], on='pmid').themes.str.contains('hallucination').sum()):,}")

    L = ["# T6 · Missing-data accounting (E14; feeds E10 flowchart)\n",
         "Script: `revision_r1/scripts/t6_missing_data.py`. Counts are recomputed from the pipeline files; "
         "log-derived counts (retrieval, pre-cutoff SJR totals, batch failures) are parsed from `output/*.log`.\n",
         "## 1. Stage table\n", md_table(st), "",
         "## 2. Losses by publication year\n",
         "Columns are stages from the table above (only stages with a per-year breakdown). 'missing' = no parseable year.\n",
         md_table(by.reset_index(), "{:.0f}"), "",
         "## 3. Title-only (empty abstract) records at each stage\n",
         "Cells are empty-abstract records / all records in that year.\n",
         md_table(ta, "{:.1f}"), "",
         "## 4. Other missing-data items\n",
         f"- Specialty FAILED in `specialty_classifications.csv` overall: {n_spec_failed_all} (of {len(spec):,}); within the "
         f"16,747 analytic set: {len(sp_f)}. Specialty labels exist only for the 16,759 retained records (see T9).",
         f"- First-author country: two resolvers exist. The Figure 4 / Table S7 resolver (`resolve_country`) leaves "
         f"{int(unres_map.sum()):,}/{len(g):,} ({unres_map.mean()*100:.1f}%) unresolved, i.e. {100-unres_map.mean()*100:.1f}% resolved "
         f"(manuscript: 90.3%). `geography_classifications.csv` (Table S9 regions) has region Unknown for "
         f"{int(unk_region.sum()):,} ({unk_region.mean()*100:.1f}%). Empty first-affiliation field: {int(no_aff.sum())}.",
         f"- Stance batch: one retrieval crashed on an empty `content` list (IndexError in `classify_stance_batch.py`, "
         f"`output/stance_batch_poll.log`) and was resumed; final FAILED = {len(failed)}.",
         f"- Theme batch: succeeded {m_th.group(1)}, errored {th_err} (`themes_batch_poll.log`); the errored record received "
         f"['other'] and cannot be distinguished from genuine 'other'-only records ({int(only_other.sum())}).",
         f"- SJR log reports Q1+Q2 = {n_q12_pre:,} as 88.1% of eligible (98,626/112,011 = {n_q12_pre/112011*100:.2f}%); the "
         f"manuscript says 88.0%.",
         "- Year field: retrieval used PDAT monthly windows; `pub_year` comes from `PubDate/Year` (or MedlineDate). Two "
         "records dated 2020 and one dated 2018 entered through PDAT windows (see T9).", "",
         "## 5. Nested flow list (for a JARS flowchart)\n"] + F
    (OUT / "T6_missing_data.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
