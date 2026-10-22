"""T3 · Failure-mode and model-type confusion matrices (X4a).

Reproduces q7_kappa.py --require-abstract (blind human codes from
output/analyses/q7_validation_coding.xlsx, sheet 'Coding'; model labels from
output/analyses/q7_classified_ac.csv; no adjudication), then adds per-class
metrics and the direction of fabrication disagreements.
Outputs: revision_r1/outputs/T3_*.csv, T3_mechanism_confusion.md
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from r1_common import (OUT, REPO_OUT, cohen_kappa_cm, confusion, gwet_ac1_cm, kappa_max_cm,
                       md_table, pabak_cm)
from t2_stance_perclass import fmt_pc, perclass_table

FM = ["confabulation", "misclassification", "both", "none_or_unclear"]
MT = ["generative", "discriminative", "both", "unclear"]
FM_DISPLAY = {"confabulation": "Confabulation (fabrication)", "misclassification": "Misclassification (factual error)",
              "both": "Both", "none_or_unclear": "None or unclear"}
MT_DISPLAY = {"generative": "Generative", "discriminative": "Discriminative", "both": "Both", "unclear": "Unclear"}

REPORTED = {"failure_mode": {"kappa": 0.57, "AC1": 0.60, "raw": 69.4, "kmax": 0.76, "k/kmax": 0.76},
            "model_type": {"kappa": 0.84, "AC1": 0.89, "raw": 90.7, "kmax": None, "k/kmax": 0.86}}


def rhu(x, dp):
    """Round half up (manuscript convention), not Python's float round."""
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP))


def load():
    b = pd.read_excel(REPO_OUT / "analyses/q7_validation_coding.xlsx", sheet_name="Coding",
                      dtype={"pmid": str})
    for c in ("human_failure_mode", "human_model_type"):
        b[c] = b[c].astype(str).str.strip().str.lower()
    n_all = len(b)
    has = b["abstract"].fillna("").astype(str).str.strip().str.len() > 0
    b = b[has].copy()
    m = pd.read_csv(REPO_OUT / "analyses/q7_classified_ac.csv", dtype={"pmid": str})[
        ["pmid", "failure_mode", "model_type"]]
    d = b.merge(m, on="pmid", how="left")
    d = d[d["human_failure_mode"].isin(FM) | d["human_model_type"].isin(MT)].copy()
    return d, n_all, int((~has).sum())


def cm_md(cm, labels, disp):
    df = pd.DataFrame(cm, index=[disp[l] for l in labels], columns=[disp[l] for l in labels])
    df["Row total"] = df.sum(axis=1)
    df.loc["Column total"] = df.sum(axis=0)
    return md_table(df.reset_index().rename(columns={"index": "Human code \\ Model label"}), "{:.0f}")


