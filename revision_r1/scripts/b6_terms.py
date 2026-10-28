"""B6 · MeSH / keyword triangulation (JMIR R1 Batch 2b; D5). Pre-specified in
ANALYSIS_PLAN_batch2b.md. Reads outputs/B6/b6_mesh_keywords.csv.

Analysis 1: pre-specified lexicon trends among critical records, 2021–2025.
Analysis 2: emerging terms, 2024–2025 vs 2021–2022 (Monroe et al. 2008).
Analysis 3: terms separating critical vs favourable, 2021–2025.
Outputs: outputs/B6/*.csv, B6_terms.md; figures/B6_terms_r1_draft.{png,pdf}
"""

from __future__ import annotations

import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from r1_common import (DATA_ROOT, FIG, OUT, boot_group_share, fmt_p, load_v1, logit_trend, md_table,
                       read_str, spearman_exact)

B6 = OUT / "B6"
Y5 = [2021, 2022, 2023, 2024, 2025]
ALPHA0, MIN_DF, TOP = 1000.0, 20, 30

# Lexicons as in the plan (text terms; MeSH descriptors parsed per the plan's note).
LEX = {
    "Errors and hallucination": (["hallucinat*", "confabulat*", "fabricat*", "inaccura*", "misinformation", "error*",
                                  "incorrect", "factual*"], ["Diagnostic Errors", "Medical Errors"], "Hallucination / errors"),
    "Patient safety": (["patient safety", "safety", "harm*", "adverse"], ["Patient Safety", "Patient Harm"], "Patient safety"),
    "Regulation": (["regulat*", "governance", "oversight", "liability", "legislat*", "policy", "policies", "accountab*"],
                   ["Government Regulation", "Legislation as Topic", "Health Policy"], "Governance / regulation"),
    "Ethics and bias": (["ethic*", "bias*", "fairness", "equit*", "discriminat*", "justice"], ["Ethics, Medical", "Bias"],
                        "Ethics & bias"),
}


def pe(p):
    f = fmt_p(p)
    return f"P{f}" if f.startswith("<") else f"P={f}"


def term_regex(terms):
    parts = []
    for t in terms:
        if t.endswith("*"):
            parts.append(r"\b" + r"\s+".join(map(re.escape, t[:-1].split())) + r"\w*")
        else:
            parts.append(r"\b" + r"\s+".join(map(re.escape, t.split())) + r"\b")
    return re.compile("|".join(parts), re.IGNORECASE)


def mesh_list(s):
    return [m.rstrip("*") for m in (s or "").split("|") if m]


def monroe(df_i, df_j, prior):
    """Weighted log-odds with informative Dirichlet prior (Monroe, Colaresi & Quinn 2008).
    df_i, df_j, prior: Series indexed by term (document frequencies)."""
    terms = prior.index
    yi, yj = df_i.reindex(terms, fill_value=0), df_j.reindex(terms, fill_value=0)
    a = prior / prior.sum() * ALPHA0
    a0 = a.sum(); ni, nj = yi.sum(), yj.sum()
    delta = (np.log((yi + a) / (ni + a0 - yi - a)) - np.log((yj + a) / (nj + a0 - yj - a)))
    var = 1 / (yi + a) + 1 / (yj + a)
    return pd.DataFrame({"term": terms, "z": delta / np.sqrt(var), "delta": delta, "df_group1": yi.values,
                         "df_group2": yj.values})


