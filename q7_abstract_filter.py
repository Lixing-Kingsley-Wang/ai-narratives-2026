"""Shared QC helper: the set of pmids in the corpus that carry a non-empty
abstract. Used to restrict Q7 analyses to abstract-present papers (title-only
papers are dropped as quality control)."""
import os, csv

def abstract_present_pmids(base_dir):
    src = os.path.join(base_dir, "output", "classified_medical_Q1Q2.csv")
    keep = set()
    with open(src, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if (r.get("abstract") or "").strip():
                keep.add(r["pmid"])
    return keep