def main():
    d, n_all, n_title = load()
    L = ["# T3 · Failure-mode and model-type confusion matrices (X4a)\n",
         "Script: `revision_r1/scripts/t3_mechanism_confusion.py`. Human codes: blind coding sheet "
         "`output/analyses/q7_validation_coding.xlsx` (sheet `Coding`), **not** the adjudicated labels. "
         "Model labels: `output/analyses/q7_classified_ac.csv`. Same join and abstract filter as "
         f"`q7_kappa.py --require-abstract`: {n_all} validation records, {n_title} title-only dropped, "
         f"n = {len(d)}.\n",
         "## 1. Reproduction of reported statistics\n"]
    rep_rows = []
    out_csv = []
    blocks = {}
    for axis, hcol, mcol, labels, disp in [("failure_mode", "human_failure_mode", "failure_mode", FM, FM_DISPLAY),
                                           ("model_type", "human_model_type", "model_type", MT, MT_DISPLAY)]:
        sub = d[d[hcol].isin(labels) & d[mcol].isin(labels)]
        cm = confusion(sub[hcol], sub[mcol], labels)
        k = cohen_kappa_cm(cm); ac1 = gwet_ac1_cm(cm); raw = np.trace(cm) / cm.sum() * 100
        km = kappa_max_cm(cm)
        rep = REPORTED[axis]
        checks = [("Cohen κ", k, rep["kappa"], 2), ("Gwet AC1", ac1, rep["AC1"], 2),
                  ("raw agreement %", raw, rep["raw"], 1), ("κ_max", km, rep["kmax"], 2),
                  ("κ/κ_max", k / km, rep["k/kmax"], 2)]
        for name, val, target, dp in checks:
            if target is None:
                ok = "n/a (not reported)"
            elif rhu(val, dp) == target:
                ok = "match"
            elif rhu(rhu(val, 3), dp) == target:
                ok = f"match only via 3-dp intermediate rounding ({val:.5f} → {rhu(val, 3):.3f} → {target})"
            else:
                ok = "**MISMATCH**"
            rep_rows.append({"axis": axis, "statistic": name, "recomputed": round(val, 4),
                             "manuscript": "" if target is None else target, "status": ok})
        blocks[axis] = (sub, cm, labels, disp, hcol, mcol, pabak_cm(cm))
        pd.DataFrame(cm, index=labels, columns=labels).to_csv(OUT / f"T3_confusion_{axis}.csv")
    L.append(md_table(pd.DataFrame(rep_rows)))
    L.append("")

    for axis, title in [("failure_mode", "Failure mode"), ("model_type", "Model type")]:
        sub, cm, labels, disp, hcol, mcol, pabak = blocks[axis]
        L.append(f"## 2. {title}: 4×4 confusion matrix (n={cm.sum()})\n")
        L.append(cm_md(cm, labels, disp))
        L.append(f"\nPABAK = {pabak:.3f}.\n")
        pc = perclass_table(sub[hcol].to_numpy(), sub[mcol].to_numpy(), labels)
        pc.insert(0, "axis", axis); out_csv.append(pc)
        L.append("Per-class precision, recall, F1 (bootstrap 95% CI, 1000 resamples of the "
                 f"{cm.sum()} records, seed 42):\n")
        L.append(md_table(fmt_pc(pc.drop(columns=["axis"]))))
        L.append("")
    pd.concat(out_csv).to_csv(OUT / "T3_perclass_metrics.csv", index=False)

    # ---- direction of fabrication disagreement --------------------------
    sub, cm, *_ = blocks["failure_mode"]
    hf = sub["human_failure_mode"].isin(["confabulation", "both"])
    mf = sub["failure_mode"].isin(["confabulation", "both"])
    tab = pd.DataFrame({"": ["Human: fabrication-involved", "Human: not fabrication", "Column total"],
                        "Model: fabrication-involved": [int((hf & mf).sum()), int((~hf & mf).sum()), int(mf.sum())],
                        "Model: not fabrication": [int((hf & ~mf).sum()), int((~hf & ~mf).sum()), int((~mf).sum())]})
    tab["Row total"] = tab.iloc[:, 1] + tab.iloc[:, 2]
    tab.to_csv(OUT / "T3_fabrication_direction.csv", index=False)
    mh = sub[(~hf) & mf]; hm = sub[hf & (~mf)]
    L.append("## 3. Direction of fabrication disagreement\n")
    L.append("Fabrication-involved = confabulation or both.\n")
    L.append(md_table(tab, "{:.0f}"))
    L.append("")
    L.append(f"- Model said fabrication-involved, human did not: **{len(mh)}** "
             f"({', '.join(f'human {a}: {b}' for a, b in mh['human_failure_mode'].value_counts().items())}).")
    L.append(f"- Human said fabrication-involved, model did not: **{len(hm)}** "
             f"({', '.join(f'model {a}: {b}' for a, b in hm['failure_mode'].value_counts().items())}).")
    L.append(f"- Fabrication-involved prevalence in the validation set: human {int(hf.sum())}/{len(sub)} "
             f"({hf.mean()*100:.1f}%), model {int(mf.sum())}/{len(sub)} ({mf.mean()*100:.1f}%).")
    # exact McNemar
    from scipy.stats import binomtest
    b_, c_ = len(mh), len(hm)
    p_mc = binomtest(min(b_, c_), b_ + c_, 0.5).pvalue if b_ + c_ else float("nan")
    L.append(f"- Exact McNemar (binomial) test of the discordant pairs {b_} vs {c_}: P {'< .001' if p_mc < 0.001 else '= ' + format(p_mc, '.3f')} (exact P = {p_mc:.2e}).")
    # confab only (strict)
    hs = sub["human_failure_mode"] == "confabulation"; ms = sub["failure_mode"] == "confabulation"
    L.append(f"- Strict confabulation only: model yes / human no = {int((ms & ~hs).sum())}; "
             f"human yes / model no = {int((hs & ~ms).sum())}.\n")
    L.append("Validation-set sampling (from Methods): 120 records stratified by year and assigned failure "
             "mode, so these prevalences are not corpus prevalences.\n")

    # ---- draft supplementary table --------------------------------------
    L.append("## 4. Draft supplementary table (Table S18 style)\n")
    L.append("**Table S19 (draft). Human versus model mechanism labels in the validation sample (n = "
             f"{cm.sum()} abstract-present records).** Rows give the blinded human code and columns the "
             "model label. (a) Failure mode. (b) Model type. (c) Per-class precision, recall, and F1 with "
             "95% percentile bootstrap CIs (1000 resamples, seed 42). Confabulation is reported in the main "
             "text as fabrication and misclassification as factual error.\n")
    for tag, axis in [("a", "failure_mode"), ("b", "model_type")]:
        sub, cmx, labels, disp, *_ = blocks[axis]
        L.append(f"{tag})\n")
        L.append(cm_md(cmx, labels, disp))
        L.append("")
    L.append("c)\n")
    rows = []
    for axis, title in [("failure_mode", "Failure mode"), ("model_type", "Model type")]:
        pc = pd.read_csv(OUT / "T3_perclass_metrics.csv")
        pc = pc[pc["axis"] == axis].drop(columns=["axis"])
        disp = FM_DISPLAY if axis == "failure_mode" else MT_DISPLAY
        f = fmt_pc(pc)
        f["class"] = f["class"].map(lambda x: disp.get(x, x))
        f.insert(0, "Axis", title)
        rows.append(f)
    L.append(md_table(pd.concat(rows)))
    L.append("\n## Output files\n")
    for fn in ["T3_confusion_failure_mode.csv", "T3_confusion_model_type.csv", "T3_perclass_metrics.csv",
               "T3_fabrication_direction.csv"]:
        L.append(f"- [{fn}]({fn})")
    (OUT / "T3_mechanism_confusion.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
