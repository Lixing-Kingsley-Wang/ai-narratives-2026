"""T2 · Stance per-class performance and Advocacy robustness (D2b; supports X1).

Inputs (read-only):
  output/validation/kingsly_coding_sheet.xlsx, kingsly_validation_full.csv
  DATA_ROOT/classified_medical_Q1Q2.csv (corpus model labels)
Layer definitions copied from compute_kappa.py (flag regexes and masks).
Outputs: revision_r1/outputs/T2_*.csv, T2_stance_perclass.md
"""

from __future__ import annotations

import re
import sys

import numpy as np
import pandas as pd

from r1_common import (OUT, REPO_OUT, SEED, N_BOOT, STANCES, boot_indices, cohen_kappa_cm,
                       confusion, gwet_ac1_cm, binary_metrics_cm, load_v1, md_table,
                       per_class_prf, read_str)

S = STANCES
SHORT = {"Alarm": "Alarm", "Caution": "Caution", "Neutral": "Neutral",
         "Cautious Optimism": "Caut. Opt.", "Advocacy": "Advocacy"}

# Table S18 as submitted (Multimedia Appendix 3), rows human, cols model.
S18A = np.array([[31, 4, 0, 1, 0], [8, 33, 3, 14, 0], [0, 1, 10, 3, 0],
                 [1, 12, 10, 61, 9], [0, 0, 0, 7, 17]])
S18B = np.array([[31, 4, 0, 1, 0], [8, 34, 3, 14, 0], [0, 10, 57, 17, 4],
                 [1, 12, 10, 61, 9], [0, 0, 0, 7, 17]])

# compute_kappa.py flag regexes (verbatim)
RE_NO_STANCE = re.compile(r"(?:\[NO[_\- ]?STANCE\])|(?:(?:no|non)[\-\s]?stance)", re.IGNORECASE)
RE_OUT_OF_SCOPE = re.compile(r"(?:\[OUT[_\- ]?OF[_\- ]?SCOPE\])|(?:out[\-\s]of[\-\s]scope)"
                             r"|(?:not\s+related\s+topic)|(?:filter\s+problem)", re.IGNORECASE)
RE_DATA_INSUFFICIENT = re.compile(r"(?:\[DATA[_\- ]?INSUFFICIENT\])|(?:abstract\s+too\s+short)"
                                  r"|(?:data\s+insufficient)", re.IGNORECASE)

CRIT3 = {"Alarm": "critical", "Caution": "critical", "Neutral": "neutral",
         "Cautious Optimism": "favourable", "Advocacy": "favourable"}
L3 = ["critical", "neutral", "favourable"]


def load_validation():
    sheet = pd.read_excel(REPO_OUT / "validation/kingsly_coding_sheet.xlsx")
    full = pd.read_csv(REPO_OUT / "validation/kingsly_validation_full.csv", dtype={"pmid": str})
    m = sheet.merge(full[["record_id", "pmid", "pub_year", "stance", "abstract"]]
                    .rename(columns={"stance": "model", "pub_year": "year_full",
                                     "abstract": "abstract_full"}),
                    on="record_id", how="inner", validate="one_to_one")
    m["human"] = m["human_stance"].astype(str).str.strip()
    m["model"] = m["model"].astype(str).str.strip()
    notes = m["human_notes"].fillna("").astype(str)
    m["out_of_layerA"] = (notes.str.contains(RE_NO_STANCE) | notes.str.contains(RE_OUT_OF_SCOPE)
                          | notes.str.contains(RE_DATA_INSUFFICIENT))
    m["year"] = pd.to_numeric(m["year_full"], errors="coerce").astype(int)
    return m