def main():
    mk = read_str(B6 / "b6_mesh_keywords.csv")
    ret = read_str(DATA_ROOT / "prefiltered_discourse_eval.csv")[["pmid", "pub_year", "title", "abstract"]]
    ret = ret.merge(mk, on="pmid", how="left")
    ret["year"] = pd.to_numeric(ret["pub_year"], errors="coerce")
    ret["fetched"] = ret["mesh"].notna()
    ret["mesh"] = ret["mesh"].fillna(""); ret["keywords"] = ret["keywords"].fillna("")
    L = ["# B6 · MeSH and keyword triangulation (D5)\n",
         "Scripts `b6_fetch_mesh.py` (NCBI efetch, 84 batches of ≤200 PMIDs; raw XML gzipped locally in `outputs/B6/raw/`, "
         "SHA-256 manifest committed) and `b6_terms.py`. Retained records: 16,759; articles returned by NCBI: "
         f"{int(ret.fetched.sum()):,} (missing PMIDs listed in `b6_fetch_missing_pmids.txt`).\n"]

    # ---- completeness ------------------------------------------------------
    ret["has_mesh"] = ret["mesh"].str.len() > 0
    ret["has_kw"] = ret["keywords"].str.len() > 0
    comp = ret.groupby("year").agg(records=("pmid", "size"), with_mesh=("has_mesh", "sum"), with_keywords=("has_kw", "sum"))
    comp["mesh_%"] = comp.with_mesh / comp.records * 100
    comp["keywords_%"] = comp.with_keywords / comp.records * 100
    comp.loc["All"] = [comp.records.sum(), comp.with_mesh.sum(), comp.with_keywords.sum(),
                       comp.with_mesh.sum() / comp.records.sum() * 100, comp.with_keywords.sum() / comp.records.sum() * 100]
    comp.to_csv(B6 / "B6_completeness_by_year.csv")
    L += ["## Completeness by year (retained records)\n", md_table(comp.reset_index(), "{:.1f}"), ""]

    # ---- Analysis 1 ---------------------------------------------------------
    v = load_v1(year_range=(2021, 2025))
    th = pd.read_csv(OUT.parent.parent / "output/analysis/thematic_alarm.csv", dtype={"pmid": str}, usecols=["pmid", "themes"])
    cr = v[v["critical"]].merge(ret[["pmid", "mesh", "keywords"]], on="pmid", how="left").merge(th, on="pmid", how="left")
    cr[["mesh", "keywords"]] = cr[["mesh", "keywords"]].fillna("")
    text = (cr["title"].fillna("") + " " + cr["abstract"].fillna("") + " " + cr["keywords"].str.replace("|", " ; "))
    meshes = cr["mesh"].map(mesh_list)
    t4 = pd.read_csv(OUT / "T4_trend_tests.csv")
    t4 = t4[(t4.domain == "Theme (among critical)") & (t4.window == "2021–2025")].set_index("outcome")
    llm_key = {"Hallucination / errors": "hallucination", "Patient safety": "safety_clinical",
               "Governance / regulation": "regulation", "Ethics & bias": "ethics_bias"}
    rows, ann = [], []
    for name, (terms, mesh_terms, llm_lab) in LEX.items():
        rx = term_regex(terms)
        hit = text.str.contains(rx) | meshes.apply(lambda ms: any(m in mesh_terms for m in ms))
        tab = boot_group_share(cr["year"].to_numpy(), hit.to_numpy(), Y5)
        rho, p, _ = spearman_exact(Y5, tab["point"].to_numpy())
        lt = logit_trend(cr["year"].to_numpy(), hit.to_numpy())
        llm = t4.loc[llm_lab]
        llm_has = cr["themes"].fillna("").str.split("|").apply(lambda l: llm_key[llm_lab] in l)
        both = int((hit & llm_has).sum())
        rows.append({"lexicon theme": name, "records matched": f"{int(hit.sum()):,}/{len(cr):,}",
                     "2021 → 2025": f"{tab.point.iloc[0]:.1f}% ({int(tab.k.iloc[0])}/{int(tab.n.iloc[0])}) → {tab.point.iloc[-1]:.1f}% ({int(tab.k.iloc[-1])}/{int(tab.n.iloc[-1])})",
                     "Spearman ρ (exact P)": f"{rho:+.2f} ({pe(p)})",
                     "OR/yr (95% CI), P": f"{lt['OR']:.3f} ({lt['OR_lo']:.3f}–{lt['OR_hi']:.3f}), {pe(lt['P_wald'])}",
                     "LLM theme (T4) ρ / OR/yr": f"{llm.rho:+.2f} / {llm.OR_per_year:.3f}",
                     "same direction": "yes" if np.sign(lt["OR"] - 1) == np.sign(llm.OR_per_year - 1) else "no",
                     "overlap: lexicon∩LLM / lexicon / LLM": f"{both:,} / {int(hit.sum()):,} / {int(llm_has.sum()):,}"})
        for r in tab.itertuples():
            ann.append({"lexicon theme": name, "year": int(r.level), "k": int(r.k), "n": int(r.n), "pct": r.point, "lo": r.lo, "hi": r.hi})
    pd.DataFrame(ann).to_csv(B6 / "B6_lexicon_annual.csv", index=False)
    A1 = pd.DataFrame(rows); A1.to_csv(B6 / "B6_lexicon_trends.csv", index=False)
    L += ["## Analysis 1 · Pre-specified lexicon trends (critical records, 2021–2025)\n",
          "Match in title + abstract + author keywords (text lexicon) or MeSH descriptors. Annual shares with bootstrap CIs "
          "are in `B6_lexicon_annual.csv`.\n", md_table(A1), ""]

    # ---- term sets -------------------------------------------------------------
    def terms_of(r):
        ts = {re.sub(r"\s+", " ", m.lower()).strip() for m in mesh_list(r["mesh"])}
        ts |= {re.sub(r"\s+", " ", k.lower()).strip() for k in (r["keywords"] or "").split("|") if k.strip()}
        return ts
    ret["terms"] = ret.apply(terms_of, axis=1)
    bg = pd.Series([t for s in ret["terms"] for t in s]).value_counts()

    def compare(g1, g2, lab1, lab2, fname):
        d1 = pd.Series([t for s in g1 for t in s]).value_counts()
        d2 = pd.Series([t for s in g2 for t in s]).value_counts()
        res = monroe(d1, d2, bg)
        res = res[(res.df_group1 + res.df_group2) >= MIN_DF].sort_values("z", ascending=False)
        res.to_csv(B6 / fname, index=False)
        up = res.head(TOP).assign(direction=f"more in {lab1}")
        dn = res.tail(TOP).iloc[::-1].assign(direction=f"more in {lab2}")
        return pd.concat([up, dn]), len(g1), len(g2), len(res)

    r5 = ret[ret["year"].between(2021, 2025)]
    late, early = r5[r5.year.isin([2024, 2025])]["terms"], r5[r5.year.isin([2021, 2022])]["terms"]
    A2, n1, n2, nq = compare(late, early, "2024–2025", "2021–2022", "B6_emerging_terms_all.csv")
    vv = load_v1(year_range=(2021, 2025))[["pmid", "stance", "critical", "favourable"]].merge(ret[["pmid", "terms"]], on="pmid")
    A3, m1, m2, mq = compare(vv[vv.critical]["terms"], vv[vv.favourable]["terms"], "critical", "favourable",
                             "B6_stance_terms_all.csv")
    for lab, A, a, b, q, desc in (("Analysis 2 · Emerging terms (2024–2025 vs 2021–2022)", A2, n1, n2, nq, "records 2024–2025 / 2021–2022"),
                                  ("Analysis 3 · Terms separating stance (critical vs favourable, 2021–2025)", A3, m1, m2, mq, "critical / favourable records")):
        L += [f"## {lab}\n", f"{desc}: {a:,} / {b:,}; qualifying terms (≥{MIN_DF} records): {q:,}. Weighted log-odds with "
              f"informative Dirichlet prior (background = 16,759 retained records, α0 = {ALPHA0:,.0f}); z = δ/σ.\n"]
        show = A.assign(z=A.z.round(2))[["direction", "term", "z", "df_group1", "df_group2"]]
        L += [md_table(show, "{:.2f}"), ""]
    A2.to_csv(B6 / "B6_emerging_terms_top30.csv", index=False); A3.to_csv(B6 / "B6_stance_terms_top30.csv", index=False)

    # ---- figure ---------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(17, 19))
    for ax, A, title, c_up, c_dn in ((axes[0], A2, "Emerging terms: 2024–2025 vs 2021–2022", "#C0392B", "#2471A3"),
                                     (axes[1], A3, "Terms separating stance: critical vs favourable", "#C0392B", "#27AE60")):
        A = A.sort_values("z")
        y = np.arange(len(A))
        cols = [c_up if z > 0 else c_dn for z in A.z]
        ax.hlines(y, 0, A.z, color="#BBBBBB", lw=0.8)
        ax.scatter(A.z, y, color=cols, s=28, zorder=3)
        for yi, z in zip(y, A.z):
            ax.annotate(f"{z:.1f}", (z, yi), xytext=(5 if z > 0 else -5, 0), textcoords="offset points",
                        ha="left" if z > 0 else "right", va="center", fontsize=7)
        ax.set_yticks(y); ax.set_yticklabels(A.term, fontsize=7.5)
        ax.axvline(0, color="#555", lw=0.8)
        ax.set_xlabel("z-score (weighted log-odds, informative Dirichlet prior)")
        ax.set_title(title, fontsize=11, fontweight="bold")
        lim = np.abs(A.z).max() * 1.25
        ax.set_xlim(-lim, lim)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(FIG / f"B6_terms_r1_draft.{ext}", dpi=300, bbox_inches="tight", facecolor="white")
    L.append(f"Figure: `revision_r1/figures/B6_terms_r1_draft.png|pdf` (dot plot; z printed beside each dot). "
             f"Left: positive z = more frequent in 2024–2025. Right: positive z = more frequent in critical records.\n")
    (B6 / "B6_terms.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:30]))


if __name__ == "__main__":
    main()
