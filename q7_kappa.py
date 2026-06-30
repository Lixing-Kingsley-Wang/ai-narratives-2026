"""Part 5 — per-axis Cohen's κ for the Q7 validation set.

Reads the filled blind file (output/analyses/q7_validation_blind.csv) and joins
back to q7_classified_ac.csv on pmid to recover the model labels, then reports
for each axis (failure_mode, model_type): Cohen's κ, raw agreement, and the
confusion matrix. Runs only on rows the human has filled.
"""
import os, sys, argparse
import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score, confusion_matrix

BASE  = os.path.dirname(os.path.abspath(__file__))
XLSX  = os.path.join(BASE, "output", "analyses", "q7_validation_coding.xlsx")
BLIND = os.path.join(BASE, "output", "analyses", "q7_validation_blind.csv")
AC    = os.path.join(BASE, "output", "analyses", "q7_classified_ac.csv")
ADJ   = os.path.join(BASE, "output", "analyses", "q7_adjudication.xlsx")

FM_LABELS = ["confabulation","misclassification","both","none_or_unclear"]
MT_LABELS = ["generative","discriminative","both","unclear"]

def load_coding():
    """Prefer the filled coding workbook (sheet 'Coding'); else the blind CSV."""
    if os.path.exists(XLSX):
        b = pd.read_excel(XLSX, sheet_name="Coding", dtype={"pmid": str})
        print(f"Source: {os.path.basename(XLSX)} (sheet 'Coding')")
        return b
    if os.path.exists(BLIND):
        print(f"Source: {os.path.basename(BLIND)}")
        return pd.read_csv(BLIND, dtype={"pmid": str})
    sys.exit(f"No coding file found: {XLSX} or {BLIND}")