def perclass_table(h, mo, labels, n_boot=N_BOOT, seed=SEED):
    h = np.asarray(h); mo = np.asarray(mo)
    point = per_class_prf(confusion(h, mo, labels), labels)
    draws = {l: {"precision": [], "recall": [], "F1": []} for l in labels}
    macro = []
    for idx in boot_indices(len(h), n_boot, seed):
        pc = per_class_prf(confusion(h[idx], mo[idx], labels), labels)
        for l in labels:
            for k in ("precision", "recall", "F1"):
                draws[l][k].append(pc[l][k])
        macro.append(np.nanmean([pc[l]["F1"] for l in labels]))
    rows = []
    for l in labels:
        r = {"class": l, "support_human": point[l]["support"],
             "n_model": int((mo == l).sum())}
        for k in ("precision", "recall", "F1"):
            lo, hi = np.nanpercentile(draws[l][k], [2.5, 97.5])
            r[k] = point[l][k]; r[f"{k}_lo"] = lo; r[f"{k}_hi"] = hi
        rows.append(r)
    mf = np.nanmean([point[l]["F1"] for l in labels])
    mlo, mhi = np.nanpercentile(macro, [2.5, 97.5])
    rows.append({"class": "macro-F1", "support_human": len(h), "n_model": len(h),
                 "precision": np.nan, "recall": np.nan, "F1": mf, "F1_lo": mlo, "F1_hi": mhi})
    return pd.DataFrame(rows)


def binary_table(hpos, mpos, n_boot=N_BOOT, seed=SEED):
    hpos = np.asarray(hpos, bool); mpos = np.asarray(mpos, bool)

    def met(idx):
        a, b = hpos[idx], mpos[idx]
        return binary_metrics_cm(int((a & b).sum()), int((a & ~b).sum()),
                                 int((~a & b).sum()), int((~a & ~b).sum()))
    full = met(np.arange(len(hpos)))
    draws = [met(i) for i in boot_indices(len(hpos), n_boot, seed)]
    tp = int((hpos & mpos).sum()); fn = int((hpos & ~mpos).sum())
    fp = int((~hpos & mpos).sum()); tn = int((~hpos & ~mpos).sum())
    nn = {"sensitivity": f"{tp}/{tp+fn}", "specificity": f"{tn}/{tn+fp}", "PPV": f"{tp}/{tp+fp}",
          "NPV": f"{tn}/{tn+fn}", "accuracy": f"{tp+tn}/{len(hpos)}",
          "prevalence_human": f"{tp+fn}/{len(hpos)}"}
    rows = []
    for k in ["sensitivity", "specificity", "PPV", "NPV", "F1", "accuracy", "kappa", "AC1",
              "prevalence_human"]:
        v = np.array([d[k] for d in draws], float)
        lo, hi = np.nanpercentile(v, [2.5, 97.5])
        rows.append({"metric": k, "n/N": nn.get(k, ""), "point": full[k], "lo": lo, "hi": hi})
    return pd.DataFrame(rows), (tp, fn, fp, tn)


def fmt_pc(df):
    out = []
    for _, r in df.iterrows():
        def c(k):
            if pd.isna(r.get(k)):
                return ""
            return f"{r[k]:.2f} ({r[k+'_lo']:.2f}–{r[k+'_hi']:.2f})"
        out.append({"class": r["class"], "support (human)": r["support_human"],
                    "n (model)": r["n_model"], "precision": c("precision"),
                    "recall": c("recall"), "F1": c("F1")})
    return pd.DataFrame(out)


def fmt_bin(df):
    return pd.DataFrame({"metric": df["metric"], "n/N": df["n/N"],
                         "estimate (95% CI)": [f"{p:.3f} ({l:.3f}–{h:.3f})" for p, l, h in
                                               zip(df["point"], df["lo"], df["hi"])]})


def cm_md(cm, labels, rlab="Human \\ Model"):
    df = pd.DataFrame(cm, index=labels, columns=labels)
    df["Row total"] = df.sum(axis=1)
    df.loc["Column total"] = df.sum(axis=0)
    df = df.reset_index().rename(columns={"index": rlab})
    return md_table(df, "{:.0f}")


