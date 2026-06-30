"""Sensitivity of validation κ to (a) adjudication and (b) dropping no-abstract
papers. Pure QC view — does not alter any rater's labels.
"""
import os
import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score, confusion_matrix

BASE = "/Users/kingslywang/repos/ai-narratives-2026"
WT   = os.path.join(BASE, ".claude/worktrees/recursing-blackwell-3becf5/output/analyses")
AC   = os.path.join(BASE, "output/analyses/q7_classified_ac.csv")
FM = ["confabulation","misclassification","both","none_or_unclear"]
MT = ["generative","discriminative","both","unclear"]

cod = pd.read_excel(os.path.join(WT,"q7_validation_coding.xlsx"), sheet_name="Coding", dtype={"pmid":str})
adj = pd.read_excel(os.path.join(WT,"q7_adjudication.xlsx"), sheet_name="Adjudicate", dtype={"pmid":str})
mdl = pd.read_csv(AC, dtype={"pmid":str})[["pmid","failure_mode","model_type"]]

for c in ("human_failure_mode","human_model_type"):
    cod[c] = cod[c].astype(str).str.strip().str.lower()
cod["has_abstract"] = cod["abstract"].fillna("").astype(str).str.strip().str.len() > 0

# adjudicated (FINAL) human labels merged over blind
adj["FINAL_failure_mode"] = adj["FINAL_failure_mode"].astype(str).str.strip().str.lower()
adj["FINAL_model_type"]   = adj["FINAL_model_type"].astype(str).str.strip().str.lower()
fm_map = dict(zip(adj.loc[adj.FINAL_failure_mode.isin(FM),"pmid"], adj.loc[adj.FINAL_failure_mode.isin(FM),"FINAL_failure_mode"]))
mt_map = dict(zip(adj.loc[adj.FINAL_model_type.isin(MT),"pmid"],   adj.loc[adj.FINAL_model_type.isin(MT),"FINAL_model_type"]))
cod["adj_failure_mode"] = cod.apply(lambda r: fm_map.get(r.pmid, r.human_failure_mode), axis=1)
cod["adj_model_type"]   = cod.apply(lambda r: mt_map.get(r.pmid, r.human_model_type), axis=1)

df = cod.merge(mdl, on="pmid", how="left")

def gwet_ac1(cm):
    M=cm.astype(float); N=M.sum(); k=M.shape[0]
    po=np.trace(M)/N; pi=(M.sum(1)+M.sum(0))/(2*N)
    pe=(pi*(1-pi)).sum()/(k-1)
    return (po-pe)/(1-pe)

def score(sub, hcol, mcol, labels):
    h=sub[hcol]; m=sub[mcol].astype(str).str.strip().str.lower()
    v=h.isin(labels)&m.isin(labels); h,m=h[v],m[v]
    k=cohen_kappa_score(h,m,labels=labels); ag=(h.values==m.values).mean()
    cm=confusion_matrix(h,m,labels=labels)
    return len(h), k, gwet_ac1(cm), ag

n_noabs = (~df["has_abstract"]).sum()
print(f"Validation n=120 | no-abstract (title-only)={n_noabs} | with-abstract={120-n_noabs}")
# how many no-abstract papers were in the original 46 disagreements?
df["blind_disagree"] = (df.human_failure_mode != df.failure_mode.str.lower()) | \
                       (df.human_model_type   != df.model_type.str.lower())
print(f"no-abstract papers among the 46 blind disagreements: "
      f"{df[(~df.has_abstract)&df.blind_disagree].shape[0]} of {n_noabs}")
print(f"  (so {df[(~df.has_abstract)&df.blind_disagree].shape[0]}/{df.blind_disagree.sum()} of all disagreements are title-only)")

print("\n" + "="*94)
print(f"{'axis':<14}{'rater':<13}{'subset':<18}{'n':>4}{'Cohen κ':>10}{'Gwet AC1':>10}{'raw agree':>11}")
print("="*94)
for axis,(hcol_b,hcol_a,mcol,labels) in {
    "failure_mode":("human_failure_mode","adj_failure_mode","failure_mode",FM),
    "model_type":  ("human_model_type","adj_model_type","model_type",MT),
}.items():
    for rater,hcol in [("blind",hcol_b),("adjudicated",hcol_a)]:
        for subset,mask in [("all 120",pd.Series(True,index=df.index)),
                             ("abstract-only",df.has_abstract)]:
            n,k,ac1,ag = score(df[mask], hcol, mcol, labels)
            print(f"{axis:<14}{rater:<13}{subset:<18}{n:>4}{k:>+10.3f}{ac1:>+10.3f}{ag*100:>10.1f}%")
    print("-"*94)
