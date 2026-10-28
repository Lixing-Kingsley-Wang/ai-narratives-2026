"""B3 analysis · symmetric 'strong endorsement' scale (JMIR R1 Batch 2b; X1, D2b).
Pre-specified in ANALYSIS_PLAN_batch2b.md.

Flag FAILED records (no resubmission was possible; see report) stay in every
denominator and are not counted as Strong endorsement; an upper bound that
counts them as 'yes' is reported beside the trend.
Outputs: revision_r1/outputs/B3/B3_analysis.md (+ csv)
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import beta

from r1_common import (OUT, SEED, N_BOOT, STANCES, binary_metrics_cm, boot_group_share, boot_indices, cohen_kappa_cm,
                       fmt_p, load_v1, logit_trend, md_table, read_str, spearman_exact)
from t2_stance_perclass import load_validation

B3 = OUT / "B3"
Y5 = [2021, 2022, 2023, 2024, 2025]
SYM = ["Alarm", "Caution", "Neutral", "Cautious Optimism (flag no)", "Strong endorsement (flag yes)", "Favourable, flag FAILED"]


def pe(p):
    f = fmt_p(p)
    return f"P{f}" if f.startswith("<") else f"P={f}"


def cp(k, n):
    return (0.0 if k == 0 else beta.ppf(0.025, k, n - k + 1)) * 100, (1.0 if k == n else beta.ppf(0.975, k + 1, n - k)) * 100


def sym_label(stance, flag):
    if stance in ("Alarm", "Caution", "Neutral"):
        return stance
    return {"yes": SYM[4], "no": SYM[3]}.get(flag, SYM[5])


def main():
    fl = read_str(B3 / "b3_endorsement_labels.csv")[["pmid", "strong_endorsement", "failed"]]
    v = load_v1(year_range=(2021, 2026)).merge(fl, on="pmid", how="left")
    v["flag"] = v["strong_endorsement"].fillna("")
    v["year"] = v["pub_year"].astype(int)
    v["sym"] = [sym_label(s, f) for s, f in zip(v.stance, v.flag)]
    fav = v[v.stance.isin(["Cautious Optimism", "Advocacy"])]
    n_failed = int((fav.failed == "1").sum())
    L = ["# B3 · Symmetric endorsement re-classification (X1, D2b)\n",
         f"Favourable records classified: {len(fav):,} (2021–Apr 2026); flag yes {int((fav.flag == 'yes').sum()):,}, "
         f"no {int((fav.flag == 'no').sum()):,}, FAILED {n_failed} (model wrote prose before the JSON within max_tokens 30; "
         "resubmission was refused by the API for insufficient credit). FAILED records stay in denominators and are not "
         "counted as Strong endorsement.\n"]

    # 1. symmetric scale
    rows = []
    for lab, ys in [("2021–2025", Y5)] + [(str(y), [y]) for y in Y5] + [("Jan–Apr 2026", [2026])]:
        s = v[v.year.isin(ys)]["sym"]
        rows.append({"period": lab, "N": len(s), **{c: f"{(s == c).mean()*100:.1f}% ({int((s == c).sum()):,})" for c in SYM}})
    T1 = pd.DataFrame(rows); T1.to_csv(B3 / "B3_symmetric_scale.csv", index=False)
    L += ["## 1. Symmetric scale distribution\n", md_table(T1), ""]

    # 2. trend
    v5 = v[v.year.isin(Y5)]
    out = []
    for lab, succ in (("Strong endorsement (flag yes)", v5.flag == "yes"),
                      ("Strong endorsement, upper bound (FAILED as yes)", (v5.flag == "yes") | (v5.failed == "1")),
                      ("Advocacy (production, T4)", v5.stance == "Advocacy")):
        tab = boot_group_share(v5.year.to_numpy(), succ.to_numpy(), Y5)
        rho, p, _ = spearman_exact(Y5, tab.point.to_numpy())
        lt = logit_trend(v5.year.to_numpy(), succ.to_numpy())
        out.append({"outcome": lab, **{str(int(r.level)): f"{r.point:.2f} ({r.lo:.2f}–{r.hi:.2f}); {int(r.k)}/{int(r.n)}" for r in tab.itertuples()},
                    "Spearman ρ (exact P)": f"{rho:+.2f} ({pe(p)})",
                    "OR/yr (95% CI), P": f"{lt['OR']:.3f} ({lt['OR_lo']:.3f}–{lt['OR_hi']:.3f}), {pe(lt['P_wald'])}"})
    T2 = pd.DataFrame(out); T2.to_csv(B3 / "B3_trend.csv", index=False)
    L += ["## 2. Trend 2021–2025 (denominator: all analytic records in the year)\n",
          "Annual %, bootstrap 95% CI (1000 joint resamples, seed 42), n/N.\n", md_table(T2), ""]

    # 3. consistency
    rows = []
    for st in ("Advocacy", "Cautious Optimism"):
        for lab, ys in [("2021–Apr 2026", Y5 + [2026]), ("2021–2025", Y5)] + [(str(y), [y]) for y in Y5 + [2026]]:
            s = fav[(fav.stance == st) & fav.year.isin(ys)]
            k, n = int((s.flag == "yes").sum()), len(s)
            lo, hi = cp(k, n)
            rows.append({"production stance": st, "period": lab, "flag yes": f"{k}/{n}", "%": f"{k/n*100:.1f}",
                         "exact 95% CI": f"{lo:.1f}–{hi:.1f}", "FAILED": int((s.failed == "1").sum())})
    T3 = pd.DataFrame(rows); T3.to_csv(B3 / "B3_consistency.csv", index=False)
    L += ["## 3. Consistency checks\n", md_table(T3), ""]

    # 4. agreement with human labels (model-favourable validation records)
    val = load_validation().merge(fl, on="pmid", how="left")
    val["flag"] = val["strong_endorsement"].fillna("FAILED")
    L.append("## 4. Agreement with existing human labels (model-favourable validation records)\n")
    agree = []
    for lab, d in (("all model-favourable", val[val.model.isin(["Cautious Optimism", "Advocacy"])]),
                   ("in-scope (T2 layer A)", val[val.model.isin(["Cautious Optimism", "Advocacy"]) & ~val.out_of_layerA])):
        d = d.reset_index(drop=True)
        h = (d.human == "Advocacy").to_numpy(); f = (d.flag == "yes").to_numpy()
        tp, fn, fp, tn = int((h & f).sum()), int((h & ~f).sum()), int((~h & f).sum()), int((~h & ~f).sum())
        pt = binary_metrics_cm(tp, fn, fp, tn)
        draws = []
        for idx in boot_indices(len(d)):
            a, b = h[idx], f[idx]
            draws.append(binary_metrics_cm(int((a & b).sum()), int((a & ~b).sum()), int((~a & b).sum()), int((~a & ~b).sum())))
        D = pd.DataFrame(draws)
        ci = lambda k: np.nanpercentile(D[k], [2.5, 97.5])
        hl = d[f]["human"].value_counts()
        agree.append({"set": lab, "n": len(d), "flag FAILED": int((d.flag == "FAILED").sum()),
                      "2×2 (TP, FN, FP, TN) human Advocacy vs flag yes": f"{tp}, {fn}, {fp}, {tn}",
                      "sensitivity": f"{tp}/{tp+fn} = {pt['sensitivity']:.3f} ({ci('sensitivity')[0]:.3f}–{ci('sensitivity')[1]:.3f})",
                      "PPV": f"{tp}/{tp+fp} = {pt['PPV']:.3f} ({ci('PPV')[0]:.3f}–{ci('PPV')[1]:.3f})",
                      "Cohen κ": f"{pt['kappa']:.3f} ({ci('kappa')[0]:.3f}–{ci('kappa')[1]:.3f})",
                      "human labels among flag yes": "; ".join(f"{k} {v}" for k, v in hl.items())})
    T4 = pd.DataFrame(agree); T4.to_csv(B3 / "B3_agreement.csv", index=False)
    L += [md_table(T4), "",
          "For reference, production Advocacy vs human Advocacy on the same records is in T2 (§3, binary Advocacy view).\n"]

    # 5. corrected prevalence (T2 estimator; strata = model stance × flag; target = human Advocacy)
    def stratum(stance, flag):
        if stance in ("Alarm", "Caution", "Neutral"):
            return stance
        return f"{stance}, flag {flag if flag in ('yes', 'no') else 'FAILED'}"
    val["stratum"] = [stratum(s, f) for s, f in zip(val.model, val.flag)]
    v5 = v5.assign(stratum=[stratum(s, f) for s, f in zip(v5.stance, v5.flag)])
    strata = sorted(set(v5.stratum) | set(val.stratum))
    vh = (val.human == "Advocacy").to_numpy(float)
    vidx = {s: np.where(val.stratum.to_numpy() == s)[0] for s in strata}
    yc = np.array([Y5.index(y) for y in v5.year]); sc = np.array([strata.index(s) for s in v5.stratum])

    def est(vi, rows_):
        P = np.array([vh[vi[s]].mean() if len(vi[s]) else np.nan for s in strata])
        M = np.zeros((5, len(strata))); np.add.at(M, (yc[rows_], sc[rows_]), 1)
        Sh = M / M.sum(1, keepdims=True)
        return np.nansum(Sh * P, axis=1) * 100, Sh
    point, Sh0 = est(vidx, np.arange(len(v5)))
    rng = np.random.default_rng(SEED); draws = []
    for _ in range(N_BOOT):
        vi = {s: (ix[rng.integers(0, len(ix), len(ix))] if len(ix) else ix) for s, ix in vidx.items()}
        draws.append(est(vi, rng.integers(0, len(v5), len(v5)))[0])
    lo, hi = np.percentile(np.array(draws), [2.5, 97.5], axis=0)
    cells = pd.DataFrame({"stratum": strata, "validation n": [len(vidx[s]) for s in strata],
                          "human Advocacy in stratum": [int(vh[vidx[s]].sum()) for s in strata],
                          "P(human Advocacy | stratum)": [f"{vh[vidx[s]].mean():.3f}" if len(vidx[s]) else "no records" for s in strata],
                          "flag (<10 validation records)": ["<10" if len(vidx[s]) < 10 else "" for s in strata]})
    cells.to_csv(B3 / "B3_corrected_strata.csv", index=False)
    corr = pd.DataFrame({"year": Y5, "corrected human-Advocacy prevalence % (95% CI)":
                         [f"{p:.2f} ({a:.2f}–{b:.2f})" for p, a, b in zip(point, lo, hi)]})
    corr.to_csv(B3 / "B3_corrected_prevalence.csv", index=False)
    L += ["## 5. Secondary: misclassification-corrected prevalence (target: human Advocacy)\n",
          "Batch 1 T2 estimator with strata = model stance × flag; P(human Advocacy | stratum) from all 300 validation records; "
          "bootstrap resamples validation records within strata and corpus records jointly (1000, seed 42). Strata with no "
          "validation record contribute 0 and are listed.\n", md_table(cells), "", md_table(corr), ""]
    (B3 / "B3_analysis.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