def corrected_prevalence(val, corpus_years, corpus_stance, years, n_boot=N_BOOT, seed=SEED):
    """Corrected prevalence of human class h in year y:
       sum_c share_y(model=c) * P(human=h | model=c), P from validation within
       model-label stratum. Bootstrap: resample validation within model strata
       and corpus rows (whole 2021–2025 set) jointly, 1000 draws, seed 42."""
    vh = val["human"].to_numpy(); vm = val["model"].to_numpy()
    strata = {c: np.where(vm == c)[0] for c in S}
    cy = np.asarray(corpus_years); cs = np.asarray(corpus_stance)
    ycode = np.array([years.index(y) for y in cy]); scode = np.array([S.index(s) for s in cs])

    def cond(idx_by_c):
        P = np.zeros((5, 5))  # [model c, human h]
        for ci, c in enumerate(S):
            ix = idx_by_c[c]
            hh = vh[ix]
            for hi_, h in enumerate(S):
                P[ci, hi_] = np.mean(hh == h) if len(ix) else np.nan
        return P

    def shares(rows):
        M = np.zeros((len(years), 5))
        np.add.at(M, (ycode[rows], scode[rows]), 1)
        return M / M.sum(axis=1, keepdims=True)

    def corr(P, Sh):
        return Sh @ P  # years x human class

    P0 = cond(strata); Sh0 = shares(np.arange(len(cy)))
    point = corr(P0, Sh0)
    rng = np.random.default_rng(seed)
    dc, do = [], []
    for _ in range(n_boot):
        ib = {c: strata[c][rng.integers(0, len(strata[c]), len(strata[c]))] for c in S}
        rows = rng.integers(0, len(cy), len(cy))
        Sh = shares(rows)
        dc.append(corr(cond(ib), Sh)); do.append(Sh)
    return P0, Sh0, point, np.array(dc), np.array(do)


