"""T1 · Prefilter validation metrics (D1, X2).

Inputs (read-only):
  DATA_ROOT/pilot_200_full_haiku.csv   human (my_label) vs Haiku (haiku_label)
  DATA_ROOT/pilot_200.xlsx, pilot_200_partial_{50,100}_haiku.csv (provenance)
  DATA_ROOT/prefiltered_discourse_eval.csv, prefiltered_application.csv
  DATA_ROOT/prefilter_batch_submit.log, prefilter.log (failure counts)
Outputs: revision_r1/outputs/T1_*.csv, T1_prefilter_validation.md
"""

from __future__ import annotations

import re

import numpy as np
import pandas as pd

from r1_common import (DATA_ROOT, OUT, N_BOOT, SEED, binary_metrics_cm, boot_indices,
                       cohen_kappa_cm, confusion, gwet_ac1_cm, md_table, pabak_cm,
                       read_str)

LAB3 = ["discourse", "evaluative", "application"]


def main():
    p = read_str(DATA_ROOT / "pilot_200_full_haiku.csv")
    p["h"] = p["my_label"].str.strip().str.lower()
    p["m"] = p["haiku_label"].str.strip().str.lower()
    assert set(p["h"]) <= set(LAB3) and set(p["m"]) <= set(LAB3), "unexpected labels"
    n = len(p)

    # ---- provenance ------------------------------------------------------
    xlsx = pd.read_excel(DATA_ROOT / "pilot_200.xlsx", dtype=str)
    xlsx_cols = list(xlsx.columns)
    p50 = read_str(DATA_ROOT / "pilot_200_partial_50_haiku.csv")
    p100 = read_str(DATA_ROOT / "pilot_200_partial_100_haiku.csv")
    final_lab = dict(zip(p["pmid"], p["h"]))
    final_m = dict(zip(p["pmid"], p["m"]))
    chg50 = sum(final_lab[r.pmid] != r.my_label.strip().lower() for r in p50.itertuples())
    chg100 = sum(final_lab[r.pmid] != r.my_label.strip().lower() for r in p100.itertuples())
    mchg50 = sum(final_m[r.pmid] != r.haiku_label.strip().lower() for r in p50.itertuples())
    mchg100 = sum(final_m[r.pmid] != r.haiku_label.strip().lower() for r in p100.itertuples())
    xl_lab = dict(zip(xlsx["pmid"].astype(str), xlsx["my_label"].astype(str).str.strip().str.lower()))
    chg_xlsx = sum(xl_lab.get(k) != v for k, v in final_lab.items())
    year_dist = p["year"].value_counts().sort_index()
    pubdate_years = p["pub_date"].str.extract(r"(20\d{2})")[0].value_counts().sort_index()
    corpus = read_str(DATA_ROOT / "filtered_medical_all_Q1Q2.csv")
    cy = corpus["year"].value_counts()
    yrs = [y for y in sorted(cy.index) if y in ("2021", "2022", "2023", "2024", "2025", "2026")]
    exp = np.array([cy[y] for y in yrs], dtype=float)
    exp = exp / exp.sum() * len(p)
    obs = np.array([int((p["year"] == y).sum()) for y in yrs])
    from scipy.stats import chisquare
    gof = chisquare(obs, exp)
    gof_tab = pd.DataFrame({"year": yrs, "pilot_n": obs, "expected_n_if_SRS": exp.round(1),
                            "corpus_n": [int(cy[y]) for y in yrs]})
    cmap = corpus.set_index("pmid")
    same_text = sum((cmap.loc[r.pmid, "title"] == r.title) and (cmap.loc[r.pmid, "abstract"] == r.abstract)
                    for r in p.itertuples())

    # production labels for the same PMIDs (production run = separate inference)
    de = read_str(DATA_ROOT / "prefiltered_discourse_eval.csv")
    ap = read_str(DATA_ROOT / "prefiltered_application.csv")
    prod = pd.concat([de[["pmid", "paper_type", "type_confidence", "pub_year"]],
                      ap[["pmid", "paper_type", "type_confidence", "pub_year"]]])
    prod_map = dict(zip(prod["pmid"], prod["paper_type"]))
    p["prod"] = p["pmid"].map(prod_map)
    in_prod = p["prod"].notna().sum()
    pilot_vs_prod = pd.crosstab(p["m"], p["prod"].fillna("not in production corpus"))
    agree_pp = (p["m"] == p["prod"]).sum()
    human_vs_prod_cm = confusion(p.loc[p["prod"].notna(), "h"],
                                 p.loc[p["prod"].notna(), "prod"], LAB3)

    # ---- 3x3 ---------------------------------------------------------------
    cm3 = confusion(p["h"], p["m"], LAB3)
    cm3_df = pd.DataFrame(cm3, index=[f"human:{l}" for l in LAB3],
                          columns=[f"model:{l}" for l in LAB3])
    cm3_df["row_total"] = cm3_df.sum(axis=1)
    cm3_df.loc["col_total"] = cm3_df.sum(axis=0)
    cm3_df.to_csv(OUT / "T1_confusion_3x3.csv")
    k3 = cohen_kappa_cm(cm3)
    raw3 = np.trace(cm3) / n
    h_arr = p["h"].to_numpy(); m_arr = p["m"].to_numpy()

    def k3_fn(idx):
        return cohen_kappa_cm(confusion(h_arr[idx], m_arr[idx], LAB3))
    k3_draws = [k3_fn(i) for i in boot_indices(n)]
    k3_lo, k3_hi = np.nanpercentile(k3_draws, [2.5, 97.5])
    recall3 = {l: cm3[i, i] / cm3[i].sum() for i, l in enumerate(LAB3)}

    # ---- binary KEEP vs DROP ---------------------------------------------
    hk = np.isin(h_arr, ["discourse", "evaluative"])
    mk = np.isin(m_arr, ["discourse", "evaluative"])

    def metrics(idx):
        a, b = hk[idx], mk[idx]
        tp = int((a & b).sum()); fn = int((a & ~b).sum())
        fp = int((~a & b).sum()); tn = int((~a & ~b).sum())
        return binary_metrics_cm(tp, fn, fp, tn)

    full = metrics(np.arange(n))
    draws = [metrics(i) for i in boot_indices(n)]
    rows = []
    for key in ["sensitivity", "specificity", "PPV", "NPV", "F1", "accuracy",
                "kappa", "AC1", "PABAK", "prevalence_human"]:
        vals = np.array([d[key] for d in draws], dtype=float)
        lo, hi = np.nanpercentile(vals, [2.5, 97.5])
        rows.append({"metric": key, "point": full[key], "ci_lo": lo, "ci_hi": hi,
                     "n_boot_valid": int(np.isfinite(vals).sum())})
    tp = int((hk & mk).sum()); fn = int((hk & ~mk).sum())
    fp = int((~hk & mk).sum()); tn = int((~hk & ~mk).sum())
    num = {"sensitivity": f"{tp}/{tp+fn}", "specificity": f"{tn}/{tn+fp}",
           "PPV": f"{tp}/{tp+fp}", "NPV": f"{tn}/{tn+fn}", "accuracy": f"{tp+tn}/{n}",
           "prevalence_human": f"{tp+fn}/{n}", "F1": "", "kappa": "", "AC1": "", "PABAK": ""}
    bin_df = pd.DataFrame(rows)
    bin_df["n/N"] = bin_df["metric"].map(num)
    bin_df.to_csv(OUT / "T1_binary_keep_drop_metrics.csv", index=False)
    cm2 = pd.DataFrame([[tp, fn, tp + fn], [fp, tn, fp + tn], [tp + fp, fn + tn, n]],
                       index=["human:KEEP", "human:DROP", "col_total"],
                       columns=["model:KEEP", "model:DROP", "row_total"])
    cm2.to_csv(OUT / "T1_confusion_2x2.csv")

    # binary metrics by pilot year (descriptive)
    by_year = []
    for y in sorted(p["year"].unique()):
        ix = np.where(p["year"].to_numpy() == y)[0]
        m = metrics(ix)
        a, b = hk[ix], mk[ix]
        by_year.append({"year": y, "n": len(ix), "human_KEEP": int(a.sum()),
                        "model_KEEP": int(b.sum()), "TP": int((a & b).sum()),
                        "FN": int((a & ~b).sum()), "FP": int((~a & b).sum()),
                        "TN": int((~a & ~b).sum()),
                        "sensitivity": m["sensitivity"], "specificity": m["specificity"]})
    by_year = pd.DataFrame(by_year)
    by_year.to_csv(OUT / "T1_binary_by_pilot_year.csv", index=False)

    # ---- silent exclusions ----------------------------------------------
    ap["pub_year_i"] = pd.to_numeric(ap["pub_year"], errors="coerce")
    de["pub_year_i"] = pd.to_numeric(de["pub_year"], errors="coerce")
    low_app = ap[ap["type_confidence"] == "Low"]
    by_y = (pd.DataFrame({
        "application_total": ap.groupby("pub_year_i").size(),
        "application_conf_Low": low_app.groupby("pub_year_i").size(),
        "retained_conf_Low": de[de["type_confidence"] == "Low"].groupby("pub_year_i").size(),
    }).fillna(0).astype(int))
    by_y.index.name = "pub_year"
    by_y.loc["All"] = by_y.sum()
    by_y.to_csv(OUT / "T1_silent_exclusion_upper_bound_by_year.csv")
    both = pd.concat([de, ap], ignore_index=True)
    conf_tab = pd.crosstab(both["paper_type"], both["type_confidence"])

    submit_log = (DATA_ROOT / "prefilter_batch_submit.log").read_text(errors="ignore")
    m_end = re.search(r"ended\s+succ=([\d,]+)\s+proc=\s*([\d,]+)\s+err=(\d+)", submit_log)
    succ = int(m_end.group(1).replace(",", "")); err = int(m_end.group(3))
    m_corpus = re.search(r"Corpus: ([\d,]+)\s+done: ([\d,]+)\s+pending: ([\d,]+)", submit_log)
    done_async = int(m_corpus.group(2).replace(",", ""))
    pending = int(m_corpus.group(3).replace(",", ""))
    unaccounted = pending - succ - err
    first_async = set(corpus["pmid"].iloc[:done_async])
    low_app = low_app.assign(path=np.where(low_app["pmid"].isin(first_async), "synchronous (prefilter.py)",
                                           "batch (prefilter_batch.py)"))
    by_path = pd.crosstab(low_app["pub_year_i"], low_app["path"], margins=True, margins_name="All")
    by_path.to_csv(OUT / "T1_fallback_Low_by_year_and_path.csv")
    n_conf_high = int((pd.concat([de, ap])["type_confidence"] == "High").sum())

    # ---- write markdown --------------------------------------------------
    f = lambda v: f"{v:.3f}"
    L = []
    L.append("# T1 · Prefilter validation metrics (D1, X2)\n")
    L.append("Script: `revision_r1/scripts/t1_prefilter_validation.py`. Inputs are the committed pilot "
             "files (`output/pilot_200_full_haiku.csv`, `output/pilot_200.xlsx`; byte-identical to the "
             "last committed versions at `31ed027^`) and the production prefilter outputs.\n")
    L.append("## 1. Pilot provenance\n")
    L.append("| Question | Finding | Evidence |\n|---|---|---|")
    L.append("| Same model? | Probably yes, not verifiable. The only pilot path in the code is `prefilter.py pilot` "
             "(model `claude-haiku-4-5-20251001`, same constant as `prefilter_batch.py`), but the script that "
             "wrote the pilot Haiku labels is not in the repository (row below). | "
             "`prefilter.py:19,106-112`; `prefilter_batch.py:34` |")
    L.append("| Same prompt? | Yes: `SYSTEM_PROMPT` and `build_prompt` are byte-identical in `prefilter.py` and "
             "`prefilter_batch.py`. | diff of the two blocks = identical |")
    L.append("| Same truncation (title + first 300 chars)? | Yes in code (`abstract[:300]` in both files). | "
             "`prefilter.py:51`; `prefilter_batch.py:71` |")
    L.append("| Same API path? | Pilot: unknown (the only pilot path in code is synchronous `prefilter.py`). "
             "Production was **mixed**, not Batch-only as Methods states: the first 2,500 records were run synchronously "
             "(`prefilter.py`, 3 retries) and the remaining 94,992 through one Message Batch. | "
             "`output/prefilter.log`; `output/prefilter_batch_submit.log` |")
    L.append("| Script that wrote `pilot_200_full_haiku.csv` | **Not found** in any branch. `prefilter.py pilot` "
             "writes `pilot_prefiltered_*.csv`, not a `haiku_label` column. The merge step is undocumented. | "
             "`git grep haiku_label` over all refs: no hit |")
    L.append(f"| Pilot labels vs production labels for the same PMIDs | {in_prod}/200 pilot PMIDs are in the "
             f"production corpus; pilot Haiku label = production Haiku label for {agree_pp}/{in_prod} "
             f"(two independent T=1.0 inferences). Title and abstract text identical to the corpus for "
             f"{same_text}/200. | table below |")
    L.append(f"| Human coder blind to model labels? | Consistent with blinding but **not provable from files**. "
             f"The coding workbook `pilot_200.xlsx` has columns {xlsx_cols} (no model label). Model labels "
             f"were generated in steps (50 → 100 → 200, file times 11:27, 11:55, 13:57 on 2026-05-09). "
             f"Human labels did not change between those steps: {chg50}/50 and {chg100}/100 changed vs the "
             f"final file; {chg_xlsx}/200 differ between the xlsx and the final csv. Model labels changed in "
             f"{mchg50}/50 and {mchg100}/100. | file comparison |")
    L.append(f"| Sampling | **Undocumented.** The committed `make_pilot.py` would draw 50 per year from 2021–2024 "
             f"only (unseeded `random.sample`), but the committed pilot has 2021–2026 records in proportions "
             f"close to the corpus year mix (χ² goodness of fit vs corpus mix, df={len(yrs)-1}: "
             f"χ²={gof.statistic:.2f}, P={gof.pvalue:.2f}). So `make_pilot.py` did not produce this file "
             f"as committed. The distribution is consistent with a simple random sample of the 97,492, but "
             f"no code or seed confirms it. | `make_pilot.py:16-19`; table below |")
    L.append("")
    L.append("Publication-year distribution of the 200 pilot records (`year` field):\n")
    L.append("| Year | n |\n|---|---|")
    for y, c in year_dist.items():
        L.append(f"| {y} | {c} |")
    L.append("")
    L.append("Pilot year mix vs corpus year mix (expected n under simple random sampling of 200):\n")
    L.append(md_table(gof_tab, "{:.1f}"))
    L.append("")
    L.append("Pilot Haiku label (rows) vs production Haiku label (columns), same PMIDs:\n")
    L.append(md_table(pilot_vs_prod.reset_index().rename(columns={"m": "pilot label"})))
    L.append("")
    L.append("**Implication for NPV (rule 4):** the sampling design is not documented. If the pilot was a simple "
             "random sample of the 97,492 eligible records (consistent with its year mix, unconfirmed), NPV can "
             "be applied to the excluded records; with n=170 model-DROP records the estimate is imprecise. "
             "This must be stated as an assumption, not a design property.\n")

    L.append("## 2. 3×3 confusion matrix (human rows, model columns), n=200\n")
    L.append(md_table(cm3_df.reset_index().rename(columns={"index": ""}), "{:.0f}"))
    L.append("")
    L.append(f"- Raw agreement {np.trace(cm3)}/{n} = {raw3*100:.1f}%. Cohen κ (3-class, unweighted) = "
             f"{k3:.3f} (95% CI {k3_lo:.3f}–{k3_hi:.3f}). Manuscript: 85.5%, κ 0.51 (0.35–0.68). Raw "
             f"agreement and point κ reproduce; the CI does **not** (the code that produced 0.347–0.676 is not in "
             f"any branch, so the bootstrap scheme cannot be checked). → discrepancy list.")
    L.append("- Per-class recall (human class correctly labelled by model): " +
             ", ".join(f"{l} {cm3[i,i]}/{cm3[i].sum()} = {recall3[l]*100:.1f}%" for i, l in enumerate(LAB3)))
    L.append("")
    L.append("## 3. Binary KEEP (discourse + evaluative) vs DROP (application)\n")
    L.append(md_table(cm2.reset_index().rename(columns={"index": ""}), "{:.0f}"))
    L.append("")
    L.append("Percentile bootstrap 95% CI, 1000 resamples of the 200 records, seed 42. Positive class = KEEP.\n")
    show = bin_df.copy()
    show["point"] = show["point"].map(f); show["ci_lo"] = show["ci_lo"].map(f); show["ci_hi"] = show["ci_hi"].map(f)
    L.append(md_table(show[["metric", "n/N", "point", "ci_lo", "ci_hi", "n_boot_valid"]]))
    L.append("")
    L.append("Descriptive, by pilot year (small n; no CIs):\n")
    L.append(md_table(by_year, "{:.3f}"))
    L.append("")
    L.append("Human-coded KEEP vs **production** label for the same PMIDs (sensitivity of the label actually "
             "used in the corpus):\n")
    hp = pd.DataFrame(human_vs_prod_cm, index=[f"human:{l}" for l in LAB3], columns=[f"prod:{l}" for l in LAB3])
    L.append(md_table(hp.reset_index().rename(columns={"index": ""}), "{:.0f}"))
    L.append("")

    L.append("## 4. Silent exclusions (default to `application`)\n")
    L.append("Rule (Supplementary Note 3): non-succeeded batch result, empty response, or JSON parse failure "
             "→ `paper_type=application`, `type_confidence=Low`. Raw responses were not stored, so the "
             "fallback records **cannot be identified individually** from the committed outputs.\n")
    L.append(f"- Synchronous path (`prefilter.py`): {done_async:,} records; failures after 3 retries also "
             "default to application/Low. No per-record error log survives (`output/prefilter.log` "
             "shows progress lines only).")
    L.append(f"- Batch path (`prefilter_batch.py`): {pending:,} records submitted in one batch. Final batch "
             f"status: succeeded={succ:,}, errored={err}. {unaccounted} further request(s) are not "
             f"counted as succeeded or errored in the logged line (canceled/expired are not printed). "
             f"So **{err + unaccounted} batch-level failures** (errored + unaccounted) defaulted to "
             f"application. Empty-response and parse-failure fallbacks were not logged (`n_err` "
             f"print line is absent from the logs) and cannot be counted.")
    L.append("- Upper bound by year: every fallback record has `type_confidence=Low`, but the model can also "
             "return Low itself. Counts of `application` + `Low` by year:\n")
    L.append(md_table(by_y.reset_index(), "{:.0f}"))
    L.append("")
    L.append("Confidence label × paper_type in production outputs (all 97,492):\n")
    L.append(md_table(conf_tab.reset_index(), "{:.0f}"))
    L.append("")
    L.append(f"**Inference: all {len(low_app)} `Low` records are fallbacks.** No record carries `High` "
             f"({n_conf_high} of 97,492): the parser keeps only the exact strings High/Medium/Low and forces "
             f"anything else to Medium, so the model's own confidence values were evidently never the exact "
             f"string `High` or `Low` (most likely lower-case). A `Low` therefore arises only from the fallback "
             f"branch. Cross-check: of the {len(low_app)} `Low` records, "
             f"{int((low_app['path'] == 'batch (prefilter_batch.py)').sum())} were written by the batch path, which "
             f"equals the {err + unaccounted} batch-level failures in the log; the rest came from the "
             f"synchronous first {done_async:,} records. Silent exclusions by year and path:\n")
    L.append(md_table(by_path.reset_index().rename(columns={"pub_year_i": "pub_year"}), "{:.0f}"))
    L.append("")
    L.append("Side finding: the stored `type_confidence` carries no information (Medium for every successful "
             "call).\n")
    L.append("## Output files\n")
    for fn_ in ["T1_confusion_3x3.csv", "T1_confusion_2x2.csv", "T1_binary_keep_drop_metrics.csv",
                "T1_binary_by_pilot_year.csv", "T1_silent_exclusion_upper_bound_by_year.csv",
                "T1_fallback_Low_by_year_and_path.csv"]:
        L.append(f"- [{fn_}]({fn_})")
    (OUT / "T1_prefilter_validation.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