def apply_adjudication(df):
    """Overwrite human labels with the FINAL adjudicated calls (by pmid).

    For each contested cell the coder filled in q7_adjudication.xlsx, the FINAL
    label replaces the original blind code; agreed axes are untouched.
    """
    if not os.path.exists(ADJ):
        sys.exit(f"--adjudicated requested but not found: {ADJ}")
    a = pd.read_excel(ADJ, sheet_name="Adjudicate", dtype={"pmid": str})
    a = a.rename(columns={"FINAL_failure_mode": "adj_fm", "FINAL_model_type": "adj_mt"})
    for c in ("adj_fm", "adj_mt"):
        a[c] = a[c].astype(str).str.strip().str.lower()
    fm_map = dict(zip(a.loc[a["adj_fm"].isin(FM_LABELS), "pmid"],
                      a.loc[a["adj_fm"].isin(FM_LABELS), "adj_fm"]))
    mt_map = dict(zip(a.loc[a["adj_mt"].isin(MT_LABELS), "pmid"],
                      a.loc[a["adj_mt"].isin(MT_LABELS), "adj_mt"]))
    blank = a[(~a["adj_fm"].isin(FM_LABELS)) & (~a["adj_mt"].isin(MT_LABELS))]
    df["human_failure_mode"] = df.apply(
        lambda r: fm_map.get(r["pmid"], r["human_failure_mode"]), axis=1)
    df["human_model_type"] = df.apply(
        lambda r: mt_map.get(r["pmid"], r["human_model_type"]), axis=1)
    print(f"Adjudication applied: {len(fm_map)} failure_mode + {len(mt_map)} model_type "
          f"FINAL labels merged from {os.path.basename(ADJ)}.")
    if len(blank):
        print(f"  WARNING: {len(blank)} adjudication rows still have BOTH FINAL cells blank.")
    return df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--adjudicated", action="store_true",
                    help="merge FINAL labels from q7_adjudication.xlsx before scoring")
    ap.add_argument("--require-abstract", action="store_true",
                    help="QC: drop title-only papers (empty abstract) before scoring")
    args = ap.parse_args()

    blind = load_coding()
    for c in ("human_failure_mode","human_model_type"):
        if c not in blind.columns:
            sys.exit(f"Missing column '{c}' in coding file.")
    # normalize human columns up front so adjudication merge compares cleanly
    for c in ("human_failure_mode","human_model_type"):
        blind[c] = blind[c].astype(str).str.strip().str.lower()
    if args.adjudicated:
        blind = apply_adjudication(blind)
    if args.require_abstract:
        if "abstract" not in blind.columns:
            sys.exit("--require-abstract needs an 'abstract' column in the coding file.")
        has = blind["abstract"].fillna("").astype(str).str.strip().str.len() > 0
        print(f"QC: dropping {int((~has).sum())} title-only papers (empty abstract); "
              f"keeping {int(has.sum())}.")
        blind = blind[has].copy()

    model = pd.read_csv(AC, dtype={"pmid": str})[["pmid","failure_mode","model_type"]]
    df = blind.merge(model, on="pmid", how="left",
                     suffixes=("", "_model"))

    # a row counts as "coded" only if it carries a valid label on at least one axis
    for c in ("human_failure_mode","human_model_type"):
        df[c] = df[c].astype(str).str.strip().str.lower()
    coded = df[df["human_failure_mode"].isin(FM_LABELS) |
               df["human_model_type"].isin(MT_LABELS)].copy()
    n_total, n_coded = len(df), len(coded)
    print(f"Validation rows: {n_total} | coded so far: {n_coded}")
    if n_coded == 0:
        print("No rows coded yet — fill human_failure_mode / human_model_type and re-run.")
        return

    def landis_koch(k):
        return ("poor" if k < 0 else "slight" if k < 0.20 else "fair" if k < 0.40
                else "moderate" if k < 0.60 else "substantial" if k < 0.80
                else "almost perfect")

    def agreement_coefficients(cm):
        """From a confusion matrix return a dict of agreement coefficients.

        Cohen κ uses each rater's own marginals for chance; Scott π/Fleiss use the
        pooled marginal; Gwet AC1 is robust to the prevalence (base-rate) paradox;
        PABAK assumes uniform chance; κ_max is the best κ achievable given the two
        marginals (a marginal mismatch / bias caps it below 1).
        """
        M = cm.astype(float); N = M.sum(); k = M.shape[0]
        po = np.trace(M) / N
        Hk = M.sum(1) / N; Mk = M.sum(0) / N
        pe_cohen = (Hk * Mk).sum()
        pi = (M.sum(1) + M.sum(0)) / (2 * N)          # pooled marginal
        pe_scott = (pi ** 2).sum()
        pe_gwet  = (pi * (1 - pi)).sum() / (k - 1)
        po_max   = np.minimum(Hk, Mk).sum()
        kap   = (po - pe_cohen) / (1 - pe_cohen)
        kmax  = (po_max - pe_cohen) / (1 - pe_cohen)
        return {
            "p_o": po, "p_e_cohen": pe_cohen,
            "cohen_kappa": kap,
            "scott_pi":    (po - pe_scott) / (1 - pe_scott),
            "gwet_ac1":    (po - pe_gwet) / (1 - pe_gwet),
            "pabak":       (po - 1/k) / (1 - 1/k),
            "kappa_max":   kmax,
            "kappa_over_max": kap / kmax if kmax else float("nan"),
        }

    def per_category_kappa(cm, labels):
        """One-vs-rest Cohen κ for each category (localizes disagreement)."""
        M = cm.astype(float); N = M.sum(); out = {}
        for i, l in enumerate(labels):
            TP = M[i, i]; H = M[i].sum(); Mc = M[:, i].sum()
            a = np.array([[TP, H - TP], [Mc - TP, N - H - Mc + TP]])
            po = (a[0, 0] + a[1, 1]) / N
            hh = a.sum(1) / N; mm = a.sum(0) / N; pe = (hh * mm).sum()
            out[l] = ((po - pe) / (1 - pe) if pe < 1 else float("nan"), po)
        return out

    md = ["# Q7 validation — inter-rater agreement (human vs classifier)\n",
          f"Coded rows: **{n_coded}/{n_total}**. Primary statistic: unweighted Cohen's "
          "κ (nominal). Also reported: Scott's π / Fleiss (pooled-marginal chance), "
          "**Gwet's AC1** (robust to the prevalence paradox), PABAK (uniform chance), "
          "and **κ_max** (best κ achievable given the two marginals — a bias/marginal "
          "mismatch caps it below 1). Weighted κ is intentionally NOT used: these "
          "categories are nominal, not ordinal. Strength labels per Landis & Koch (1977).\n"]

    def report(axis, human_col, model_col, labels):
        h = coded[human_col]
        m = coded[model_col].astype(str).str.strip().str.lower()
        valid = h.isin(labels) & m.isin(labels)
        bad = (~valid).sum()
        h, m = h[valid], m[valid]
        if len(h) == 0:
            print(f"\n[{axis}] no valid coded rows."); return
        kappa = cohen_kappa_score(h, m, labels=labels)
        agree = (h.values == m.values).mean()
        cm = confusion_matrix(h, m, labels=labels)
        co = agreement_coefficients(cm)
        pck = per_category_kappa(cm, labels)
        print(f"\n{'='*70}\n[{axis}]  n={len(h)}"
              + (f"  ({bad} rows with out-of-vocab labels skipped)" if bad else ""))
        print(f"  Cohen's kappa : {kappa:+.3f}  ({landis_koch(kappa)})")
        print(f"  raw agreement : {agree*100:.1f}%   (chance p_e={co['p_e_cohen']:.3f})")
        print(f"  Scott π/Fleiss: {co['scott_pi']:+.3f} | Gwet AC1: {co['gwet_ac1']:+.3f} | "
              f"PABAK: {co['pabak']:+.3f}")
        print(f"  kappa_max     : {co['kappa_max']:.3f}  (κ/κ_max = {co['kappa_over_max']:.2f})")
        cmdf = pd.DataFrame(cm, index=[f"H:{l}" for l in labels],
                            columns=[f"M:{l}" for l in labels])
        print("  confusion matrix (rows=human, cols=model):")
        print(cmdf.to_string())
        print("  per-category one-vs-rest κ:")
        for l, (kk, pa) in pck.items():
            print(f"    {l:18s} κ={kk:+.3f}  agreement={pa*100:.1f}%")
        md.append(f"\n## {axis}\n")
        md.append(f"- n = {len(h)}{f' ({bad} out-of-vocab skipped)' if bad else ''}")
        md.append(f"- **Cohen's κ = {kappa:+.3f}** ({landis_koch(kappa)}); raw agreement "
                  f"= {agree*100:.1f}% (chance p_e = {co['p_e_cohen']:.3f})")
        md.append(f"- Scott's π / Fleiss = {co['scott_pi']:+.3f} · "
                  f"**Gwet's AC1 = {co['gwet_ac1']:+.3f}** · PABAK = {co['pabak']:+.3f}")
        md.append(f"- κ_max = {co['kappa_max']:.3f} (κ/κ_max = {co['kappa_over_max']:.2f}) "
                  "— marginal mismatch caps the achievable κ\n")
        md.append("Confusion matrix (rows = human, cols = model):\n")
        md.append("| | " + " | ".join(cmdf.columns) + " |")
        md.append("|" + "---|" * (len(cmdf.columns) + 1))
        for idx, row in cmdf.iterrows():
            md.append(f"| **{idx}** | " + " | ".join(str(v) for v in row.values) + " |")
        md.append("\nPer-category one-vs-rest κ:\n")
        md.append("| category | κ | agreement |")
        md.append("|---|--:|--:|")
        for l, (kk, pa) in pck.items():
            md.append(f"| {l} | {kk:+.3f} | {pa*100:.1f}% |")
        md.append("")

    report("failure_mode", "human_failure_mode", "failure_mode", FM_LABELS)
    report("model_type",   "human_model_type",   "model_type",   MT_LABELS)

    suffix = ("_adjudicated" if args.adjudicated else "") + \
             ("_abstractonly" if args.require_abstract else "")
    # disagreement rows (post-adjudication these are the residual unresolved ones)
    dis = coded[(coded["human_failure_mode"] != coded["failure_mode"].str.lower()) |
                (coded["human_model_type"]   != coded["model_type"].str.lower())]
    keep = ["pmid","pub_year","human_failure_mode","failure_mode",
            "human_model_type","model_type"]
    keep = [c for c in keep if c in dis.columns]
    if not args.adjudicated and not args.require_abstract:  # only the canonical blind-120 run writes disagreements
        out_dis = os.path.join(BASE, "output", "analyses", "q7_validation_disagreements.csv")
        dis[keep].to_csv(out_dis, index=False)
        print(f"\nDisagreements ({len(dis)} rows) → {out_dis}")
    out_md = os.path.join(BASE, "output", "analyses", f"q7_kappa_report{suffix}.md")
    with open(out_md, "w") as f:
        f.write("\n".join(md))
    print(f"Report → {out_md}")
    if args.adjudicated:
        print(f"(residual disagreements after adjudication: {len(dis)} rows)")

if __name__ == "__main__":
    main()
