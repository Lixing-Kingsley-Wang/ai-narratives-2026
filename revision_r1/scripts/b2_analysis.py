"""B2 analysis · stance of recovered records and augmented-corpus trends,
2021–2025 (JMIR R1 Batch 2b; D1, X2). Pre-specified in ANALYSIS_PLAN_batch2b.md.
Run with revision_r1/.venv (statsmodels for the weighted logistic model).
Outputs: revision_r1/outputs/B2/B2_analysis.md (+ csv)
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm

from r1_common import (OUT, STANCES, boot_indices, fmt_p, load_v1, logit_trend, md_table, read_str,
                       spearman_exact)

B2 = OUT / "B2"
Y5 = [2021, 2022, 2023, 2024, 2025]
EXF_PRECISION = {2021: 11 / 15, 2022: 12 / 15, 2023: 10 / 15, 2024: 11 / 15, 2025: 14 / 15}  # A3 primary
CATS = STANCES + ["Critical", "Favourable"]


def pe(p):
    f = fmt_p(p)
    return f"P{f}" if f.startswith("<") else f"P={f}"


def indicators(st):
    m = {s: (st == s).to_numpy(float) for s in STANCES}
    m["Critical"] = st.isin(["Alarm", "Caution"]).to_numpy(float)
    m["Favourable"] = st.isin(["Cautious Optimism", "Advocacy"]).to_numpy(float)
    return m


def annual(df, w):
    """Weighted annual shares for all categories + joint row bootstrap CIs (1000, seed 42)."""
    yr = df["year"].to_numpy(); ind = indicators(df["stance"])
    codes = np.array([Y5.index(y) for y in yr])

    def shares(idx):
        out = {}
        den = np.bincount(codes[idx], weights=w[idx], minlength=5)
        for c in CATS:
            out[c] = np.bincount(codes[idx], weights=(w * ind[c])[idx], minlength=5) / den * 100
        return out
    pt = shares(np.arange(len(df)))
    draws = {c: [] for c in CATS}
    for i in boot_indices(len(df)):
        s = shares(i)
        for c in CATS:
            draws[c].append(s[c])
    rows = []
    for c in CATS:
        D = np.array(draws[c]); lo, hi = np.percentile(D, [2.5, 97.5], axis=0)
        for j, y in enumerate(Y5):
            m = codes == j
            rows.append({"category": c, "year": y, "k_weighted": float((w * ind[c])[m].sum()), "N_weighted": float(w[m].sum()),
                         "k": int(ind[c][m].sum()), "N": int(m.sum()), "pct": pt[c][j], "lo": lo[j], "hi": hi[j]})
    return pd.DataFrame(rows)


def wlogit(df, w, cat):
    y = indicators(df["stance"])[cat]
    if np.all(w == 1):
        return logit_trend(df["year"].to_numpy(), y)
    x = df["year"].to_numpy(float); xc = x - np.average(x, weights=w)
    res = sm.GLM(y, sm.add_constant(xc), family=sm.families.Binomial(), freq_weights=w).fit(cov_type="HC0")
    b, se = res.params[1], res.bse[1]
    return {"OR": np.exp(b), "OR_lo": np.exp(b - 1.96 * se), "OR_hi": np.exp(b + 1.96 * se), "P_wald": res.pvalues[1]}


def main():
    prod = load_v1(year_range=(2021, 2025))[["pmid", "pub_year", "stance"]].rename(columns={"pub_year": "year"})
    prod["year"] = prod["year"].astype(int)
    a2 = read_str(OUT / "A2" / "a2_fullabstract_labels.csv")
    b2 = read_str(B2 / "b2_stance_labels.csv")
    rec = b2.merge(a2[["pmid", "year"]], on="pmid")
    n_rec_all = len(rec); n_failed = int((rec.failed == "1").sum())
    rec = rec[rec.failed != "1"].copy()
    rec["year"] = pd.to_numeric(rec["year"], errors="coerce")
    rec_all_years = rec.copy()
    rec = rec[rec.year.isin(Y5)][["pmid", "year", "stance"]]
    rec["year"] = rec["year"].astype(int)
    full_keep = set(a2.loc[a2.label_fullabstract.isin(["discourse", "evaluative"]), "pmid"])

    corpora = {
        "(a) Production": (prod, np.ones(len(prod))),
        "(b) Augmented": (pd.concat([prod, rec], ignore_index=True), np.ones(len(prod) + len(rec))),
        "(c) Precision-weighted augmented": (pd.concat([prod, rec], ignore_index=True),
                                             np.r_[np.ones(len(prod)), rec["year"].map(EXF_PRECISION).to_numpy()]),
        "(d) Full-abstract corpus": None,
    }
    dprod = prod[prod.pmid.isin(full_keep)]
    corpora["(d) Full-abstract corpus"] = (pd.concat([dprod, rec], ignore_index=True), np.ones(len(dprod) + len(rec)))

    L = ["# B2 · Stance of recovered records; augmented-corpus trends, 2021–2025 (D1, X2)\n",
         f"Recovered frame: {n_rec_all:,} records (production `application`, full-abstract discourse/evaluative; all years). "
         f"v1 stance FAILED after one resubmission: {n_failed}. With a valid stance and dated 2021–2025: {len(rec):,}. "
         f"Corpus (d) drops {len(prod) - len(dprod):,} production records (2021–2025) whose full-abstract label is "
         "`application`. EX-F precision weights for (c) (A3 primary): "
         + ", ".join(f"{y} {v:.3f}" for y, v in EXF_PRECISION.items()) + ".\n"]

    # recovered vs retained
    rows = []
    for name, df in (("Retained (production), 2021–2025", prod), ("Recovered, 2021–2025", rec),
                     ("Recovered, all years", rec_all_years)):
        vc = df["stance"].value_counts()
        rows.append({"set": name, "N": len(df), **{s: f"{vc.get(s, 0)/len(df)*100:.1f}% ({vc.get(s, 0)})" for s in STANCES},
                     "Critical": f"{df.stance.isin(['Alarm','Caution']).mean()*100:.1f}% ({int(df.stance.isin(['Alarm','Caution']).sum())})"})
    L += ["## Stance distribution: recovered vs retained\n", md_table(pd.DataFrame(rows)), ""]
    by = []
    for y in Y5:
        for name, df in (("retained", prod), ("recovered", rec)):
            s = df[df.year == y]["stance"]
            by.append({"year": y, "set": name, "N": len(s), **{st: f"{(s == st).mean()*100:.1f}% ({int((s == st).sum())})" for st in STANCES}})
    by = pd.DataFrame(by); by.to_csv(B2 / "B2_recovered_vs_retained_by_year.csv", index=False)
    L += ["By year:\n", md_table(by), ""]

    move, allann = [], []
    for name, (df, w) in corpora.items():
        an = annual(df, w); an.insert(0, "corpus", name); allann.append(an)
        L.append(f"## {name}: n = {len(df):,}" + (f" (weighted N = {w.sum():,.1f})" if not np.all(w == 1) else "") + "\n")
        piv = an.assign(cell=[f"{p:.1f} ({lo:.1f}–{hi:.1f}); {k:,}/{n:,}" if np.all(w == 1) else
                              f"{p:.1f} ({lo:.1f}–{hi:.1f}); {kw:,.1f}/{nw:,.1f}"
                              for p, lo, hi, k, n, kw, nw in zip(an.pct, an.lo, an.hi, an.k, an.N, an.k_weighted, an.N_weighted)])
        L += [md_table(piv.pivot(index="category", columns="year", values="cell").reindex(CATS).reset_index()), ""]
        for c in ("Critical", "Advocacy"):
            s = an[an.category == c].sort_values("year")
            rho, p, _ = spearman_exact(Y5, s.pct.to_numpy())
            lt = wlogit(df, w, c)
            move.append({"outcome": c, "corpus": name, "2021 %": round(s.pct.iloc[0], 2), "2025 %": round(s.pct.iloc[-1], 2),
                         "Δ pp": round(s.pct.iloc[-1] - s.pct.iloc[0], 2), "Spearman ρ (exact P)": f"{rho:+.2f} ({pe(p)})",
                         "OR/yr (95% CI), P": f"{lt['OR']:.3f} ({lt['OR_lo']:.3f}–{lt['OR_hi']:.3f}), {pe(lt['P_wald'])}"})
    pd.concat(allann).to_csv(B2 / "B2_annual_by_corpus.csv", index=False)
    M = pd.DataFrame(move).sort_values(["outcome", "corpus"])
    M.to_csv(B2 / "B2_trend_movement.csv", index=False)
    L += ["## Movement of trend estimates, (a) → (d)\n",
          "Logistic OR per year: unweighted for (a), (b), (d); for (c) a frequency-weighted GLM with HC0 robust SEs.\n",
          md_table(M), ""]
    (B2 / "B2_analysis.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:12])); print(M.to_string())


if __name__ == "__main__":
    main()
