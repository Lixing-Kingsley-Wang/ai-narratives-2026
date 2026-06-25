"""Part 5 — build the BLIND validation set for Q7.

~120 papers stratified by pub_year × failure_mode (model labels NOT shown).
Output columns: pmid, pub_year, title, abstract, human_failure_mode, human_model_type
The two human_* columns are BLANK for the coder to fill. Model labels are
deliberately omitted; q7_kappa.py recovers them by joining back to
q7_classified_ac.csv on pmid after coding.
"""
import os
import numpy as np
import pandas as pd

SEED = 42
TARGET = 120
PER_CELL = 5
BASE = os.path.dirname(os.path.abspath(__file__))
AC   = os.path.join(BASE, "output", "analyses", "q7_classified_ac.csv")
SRC  = os.path.join(BASE, "output", "classified_medical_Q1Q2.csv")
OUT  = os.path.join(BASE, "output", "analyses", "q7_validation_blind.csv")

YEARS = ["2021","2022","2023","2024","2025","2026"]
FM    = ["confabulation","misclassification","both","none_or_unclear"]

ac = pd.read_csv(AC, dtype={"pmid": str})
ac = ac[ac["failure_mode"] != "FAILED"].copy()
ac["pub_year"] = ac["pub_year"].astype(str)

rng = np.random.RandomState(SEED)
picked = []
# pass 1: up to PER_CELL per (year, failure_mode) cell
for y in YEARS:
    for fm in FM:
        cell = ac[(ac["pub_year"] == y) & (ac["failure_mode"] == fm)]
        if len(cell):
            take = cell.sample(min(PER_CELL, len(cell)), random_state=rng)
            picked.append(take)
picked = pd.concat(picked) if picked else ac.head(0)
picked = picked.drop_duplicates("pmid")
print(f"After stratified pass: {len(picked)} papers")

# pass 2: top up to TARGET from the remaining pool, weighted to fill rarer fm
if len(picked) < TARGET:
    remaining = ac[~ac["pmid"].isin(picked["pmid"])]
    need = TARGET - len(picked)
    extra = remaining.sample(min(need, len(remaining)), random_state=rng)
    picked = pd.concat([picked, extra]).drop_duplicates("pmid")
print(f"After top-up: {len(picked)} papers (target {TARGET})")

# distribution report (for our own QA; not shown to coder)
print("\nHidden strata (model labels — for QA only, NOT in blind file):")
print(pd.crosstab(picked["failure_mode"], picked["pub_year"]).reindex(
      index=FM, columns=YEARS, fill_value=0).to_string())

# attach title + abstract
src = pd.read_csv(SRC, dtype={"pmid": str})[["pmid","title","abstract"]]
blind = picked[["pmid","pub_year"]].merge(src, on="pmid", how="left")

# shuffle so cell order does not leak the hidden stratum
blind = blind.sample(frac=1.0, random_state=SEED).reset_index(drop=True)
blind["human_failure_mode"] = ""
blind["human_model_type"]   = ""
blind = blind[["pmid","pub_year","title","abstract","human_failure_mode","human_model_type"]]
blind.to_csv(OUT, index=False)
print(f"\nSaved BLIND validation set → {OUT}  ({len(blind)} rows)")
print("Coder fills human_failure_mode ∈ {confabulation, misclassification, both, none_or_unclear}")
print("            human_model_type   ∈ {generative, discriminative, both, unclear}")
print("Then run: python q7_kappa.py")