def main():
    v = load_validation()
    inA = v[~v["out_of_layerA"]].copy()
    cmA = confusion(inA["human"], inA["model"], S)
    cmB = confusion(v["human"], v["model"], S)
    okA = np.array_equal(cmA, S18A); okB = np.array_equal(cmB, S18B)
    L = ["# T2 · Stance per-class performance and Advocacy robustness (D2b; supports X1)\n",
         "Script: `revision_r1/scripts/t2_stance_perclass.py`. Validation inputs: "
         "`output/validation/kingsly_coding_sheet.xlsx` (human) joined to `kingsly_validation_full.csv` "
         "(model) on `record_id`; in-scope layer = compute_kappa.py 'Sensitivity A' (excludes NO_STANCE, "
         "OUT_OF_SCOPE, DATA_INSUFFICIENT flags in `human_notes`).\n",
         "## 1. Reproduction of Table S18\n",
         f"- (a) in-scope, n={len(inA)}: **{'reproduced exactly' if okA else 'MISMATCH'}**",
         f"- (b) all records, n={len(v)}: **{'reproduced exactly' if okB else 'MISMATCH'}**\n"]
    if not (okA and okB):
        L.append("Stopping T2 per instructions. Recomputed matrices:\n")
        L.append(cm_md(cmA, S)); L.append(""); L.append(cm_md(cmB, S))
        (OUT / "T2_stance_perclass.md").write_text("\n".join(L) + "\n")
        sys.exit("S18 mismatch")

    # Table S18(c) check
    rowsc = []
    for i, s in enumerate(S):
        n = cmA[i].sum(); ex = cmA[i, i]
        adj = sum(cmA[i, j] for j in (i - 1, i + 1) if 0 <= j < 5)
        rowsc.append((s, n, ex, adj))
    L.append("Table S18(c) exact and adjacent counts recomputed from (a): " +
             "; ".join(f"{s} {ex}/{n} exact, {adj} adjacent" for s, n, ex, adj in rowsc) + ".\n")

    # ---- 2. per-class ---------------------------------------------------
    pcA = perclass_table(inA["human"], inA["model"], S)
    pcB = perclass_table(v["human"], v["model"], S)
    pcA.to_csv(OUT / "T2_perclass_inscope225.csv", index=False)
    pcB.to_csv(OUT / "T2_perclass_all300.csv", index=False)
    L.append("## 2. Per-class precision, recall, F1 (bootstrap 95% CI, 1000 resamples, seed 42)\n")
    L.append("Precision = share of model-assigned labels that the human agreed with; recall = share of "
             "human-coded records the model labelled the same. Support = human row total.\n")
    L.append(f"**Primary: in-scope records (n={len(inA)})**\n")
    L.append(md_table(fmt_pc(pcA)))
    L.append(f"\n**Secondary: all records (n={len(v)})**\n")
    L.append(md_table(fmt_pc(pcB)))
    L.append("")

    # ---- 3. collapsed views ---------------------------------------------
    L.append("## 3. Collapsed views\n")
    out_rows = []
    for lay_name, d in [("in-scope (n=225)", inA), ("all (n=300)", v)]:
        h3 = d["human"].map(CRIT3); m3 = d["model"].map(CRIT3)
        cm3 = confusion(h3, m3, L3)
        L.append(f"### 3-class (critical / neutral / favourable), {lay_name}\n")
        L.append(cm_md(cm3, L3))
        L.append(f"\nRaw agreement {np.trace(cm3)}/{cm3.sum()} = {np.trace(cm3)/cm3.sum()*100:.1f}%; "
                 f"Cohen κ (unweighted) = {cohen_kappa_cm(cm3):.3f}; quadratic-weighted κ "
                 f"= {cohen_kappa_cm(cm3, 'quadratic'):.3f}; Gwet AC1 = {gwet_ac1_cm(cm3):.3f}.\n")
        pc3 = perclass_table(h3, m3, L3)
        pc3.insert(0, "layer", lay_name); out_rows.append(pc3)
        L.append(md_table(fmt_pc(pc3)))
        L.append("")
        for name, hp, mp in [("Advocacy vs not Advocacy", d["human"] == "Advocacy", d["model"] == "Advocacy"),
                             ("Critical (Alarm+Caution) vs not critical",
                              d["human"].isin(["Alarm", "Caution"]), d["model"].isin(["Alarm", "Caution"]))]:
            bt, (tp, fn, fp, tn) = binary_table(hp, mp)
            bt.insert(0, "view", name); bt.insert(0, "layer", lay_name)
            out_rows.append(bt)
            L.append(f"### Binary: {name}, {lay_name}\n")
            L.append(f"TP={tp}, FN={fn}, FP={fp}, TN={tn} (rows human, positive = {name.split(' vs')[0]}).\n")
            L.append(md_table(fmt_bin(bt)))
            L.append("")
    pd.concat(out_rows, ignore_index=True).to_csv(OUT / "T2_collapsed_views.csv", index=False)

    # ---- 4. non-adjacent --------------------------------------------------
    L.append("## 4. Non-adjacent disagreements (≥2 steps on the ordinal scale)\n")
    na_rows = []
    for lay_name, d in [("in-scope (n=225)", inA), ("all (n=300)", v)]:
        dist = (d["human"].map(S.index) - d["model"].map(S.index)).abs()
        disag = (dist > 0).sum()
        na = d[dist >= 2]
        na_rows.append({"layer": lay_name, "n": len(d), "disagreements": int(disag),
                        "adjacent (1 step)": int((dist == 1).sum()),
                        "2 steps": int((dist == 2).sum()), "3 steps": int((dist == 3).sum()),
                        "4 steps": int((dist == 4).sum()),
                        "non-adjacent total": int((dist >= 2).sum())})
    nadf = pd.DataFrame(na_rows)
    L.append(md_table(nadf, "{:.0f}"))
    dist_all = (v["human"].map(S.index) - v["model"].map(S.index)).abs()
    na_list = v.loc[dist_all >= 2, ["pmid", "year", "human", "model", "out_of_layerA"]].sort_values(["human", "model"])
    na_list.to_csv(OUT / "T2_nonadjacent_records.csv", index=False)
    L.append("\nPairs (all 300): " + "; ".join(f"human {a} → model {b}: {c}" for (a, b), c in
                                                 na_list.groupby(["human", "model"]).size().items()) + ".\n")

    # ---- 5. by year band ---------------------------------------------------
    L.append("## 5. Agreement by publication-year band (descriptive)\n")
    bands = {"2021–2022": [2021, 2022], "2023": [2023], "2024–2026": [2024, 2025, 2026]}
    yr_rows = []
    for lay_name, d in [("in-scope (n=225)", inA), ("all (n=300)", v)]:
        groups = list(bands.items()) + [(str(y), [y]) for y in sorted(d["year"].unique())
                                        if (d["year"] == y).sum() >= 20 and str(y) not in bands]
        for gname, ys in groups:
            sub = d[d["year"].isin(ys)]
            cm = confusion(sub["human"], sub["model"], S)
            hA = sub["human"] == "Advocacy"; mA = sub["model"] == "Advocacy"
            yr_rows.append({"layer": lay_name, "years": gname, "n": len(sub),
                            "exact agreement": f"{np.trace(cm)}/{len(sub)} ({np.trace(cm)/len(sub)*100:.1f}%)",
                            "quadratic κ": round(cohen_kappa_cm(cm, 'quadratic'), 3),
                            "unweighted κ": round(cohen_kappa_cm(cm), 3),
                            "critical: human/model": f"{int(sub['human'].isin(['Alarm','Caution']).sum())}/"
                                                     f"{int(sub['model'].isin(['Alarm','Caution']).sum())}",
                            "Advocacy: human/model/both": f"{int(hA.sum())}/{int(mA.sum())}/{int((hA & mA).sum())}"})
    yrdf = pd.DataFrame(yr_rows)
    yrdf.to_csv(OUT / "T2_agreement_by_year.csv", index=False)
    L.append(md_table(yrdf))
    L.append("\nValidation sample year distribution (all 300): " +
             ", ".join(f"{y}: {c}" for y, c in v["year"].value_counts().sort_index().items()) +
             ". Single years shown where n≥20.\n")

    # ---- 6. corrected prevalence -----------------------------------------
    corpus_all = load_v1(year_range=None)
    pool = corpus_all[corpus_all["stance"].isin(S) & corpus_all["has_abstract"]]
    pool_n = pool["stance"].value_counts()
    samp_n = v["model"].value_counts()
    sf = pd.DataFrame({"model stratum": S,
                       "sampling pool (valid stance, abstract present, all years)": [int(pool_n[s]) for s in S],
                       "sampled": [int(samp_n[s]) for s in S]})
    sf["sampling fraction"] = (sf["sampled"] / sf.iloc[:, 1]).map(lambda x: f"{x*100:.2f}%")
    sf["in-scope (layer A)"] = [int((inA["model"] == s).sum()) for s in S]
    sf.to_csv(OUT / "T2_sampling_fractions.csv", index=False)
    L.append("## 6. Misclassification-corrected annual prevalence, 2021–2025\n")
    L.append("**Sampling design (confirmed from `export_validation.py`):** stratified by model-assigned "
             "stance with fixed targets Alarm 40, Caution 60, Neutral 70, Cautious Optimism 100, Advocacy 30 "
             "(`STANCE_TARGETS`, `random.seed(42)`), from records with a valid stance **and a non-empty "
             "abstract** in `classified_medical_Q1Q2.csv` (all years, including 2020). Pool sizes below are "
             "recomputed from the current file.\n")
    L.append(md_table(sf))
    L.append("")

    corpus = load_v1(year_range=(2021, 2025))
    years = [2021, 2022, 2023, 2024, 2025]
    res_rows = []
    pmats = {}
    for lay_name, d in [("primary: all 300", v), ("sensitivity: in-scope 225", inA)]:
        for cname, cdf in [("all records", corpus),
                           ("abstract-present records only", corpus[corpus["has_abstract"]])]:
            P0, Sh0, point, dc, do = corrected_prevalence(d, cdf["pub_year"].astype(int), cdf["stance"], years)
            pmats[lay_name] = P0
            for yi, y in enumerate(years):
                for target, hidx in [("Advocacy", [4]), ("Critical", [0, 1])]:
                    obs = Sh0[yi, hidx].sum() * 100
                    olo, ohi = np.percentile(do[:, yi, hidx].sum(axis=1) * 100, [2.5, 97.5])
                    c = point[yi, hidx].sum() * 100
                    clo, chi = np.percentile(dc[:, yi, hidx].sum(axis=1) * 100, [2.5, 97.5])
                    res_rows.append({"validation set": lay_name, "corpus": cname, "outcome": target,
                                     "year": y, "n_year": int((cdf["pub_year"] == y).sum()),
                                     "observed %": obs, "obs_lo": olo, "obs_hi": ohi,
                                     "corrected %": c, "corr_lo": clo, "corr_hi": chi})
            for target, hidx in [("Advocacy", [4]), ("Critical", [0, 1])]:
                dd = (dc[:, 4, hidx].sum(axis=1) - dc[:, 0, hidx].sum(axis=1)) * 100
                od = (do[:, 4, hidx].sum(axis=1) - do[:, 0, hidx].sum(axis=1)) * 100
                lo_, hi_ = np.percentile(dd, [2.5, 97.5]); olo_, ohi_ = np.percentile(od, [2.5, 97.5])
                res_rows.append({"validation set": lay_name, "corpus": cname, "outcome": target,
                                 "year": "Δ 2025−2021 (pp)", "n_year": "",
                                 "observed %": (Sh0[4, hidx].sum() - Sh0[0, hidx].sum()) * 100,
                                 "obs_lo": olo_, "obs_hi": ohi_,
                                 "corrected %": (point[4, hidx].sum() - point[0, hidx].sum()) * 100,
                                 "corr_lo": lo_, "corr_hi": hi_})
    res = pd.DataFrame(res_rows)
    res.to_csv(OUT / "T2_corrected_prevalence.csv", index=False)

    L.append("**Estimator.** For year y and human class h: corrected prevalence = Σ_c (share of year-y corpus "
             "records with model label c) × P(human = h | model = c). P(h | c) is estimated within each "
             "model-label stratum of the validation set (stratified sampling makes this conditional unbiased "
             "within stratum). CIs: 1000 joint bootstrap draws (seed 42) resampling validation records within "
             "model strata and corpus records (2021–2025 set as a whole).\n")
    L.append("**Assumptions (stated plainly):** (i) P(human | model) is constant across years; (ii) the "
             "validation pool excluded title-only records, so applying P to all corpus records assumes "
             "title-only records are misclassified like abstract-present ones (an abstract-present-only "
             "corpus row is given as a check); (iii) in the primary analysis, records the human judged "
             "not codable/out of scope count as human Neutral (as in Table S18b).\n")
    for lay_name in pmats:
        P = pd.DataFrame(pmats[lay_name], index=[f"model:{SHORT[s]}" for s in S],
                         columns=[f"human:{SHORT[s]}" for s in S])
        L.append(f"P(human | model), {lay_name}:\n")
        L.append(md_table(P.reset_index().rename(columns={"index": ""}), "{:.3f}"))
        L.append("")
    for lay_name in ["primary: all 300", "sensitivity: in-scope 225"]:
        for cname in ["all records", "abstract-present records only"]:
            sub = res[(res["validation set"] == lay_name) & (res["corpus"] == cname)]
            L.append(f"**{lay_name}; corpus = {cname}**\n")
            t = []
            for _, r in sub.iterrows():
                t.append({"outcome": r["outcome"], "year": r["year"], "N (year)": r["n_year"],
                          "observed % (95% CI)": f"{r['observed %']:.2f} ({r['obs_lo']:.2f} to {r['obs_hi']:.2f})",
                          "corrected % (95% CI)": f"{r['corrected %']:.2f} ({r['corr_lo']:.2f} to {r['corr_hi']:.2f})"})
            L.append(md_table(pd.DataFrame(t)))
            L.append("")

    # ---- 7. Advocacy record list -------------------------------------------
    adv = v[(v["human"] == "Advocacy") | (v["model"] == "Advocacy")][
        ["pmid", "year", "human", "model", "out_of_layerA", "record_id"]].sort_values(["year", "pmid"])
    adv = adv.rename(columns={"out_of_layerA": "excluded_from_inscope_layer"})
    adv.to_csv(OUT / "T2_advocacy_records_for_review.csv", index=False)
    L.append("## 7. Records coded Advocacy by the human or the model (for Peter's review)\n")
    L.append(f"{len(adv)} records: both Advocacy {int(((adv.human=='Advocacy')&(adv.model=='Advocacy')).sum())}, "
             f"human only {int(((adv.human=='Advocacy')&(adv.model!='Advocacy')).sum())}, "
             f"model only {int(((adv.human!='Advocacy')&(adv.model=='Advocacy')).sum())}.\n")
    L.append(md_table(adv.drop(columns=["record_id"])))
    L.append("\n## Output files\n")
    for fn in ["T2_perclass_inscope225.csv", "T2_perclass_all300.csv", "T2_collapsed_views.csv",
               "T2_nonadjacent_records.csv", "T2_agreement_by_year.csv", "T2_sampling_fractions.csv",
               "T2_corrected_prevalence.csv", "T2_advocacy_records_for_review.csv"]:
        L.append(f"- [{fn}]({fn})")
    (OUT / "T2_stance_perclass.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
