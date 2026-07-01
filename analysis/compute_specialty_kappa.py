"""Specialty validation — human-vs-classifier agreement (nominal Cohen's κ).

Parallel to q7_kappa.py, for the 18-way clinical-specialty classifier. Run this
AFTER filling human_specialty in the blind coding sheet.

Reads:
  output/analyses/specialty_validation_sample.xlsx  (sheet 'Coding': pmid, human_specialty)
  output/analyses/specialty_validation_key.csv      (pmid, model_specialty  — hidden key)

Writes:
  output/analyses/specialty_kappa_report.md

Specialty labels are NOMINAL (unordered), so κ is UNWEIGHTED. The human sheet has
one extra option, "Unclear / cannot determine from abstract"; agreement is reported
BOTH with that option kept as its own category and with those rows excluded
(sensitivity), so you can report whichever is cleaner.
"""
import os, sys
import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score, confusion_matrix

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # repo root
XLSX = os.path.join(BASE, "output", "analyses", "specialty_validation_sample.xlsx")
KEY  = os.path.join(BASE, "output", "analyses", "specialty_validation_key.csv")
OUT_MD  = os.path.join(BASE, "output", "analyses", "specialty_kappa_report.md")
OUT_DIS = os.path.join(BASE, "output", "analyses", "specialty_validation_disagreements.csv")

# canonical 18-way taxonomy (verbatim, from analysis/classify_specialty.py)
CANON = [
    "Radiology / Diagnostic Imaging",
    "Pathology / Laboratory Medicine",
    "Cardiology",
    "Oncology",
    "Surgery",
    "Ophthalmology",
    "Dermatology",
    "Neurology / Neuroscience",
    "Mental Health / Psychiatry",
    "Internal Medicine / Primary Care",
    "Emergency Medicine / Critical Care",
    "Pediatrics",
    "Obstetrics / Gynecology",
    "Dentistry",
    "Medical Informatics / Digital Health",
    "Nursing",
    "Medical Education",
    "Multidisciplinary / Other",
]
UNCLEAR = "Unclear / cannot determine from abstract"


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
    kap   = (po - pe_cohen) / (1 - pe_cohen) if pe_cohen < 1 else float("nan")
    kmax  = (po_max - pe_cohen) / (1 - pe_cohen) if pe_cohen < 1 else float("nan")
    return {
        "p_o": po, "p_e_cohen": pe_cohen,
        "cohen_kappa": kap,
        "scott_pi":    (po - pe_scott) / (1 - pe_scott) if pe_scott < 1 else float("nan"),
        "gwet_ac1":    (po - pe_gwet) / (1 - pe_gwet) if pe_gwet < 1 else float("nan"),
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


def load_coding():
    if not os.path.exists(XLSX):
        sys.exit(f"Coding sheet not found: {XLSX}")
    b = pd.read_excel(XLSX, sheet_name="Coding", dtype={"pmid": str})
    if "human_specialty" not in b.columns:
        sys.exit("Missing column 'human_specialty' in the coding sheet.")
    b["human_specialty"] = b["human_specialty"].fillna("").astype(str).str.strip()
    return b[["pmid", "human_specialty"]]


def block(md, title, coded, labels, note):
    """Score one label-set and append a full Q7-format block to `md`. Returns dict."""
    h = coded["human_specialty"]
    m = coded["model_specialty"]
    valid = h.isin(labels) & m.isin(labels)
    bad = int((~valid).sum())
    h, m = h[valid], m[valid]
    print(f"\n{'='*70}\n[{title}]  n={len(h)}"
          + (f"  ({bad} rows with out-of-vocab labels skipped)" if bad else ""))
    md.append(f"\n## {title}\n")
    md.append(note + "\n")
    if len(h) == 0:
        print("  no valid coded rows.")
        md.append("_No valid coded rows yet._\n")
        return None

    kappa = cohen_kappa_score(h, m, labels=labels)
    agree = (h.values == m.values).mean()
    cm = confusion_matrix(h, m, labels=labels)
    co = agreement_coefficients(cm)
    pck = per_category_kappa(cm, labels)

    print(f"  Cohen's kappa : {kappa:+.3f}  ({landis_koch(kappa)})")
    print(f"  raw agreement : {agree*100:.1f}%   (chance p_e={co['p_e_cohen']:.3f})")
    print(f"  Scott π/Fleiss: {co['scott_pi']:+.3f} | Gwet AC1: {co['gwet_ac1']:+.3f} | "
          f"PABAK: {co['pabak']:+.3f}")
    print(f"  kappa_max     : {co['kappa_max']:.3f}  (κ/κ_max = {co['kappa_over_max']:.2f})")

    cmdf = pd.DataFrame(cm, index=[f"H:{l}" for l in labels],
                        columns=[f"M:{l}" for l in labels])

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
    return {"n": len(h), "kappa": kappa}


def main():
    coding = load_coding()
    key = pd.read_csv(KEY, dtype={"pmid": str})[["pmid", "model_specialty"]]
    key["model_specialty"] = key["model_specialty"].astype(str).str.strip()
    df = coding.merge(key, on="pmid", how="left")

    ALL_HUMAN = set(CANON) | {UNCLEAR}
    coded = df[df["human_specialty"].isin(ALL_HUMAN)].copy()
    n_total, n_coded = len(df), len(coded)
    print(f"Validation rows: {n_total} | coded so far: {n_coded}")
    if n_coded == 0:
        print("No rows coded yet — fill human_specialty in the coding sheet and re-run.")
        return

    md = ["# Specialty validation — inter-rater agreement (human vs classifier)\n",
          f"Coded rows: **{n_coded}/{n_total}**. Primary statistic: unweighted Cohen's "
          "κ (nominal — specialty labels are unordered). Also reported: Scott's π / "
          "Fleiss (pooled-marginal chance), **Gwet's AC1** (robust to the prevalence "
          "paradox), PABAK (uniform chance), and **κ_max** (best κ achievable given the "
          "two marginals — a bias/marginal mismatch caps it below 1). Weighted κ is "
          "intentionally NOT used. Strength labels per Landis & Koch (1977).\n"]

    # (A) keep "Unclear" as its own category
    block(md, "specialty — including 'Unclear' as a category",
          coded, CANON + [UNCLEAR],
          "Human 'Unclear / cannot determine from abstract' is treated as its own "
          "category. The model never emits it, so its model column is all-zero.")

    # (B) sensitivity: drop rows the human marked Unclear
    coded_excl = coded[coded["human_specialty"] != UNCLEAR].copy()
    n_uncl = n_coded - len(coded_excl)
    block(md, "specialty — excluding 'Unclear' (sensitivity)",
          coded_excl, CANON,
          f"Sensitivity analysis: the {n_uncl} row(s) the human marked "
          "'Unclear / cannot determine from abstract' are excluded; only the 18 "
          "canonical categories are scored.")

    # disagreements (canonical-vs-canonical rows where human ≠ model)
    valid = coded["human_specialty"].isin(CANON) & coded["model_specialty"].isin(CANON)
    dis = coded[valid & (coded["human_specialty"] != coded["model_specialty"])]
    dis[["pmid", "human_specialty", "model_specialty"]].to_csv(OUT_DIS, index=False)
    print(f"\nDisagreements ({len(dis)} rows) → {OUT_DIS}")

    with open(OUT_MD, "w") as f:
        f.write("\n".join(md))
    print(f"Report → {OUT_MD}")


if __name__ == "__main__":
    main()
